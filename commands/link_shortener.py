# Link Shortener using ice.bio API
# Features: Shorten links with custom alias and password, view user links with stats

import time
from core.database import save_shortened_link, get_user_link_ids
from config.messages import get_message
from core.api_requests import link_shorten_request, link_list_request, link_stats_request
from core.logger import log_api_error, log_link_operation, log_db_operation

# ==================== LINK SHORTENING ====================

def shorten_link(user_id, url, custom_alias=None, password=None):
    # Shorten a URL using ice.bio API
    # Args: user_id, url, custom_alias (optional), password (optional)
    # Returns: dict with 'success', 'message', 'short_url', 'link_id'
    
    # Performance timing
    start_time = time.perf_counter()
    
    if not url.startswith(('http://', 'https://')):
        return {
            'success': False,
            'message': get_message("shortener_invalid_url")
        }
    
    # Call API via centralized handler
    api_start = time.perf_counter()
    result = link_shorten_request(url, custom_alias, password)
    api_duration = (time.perf_counter() - api_start) * 1000
    print(f"⏱️  Link Shortener API call took {api_duration:.2f}ms")
    
    if not result.get('success'):
        # Handle different error types
        error_type = result.get('error_type')
        
        if error_type == 'timeout':
            log_api_error('Link Shortener', 'timeout', 'Request timed out after 30 seconds')
            return {
                'success': False,
                'message': get_message("shortener_timeout")
            }
        elif error_type == 'http_error':
            log_api_error('Link Shortener', 'http_error', f"Status: {result.get('status_code')}")
            return {
                'success': False,
                'message': get_message("shortener_api_error", error_message=f"HTTP {result.get('status_code')}")
            }
        elif error_type == 'incomplete_response':
            log_api_error('Link Shortener', 'incomplete_response', f"Raw data: {result.get('raw_data')}")
            return {
                'success': False,
                'message': get_message("shortener_api_error", error_message="Incomplete response from API")
            }
        elif error_type == 'api_error':
            log_api_error('Link Shortener', 'api_error', 
                         f"Code: {result.get('error_code')}, Message: {result.get('error_message')}")
            return {
                'success': False,
                'message': get_message("shortener_api_error", error_message=result.get('error_message'))
            }
        elif error_type == 'connection_error':
            log_api_error('Link Shortener', 'connection_error', result.get('error'))
            return {
                'success': False,
                'message': get_message("shortener_connection_error")
            }
        else:
            log_api_error('Link Shortener', 'unexpected_error', result.get('error'))
            return {
                'success': False,
                'message': get_message("shortener_unexpected_error")
            }
    
    # Extract success data
    link_id = result.get('link_id')
    short_url = result.get('short_url')
    
    # Save link ID and password to database
    db_start = time.perf_counter()
    log_db_operation('link_saved', link_id=link_id, user=user_id)
    save_shortened_link(user_id, link_id, password)
    db_duration = (time.perf_counter() - db_start) * 1000
    print(f"⏱️  Database save took {db_duration:.2f}ms")
    
    log_link_operation('shortened', short_url=short_url, link_id=link_id)
    
    # Build success message with templates from messages.py
    msg_start = time.perf_counter()
    alias_info = get_message("shortener_alias_line", alias=custom_alias) if custom_alias else ""
    password_info = get_message("shortener_password_line", password=password) if password else ""
    
    message = get_message(
        "shortener_success",
        short_url=short_url,
        alias_info=alias_info,
        password_info=password_info,
        link_id=link_id
    )
    msg_duration = (time.perf_counter() - msg_start) * 1000
    print(f"⏱️  Message formatting took {msg_duration:.2f}ms")
    
    total_duration = (time.perf_counter() - start_time) * 1000
    print(f"⏱️  TOTAL link shortening took {total_duration:.2f}ms")
    
    return {
        'success': True,
        'message': message,
        'short_url': short_url,
        'link_id': link_id
    }


# ==================== LINK LISTING ====================

def fetch_all_links_from_api():
    # Fetch links from ice.bio API
    # Returns: list of link objects or None on error
    # Note: Reduced limit from 1000 to 200 for better performance
    # Most users won't have more than 200 links, and this significantly speeds up the request
    
    log_link_operation('fetching')
    
    # Call API via centralized handler (reduced from 1000 to 200 for performance)
    result = link_list_request(limit=200, page=1)
    
    if not result.get('success'):
        # Handle error
        error_type = result.get('error_type')
        
        if error_type == 'http_error':
            log_api_error('Link List', 'http_error', f"Status: {result.get('status_code')}")
        elif error_type == 'api_error':
            log_api_error('Link List', 'api_error', result.get('error_message'))
        else:
            log_api_error('Link List', 'unexpected_error', result.get('error'))
        
        return None
    
    return result.get('links', [])


def list_user_recent_links(user_id, page=1):
    # List user's recent shortened links by fetching from ice.bio API with pagination
    # Args: user_id, page (default 1)
    # Returns: formatted message string
    
    # Get user's link IDs with passwords from database
    log_db_operation('link_query', chat_id=user_id)
    user_link_data = get_user_link_ids(user_id)
    
    if not user_link_data:
        return get_message("mylinks_no_links")
    
    # Fetch all links from ice.bio API
    all_links = fetch_all_links_from_api()
    
    if all_links is None:
        return get_message("mylinks_api_error")
    
    # Filter to only show user's links (convert API ids to string for comparison)
    user_links = [link for link in all_links if str(link.get('id')) in user_link_data.keys()]
    
    if not user_links:
        return get_message("mylinks_no_links")
    
    # Pagination logic
    links_per_page = 5
    total_links = len(user_links)
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
    page_links = user_links[start_idx:end_idx]
    
    # Build message using templates
    message = get_message("mylinks_header", count=total_links)
    
    for i, link in enumerate(page_links, start_idx + 1):
        short_url = link.get('shorturl', 'N/A')
        alias = link.get('alias', '')
        clicks = link.get('clicks', 0)
        link_id = str(link.get('id'))
        date_raw = link.get('date', 'N/A')
        
        # Extract only date (remove time) - format: "2024-11-13 14:30:45" -> "2024-11-13"
        date = date_raw.split(' ')[0] if ' ' in date_raw else date_raw
        
        # Get password from database
        password = user_link_data.get(link_id)
        
        # Format password line if password exists (using template from messages.py)
        password_line = f"- {get_message('shortener_password_line', password=password)}" if password else ""
        
        # Use appropriate template based on alias
        if alias:
            message += get_message(
                "mylinks_item_with_alias",
                number=i,
                alias=alias,
                short_url=short_url,
                link_id=link_id,
                date=date,
                clicks=clicks,
                password_line=password_line
            )
        else:
            message += get_message(
                "mylinks_item_no_alias",
                number=i,
                short_url=short_url,
                link_id=link_id,
                date=date,
                clicks=clicks,
                password_line=password_line
            )
    
    # Add pagination footer if there are multiple pages
    if total_pages > 1:
        next_page = page + 1 if page < total_pages else 1
        message += get_message(
            "mylinks_pagination",
            current_page=page,
            total_pages=total_pages,
            next_page=next_page
        )
    
    return message


# ==================== COMMAND HANDLERS ====================

def handle_shortener_command(user_id, args):
    # Handle link shortening command
    
    if not args or args.strip() == '':
        return {
            'type': 'usage',
            'message': get_message("shortener_usage")
        }
    
    # Parse arguments: url [custom_alias] [password]
    parts = args.strip().split()
    
    url = parts[0] if len(parts) > 0 else None
    custom_alias = parts[1] if len(parts) > 1 else None
    password = parts[2] if len(parts) > 2 else None
    
    if not url:
        return {
            'type': 'usage',
            'message': get_message("shortener_usage")
        }
    
    # Shorten the link
    result = shorten_link(user_id, url, custom_alias, password)
    
    # Check if result is valid (fix NoneType error)
    if not result or not isinstance(result, dict):
        return {
            'type': 'error',
            'message': get_message("shortener_unexpected_error"),
            'success': False
        }
    
    return {
        'type': 'result',
        'message': result.get('message', 'Unknown error'),
        'success': result.get('success', False)
    }


def handle_mylinks_command(user_id, args=None):
    # Handle my links command with optional page number
    # Args: user_id, args (optional page number)
    
    page = 1
    if args and args.strip():
        try:
            page = int(args.strip().split()[0])
        except (ValueError, IndexError):
            page = 1
    
    return list_user_recent_links(user_id, page)


# ==================== LINK STATS ====================

def get_link_stats(link_id):
    # Get detailed statistics for a shortened link
    # Args: link_id (str or int)
    # Returns: formatted message string
    
    # Fetch stats from API
    result = link_stats_request(link_id)
    
    if not result.get('success'):
        # Handle different error types
        error_type = result.get('error_type')
        
        if error_type == 'timeout':
            return get_message("stats_timeout")
        elif error_type == 'http_error':
            return get_message("stats_api_error", error_message=f"HTTP {result.get('status_code')}")
        elif error_type == 'api_error':
            error_msg = result.get('error_message', 'Unknown error')
            if 'not found' in error_msg.lower():
                return get_message("stats_not_found", link_id=link_id)
            return get_message("stats_api_error", error_message=error_msg)
        elif error_type == 'connection_error':
            return get_message("stats_connection_error")
        else:
            return get_message("stats_unexpected_error")
    
    # Extract stats data
    details = result.get('details', {})
    stats_data = result.get('data', {})
    
    link_id = details.get('id', 'N/A')
    short_url = details.get('shorturl', 'N/A')
    clicks = stats_data.get('clicks', 0)
    unique_clicks = stats_data.get('uniqueClicks', 0)
    top_countries = stats_data.get('topCountries', {})
    top_browsers = stats_data.get('topBrowsers', {})
    top_os = stats_data.get('topOs', {})
    
    # Build stats message using templates from messages.py
    message = get_message("stats_header", link_id=link_id, short_url=short_url)
    message += get_message("stats_clicks", clicks=clicks, unique_clicks=unique_clicks)
    
    # Track which stats are available
    available_stats = []
    
    # Top Countries
    if top_countries and any(top_countries.values()):
        message += get_message("stats_countries_header")
        for country, count in list(top_countries.items())[:5]:
            message += f"- {country}: {count}\n"
        message += "\n"
        available_stats.append("Countries")
    
    # Top Browsers
    if top_browsers and any(top_browsers.values()):
        message += get_message("stats_browsers_header")
        for browser, count in list(top_browsers.items())[:5]:
            message += f"- {browser}: {count}\n"
        message += "\n"
        available_stats.append("Browsers")
    
    # Top Operating Systems
    if top_os and any(top_os.values()):
        message += get_message("stats_os_header")
        for os, count in list(top_os.items())[:5]:
            message += f"- {os}: {count}\n"
        message += "\n"
        available_stats.append("Operating Systems")
    
    # Add footer message using templates
    if available_stats:
        stats_list = ", ".join(available_stats)
        message += get_message("stats_footer_with_stats", stats_list=stats_list)
    else:
        message += get_message("stats_footer_clicks_only")
    
    return message


def handle_stats_command(user_chat_id, args):
    # Handle link stats command
    # Args: user_chat_id, args (for consistency with other commands)
    
    if not args or (isinstance(args, str) and args.strip() == ''):
        return get_message("stats_usage")
    
    # Handle both string and list args
    if isinstance(args, list):
        if not args:
            return get_message("stats_usage")
        link_id = str(args[0])
    else:
        link_id = args.strip().split()[0]
    
    # Validate link ID is numeric
    if not link_id.isdigit():
        return get_message("stats_invalid_id")
    
    # Get and return stats
    return get_link_stats(link_id)
