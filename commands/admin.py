# Admin Commands
# Admin-only features: alllinks, videoonly mode

from core.database import get_all_link_ids, add_video_only_group, remove_video_only_group
from commands.link_shortener import fetch_all_links_from_api
from config.messages import get_message
from core.api_requests import greenapi_send_message as send_message


def handle_alllinks_command():
    # List all shortened links (admin only) by fetching from ice.bio API
    # Returns: formatted message string
    
    # Get all link IDs from database with user info
    all_db_links = get_all_link_ids()
    
    if not all_db_links:
        return get_message("alllinks_no_links")
    
    # Fetch all links from ice.bio API
    all_api_links = fetch_all_links_from_api()
    
    if all_api_links is None:
        return get_message("alllinks_api_error")
    
    # Create mapping of link_id to user_chat_id
    link_id_to_user = {item['link_id']: item['user_chat_id'] for item in all_db_links}
    
    # Filter to only show links in our database (convert API ids to string for comparison)
    db_link_ids = [item['link_id'] for item in all_db_links]
    filtered_links = [link for link in all_api_links if str(link.get('id')) in db_link_ids]
    
    if not filtered_links:
        return get_message("alllinks_no_links")
    
    # Build message using templates
    message = get_message("alllinks_header", count=len(filtered_links))
    
    for i, link in enumerate(filtered_links, 1):
        link_id = link.get('id')
        short_url = link.get('shorturl', 'N/A')
        long_url = link.get('longurl', 'N/A')
        alias = link.get('alias', '')
        clicks = link.get('clicks', 0)
        user_chat_id = link_id_to_user.get(str(link_id), 'Unknown')
        
        # Get last 4 digits of user phone
        user_display = user_chat_id.split('@')[0][-4:] if '@' in user_chat_id else 'Unknown'
        
        # Truncate long URL if needed
        long_url_display = long_url if len(long_url) <= 40 else long_url[:37] + "..."
        
        # Use appropriate template based on alias
        if alias:
            message += get_message(
                "alllinks_item_with_alias",
                number=i,
                alias=alias,
                short_url=short_url,
                long_url=long_url_display,
                user_display=user_display,
                clicks=clicks
            )
        else:
            message += get_message(
                "alllinks_item_no_alias",
                number=i,
                short_url=short_url,
                long_url=long_url_display,
                user_display=user_display,
                clicks=clicks
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
