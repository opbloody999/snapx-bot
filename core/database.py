# Database Management using Turso (libSQL)
# Handles: users, shortened links, video-only groups

import os
import libsql_experimental as libsql
from datetime import datetime
from core.logger import log_db_link_saved, log_db_link_query, log_db_link_found, log_db_reconnect, log_db_init

# Get database credentials
TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL", "")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN", "")

# Database connection variable
db = None

def reconnect_db():
    """Reconnect to database when connection expires"""
    global db
    
    if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
        return None
    
    try:
        db = libsql.connect(TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN)  # type: ignore
        log_db_reconnect(True)
        return db
    except Exception as e:
        log_db_reconnect(False, e)
        return None

def execute_with_retry(query, params=None, needs_commit=False, max_retries=2):
    """Execute database query with automatic retry on connection errors and optional commit"""
    global db
    
    for attempt in range(max_retries):
        try:
            if not db:
                if not reconnect_db():
                    return None
            
            # Execute query
            if params:
                result = db.execute(query, params)
            else:
                result = db.execute(query)
            
            # Commit if this is a write operation
            if needs_commit:
                db.commit()
                
            return result
                
        except ValueError as e:
            error_msg = str(e)
            # Check if it's a stream expiration error
            if "stream not found" in error_msg and attempt < max_retries - 1:
                print(f"⚠️ Connection expired, reconnecting... (attempt {attempt + 1}/{max_retries})")
                reconnect_db()
                continue
            else:
                raise
        except Exception as e:
            raise
    
    return None

# Initialize database connection on startup
if TURSO_DATABASE_URL and TURSO_AUTH_TOKEN:
    try:
        db = libsql.connect(TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN)  # type: ignore
        log_db_init(True)
    except Exception as e:
        log_db_init(False, e)
        db = None
else:
    log_db_init(not_configured=True)
    print("The bot will run without database features (link shortening, user tracking, video-only mode)")




# ==================== USER MANAGEMENT ====================

def track_user(chat_id):
    """Track user interaction (silent - no logging for routine tracking)"""
    if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
        return False
    
    try:
        execute_with_retry(
            """
            INSERT INTO users (chat_id, message_count)
            VALUES (?, 1)
            ON CONFLICT(chat_id) DO UPDATE SET
                last_interaction = CURRENT_TIMESTAMP,
                message_count = message_count + 1
            """,
            (chat_id,),
            needs_commit=True
        )
        return True
    except Exception:
        return False


def get_user_stats(chat_id):
    """Get user statistics"""
    if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
        return None
    try:
        result = execute_with_retry(
            "SELECT first_interaction, message_count FROM users WHERE chat_id = ?",
            (chat_id,)
        )
        if result:
            rows = result.fetchall()
            if rows:
                row = rows[0]
                return {
                    'first_interaction': row[0],
                    'message_count': row[1]
                }
        return None
    except Exception as e:
        print(f"Error getting user stats: {e}")
        return None


# ==================== LINK SHORTENING ====================

def save_shortened_link(user_chat_id, link_id, password=None):
    """Save a shortened link ID with optional password (prevents duplicates)"""
    if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
        return False
    
    try:
        # Check if link already exists for this user
        result = execute_with_retry(
            """
            SELECT id FROM shortened_links 
            WHERE user_chat_id = ? AND link_id = ?
            """,
            (user_chat_id, str(link_id))
        )
        
        if result and len(result.fetchall()) > 0:
            execute_with_retry(
                """
                UPDATE shortened_links 
                SET password = ?
                WHERE user_chat_id = ? AND link_id = ?
                """,
                (password, user_chat_id, str(link_id)),
                needs_commit=True
            )
        else:
            execute_with_retry(
                """
                INSERT INTO shortened_links (user_chat_id, link_id, password)
                VALUES (?, ?, ?)
                """,
                (user_chat_id, str(link_id), password),
                needs_commit=True
            )
        
        log_db_link_saved(link_id, user_chat_id)
        return True
    except Exception as e:
        print(f"❌ DATABASE ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def get_user_link_ids(user_chat_id):
    """Get user's shortened link IDs with passwords"""
    if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
        return {}
    
    log_db_link_query(user_chat_id)
    
    try:
        result = execute_with_retry(
            """
            SELECT link_id, password
            FROM shortened_links
            WHERE user_chat_id = ?
            ORDER BY id DESC
            """,
            (user_chat_id,)
        )
        if result:
            # Return dict mapping link_id to password
            link_data = {row[0]: row[1] for row in result.fetchall()}
            log_db_link_found(len(link_data))
            return link_data
        return {}
    except Exception as e:
        print(f"❌ DATABASE ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {}


def get_all_link_ids():
    """Get all shortened link IDs (admin only)"""
    if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
        return []
    try:
        result = execute_with_retry(
            """
            SELECT link_id, user_chat_id
            FROM shortened_links
            ORDER BY id DESC
            """
        )
        if result:
            links = []
            for row in result.fetchall():
                links.append({
                    'link_id': row[0],
                    'user_chat_id': row[1]
                })
            return links
        return []
    except Exception as e:
        print(f"Error getting all link IDs: {e}")
        return []


# ==================== VIDEO-ONLY MODE ====================

def add_video_only_group(group_id, admin_chat_id):
    """Add a group to video-only mode"""
    if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
        return False
    try:
        execute_with_retry(
            """
            INSERT INTO video_only_groups (group_id, enabled_by_admin)
            VALUES (?, ?)
            ON CONFLICT(group_id) DO UPDATE SET
                enabled_by_admin = excluded.enabled_by_admin
            """,
            (group_id, admin_chat_id),
            needs_commit=True
        )
        return True
    except Exception as e:
        print(f"Error adding video-only group: {e}")
        return False


def remove_video_only_group(group_id):
    """Remove a group from video-only mode"""
    if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
        return False
    try:
        execute_with_retry("DELETE FROM video_only_groups WHERE group_id = ?", (group_id,), needs_commit=True)
        return True
    except Exception as e:
        print(f"Error removing video-only group: {e}")
        return False


def is_video_only_group(group_id):
    """Check if a group is in video-only mode (silent - no logging for routine checks)"""
    if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
        return False
    
    try:
        result = execute_with_retry(
            "SELECT 1 FROM video_only_groups WHERE group_id = ?",
            (group_id,)
        )
        if result:
            is_video_only = len(result.fetchall()) > 0
            return is_video_only
        return False
    except Exception:
        return False


def get_all_video_only_groups():
    """Get all video-only groups"""
    if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
        return []
    try:
        result = execute_with_retry("SELECT group_id, enabled_by_admin FROM video_only_groups")
        if result:
            groups = []
            for row in result.fetchall():
                groups.append({
                    'group_id': row[0],
                    'enabled_by_admin': row[1]
                })
            return groups
        return []
    except Exception as e:
        print(f"Error getting video-only groups: {e}")
        return []
