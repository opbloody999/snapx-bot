# Admin Commands
# Admin-only features: alllinks, videoonly mode

from core.database import get_all_link_ids, add_video_only_group, remove_video_only_group, get_allowed_chats, is_video_only_group
from commands.link_shortener import fetch_all_links_from_api
from config.messages import get_message
from core.api_requests import greenapi_send_message as send_message

# Session management for videoonly command - tracks pending selections
videoonly_sessions = {}  # {chat_id: {'action': 'enable'/'disable', 'groups': [list of groups]}}



def handle_alllinks_command(page=1):
    # List all shortened links (admin only) by fetching from ice.bio API with pagination
    # Args: page (default 1)
    # Returns: formatted message string
    
    # Get all link IDs from database with user info and passwords
    all_db_links = get_all_link_ids()
    
    if not all_db_links:
        return get_message("alllinks_no_links")
    
    # Fetch all links from ice.bio API
    all_api_links = fetch_all_links_from_api()
    
    if all_api_links is None:
        return get_message("alllinks_api_error")
    
    # Create mapping of link_id to user_chat_id and password
    link_id_to_user = {item['link_id']: item['user_chat_id'] for item in all_db_links}
    link_id_to_password = {item['link_id']: item.get('password') for item in all_db_links}
    
    # Filter to only show links in our database (convert API ids to string for comparison)
    db_link_ids = [item['link_id'] for item in all_db_links]
    filtered_links = [link for link in all_api_links if str(link.get('id')) in db_link_ids]
    
    if not filtered_links:
        return get_message("alllinks_no_links")
    
    # Pagination logic
    links_per_page = 5
    total_links = len(filtered_links)
    total_pages = (total_links + links_per_page - 1) // links_per_page
    
    # Validate page number
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
    
    # Calculate slice indices
    start_idx = (page - 1) * links_per_page
    end_idx = min(start_idx + links_per_page, total_links)
    
    # Get links for current page
    page_links = filtered_links[start_idx:end_idx]
    
    # Build message using templates
    message = get_message("alllinks_header", count=total_links)
    
    for i, link in enumerate(page_links, start_idx + 1):
        link_id = str(link.get('id'))
        short_url = link.get('shorturl', 'N/A')
        alias = link.get('alias', '')
        clicks = link.get('clicks', 0)
        date_raw = link.get('date', 'N/A')
        user_chat_id = link_id_to_user.get(link_id, 'Unknown')
        
        # Extract only date (remove time) - format: "2024-11-13 14:30:45" -> "2024-11-13"
        date = date_raw.split(' ')[0] if ' ' in date_raw else date_raw
        
        # Get last 4 digits of user phone
        user_display = user_chat_id.split('@')[0][-4:] if '@' in user_chat_id else 'Unknown'
        
        # Get password from database
        password = link_id_to_password.get(link_id)
        
        # Format password line if password exists
        password_line = f"- 🔒 *Password:* {password}\n" if password else ""
        
        # Use appropriate template based on alias
        if alias:
            message += get_message(
                "alllinks_item_with_alias",
                number=i,
                alias=alias,
                short_url=short_url,
                link_id=link_id,
                date=date,
                password_line=password_line,
                user_display=user_display,
                clicks=clicks
            )
        else:
            message += get_message(
                "alllinks_item_no_alias",
                number=i,
                short_url=short_url,
                link_id=link_id,
                date=date,
                password_line=password_line,
                user_display=user_display,
                clicks=clicks
            )
    
    # Add pagination footer if there are multiple pages
    if total_pages > 1:
        next_page = page + 1 if page < total_pages else 1
        message += get_message(
            "alllinks_pagination",
            current_page=page,
            total_pages=total_pages,
            next_page=next_page
        )
    
    return message


def handle_videoonly_command(chat_id, args):
    # Handle video-only mode command (admin only)
    # Enable or disable silent video downloading for groups
    
    if not args.strip():
        send_message(chat_id, get_message("videoonly_usage"))
        return
    
    parts = args.strip().split()
    action = parts[0].lower() if parts else ''
    
    if action == 'enable' or action == 'on':
        # Get allowed groups from database
        allowed_chats = get_allowed_chats()
        
        # Filter only groups (ending with @g.us)
        all_groups = [chat for chat in allowed_chats if chat['chat_id'].endswith('@g.us')]
        
        if not all_groups:
            send_message(chat_id, get_message("videoonly_no_groups"))
            return
        
        # Filter groups that are NOT already in video-only mode
        groups = [group for group in all_groups if not is_video_only_group(group['chat_id'])]
        
        if not groups:
            send_message(chat_id, get_message("videoonly_all_groups_enabled"))
            return
        
        # Store session for this user
        videoonly_sessions[chat_id] = {
            'action': 'enable',
            'groups': groups
        }
        
        # Build and send group selection message
        message = get_message("videoonly_select_group_enable", count=len(groups))
        
        for idx, group in enumerate(groups, 1):
            group_name = group['name']
            message += get_message("videoonly_group_item", number=idx, name=group_name)
        
        message += get_message("videoonly_select_footer")
        send_message(chat_id, message)
    
    elif action == 'disable' or action == 'off':
        # Get allowed groups from database
        allowed_chats = get_allowed_chats()
        
        # Filter only groups (ending with @g.us)
        all_groups = [chat for chat in allowed_chats if chat['chat_id'].endswith('@g.us')]
        
        if not all_groups:
            send_message(chat_id, get_message("videoonly_no_groups"))
            return
        
        # Filter groups that ARE in video-only mode
        groups = [group for group in all_groups if is_video_only_group(group['chat_id'])]
        
        if not groups:
            send_message(chat_id, get_message("videoonly_no_groups_enabled"))
            return
        
        # Store session for this user
        videoonly_sessions[chat_id] = {
            'action': 'disable',
            'groups': groups
        }
        
        # Build and send group selection message
        message = get_message("videoonly_select_group_disable", count=len(groups))
        
        for idx, group in enumerate(groups, 1):
            group_name = group['name']
            message += get_message("videoonly_group_item", number=idx, name=group_name)
        
        message += get_message("videoonly_select_footer")
        send_message(chat_id, message)
    
    else:
        send_message(chat_id, get_message("videoonly_usage"))


def handle_videoonly_selection(chat_id, selection):
    # Handle numeric selection for videoonly command
    # Returns True if handled, False if not a videoonly session
    
    if chat_id not in videoonly_sessions:
        return False
    
    session = videoonly_sessions[chat_id]
    groups = session['groups']
    action = session['action']
    
    # Validate selection is a number
    try:
        selection_num = int(selection.strip())
    except ValueError:
        send_message(chat_id, get_message("videoonly_invalid_selection"))
        return True
    
    # Validate selection is in range
    if selection_num < 1 or selection_num > len(groups):
        send_message(chat_id, get_message("videoonly_invalid_number", max=len(groups)))
        return True
    
    # Get selected group
    selected_group = groups[selection_num - 1]
    group_id = selected_group['chat_id']
    group_name = selected_group['name']
    
    # Perform action
    if action == 'enable':
        success = add_video_only_group(group_id, chat_id)
        if success:
            send_message(chat_id, get_message("videoonly_enabled", group_name=group_name))
        else:
            send_message(chat_id, get_message("videoonly_enable_failed"))
    else:  # disable
        success = remove_video_only_group(group_id)
        if success:
            send_message(chat_id, get_message("videoonly_disabled", group_name=group_name))
        else:
            send_message(chat_id, get_message("videoonly_disable_failed"))
    
    # Clear session
    del videoonly_sessions[chat_id]
    return True
