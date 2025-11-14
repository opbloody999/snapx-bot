# Admin Commands
# Admin-only features: alllinks, videoonly mode

from core.database import get_all_link_ids, add_video_only_group, remove_video_only_group
from commands.link_shortener import fetch_all_links_from_api
from config.messages import get_message
from core.api_requests import greenapi_send_message as send_message


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
        if len(parts) < 2:
            send_message(chat_id, get_message("videoonly_missing_group_id", action="enable"))
            return
        
        group_id = parts[1]
        if not group_id.endswith('@g.us'):
            group_id = f"{group_id}@g.us"
        
        success = add_video_only_group(group_id, chat_id)
        if success:
            send_message(chat_id, get_message("videoonly_enabled", group_id=group_id))
        else:
            send_message(chat_id, get_message("videoonly_enable_failed"))
    
    elif action == 'disable' or action == 'off':
        if len(parts) < 2:
            send_message(chat_id, get_message("videoonly_missing_group_id", action="disable"))
            return
        
        group_id = parts[1]
        if not group_id.endswith('@g.us'):
            group_id = f"{group_id}@g.us"
        
        success = remove_video_only_group(group_id)
        if success:
            send_message(chat_id, get_message("videoonly_disabled", group_id=group_id))
        else:
            send_message(chat_id, get_message("videoonly_disable_failed"))
    
    else:
        send_message(chat_id, get_message("videoonly_usage"))
