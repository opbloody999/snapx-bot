# Bot Response Messages
# All text responses sent to users
# Edit these to customize bot messages

MESSAGES = {
    # ==================== MAIN & MENU MESSAGES ====================
    
    # Main menu showing all available bot commands and features
    "menu": (
        """👾 *SnapX Bot Commands* ⚡

_Your fast & intelligent WhatsApp assistant_

*🎬 Video Downloader*

_Just send any video URL and I'll download it automatically!_

*🤖 AI Assistant*

- *_.gpt on_* / *_.gpt off_*
_Enable or disable ChatGPT-style conversations._

*🔗 Link Shortener*

- *_.short <url>_*
_Shortens any link with tracking support._

- *_.mylinks_*
_View your shortened links and click stats._

- *_.stats <link_id>_*
_View detailed analytics for a specific link._

*📱 WhatsApp Tools*

- *_.checkwa <number>_*
_Check if a number is active on WhatsApp._

- *_.avatar <number>_*
_Get someone's profile picture._

- *_.userinfo <number>_*
_View contact details and metadata._

💡 Use commands without parameters to get usage examples and more options!"""
    ),
    
    # Welcome message introducing the bot and its features
    "greeting": (
        """👾 *Welcome to SnapX Bot!*  
Your smart WhatsApp assistant ⚡  

💡 *What SnapX can do:*  

*1. 🎬 Video Downloader*  
_Instantly grab videos from TikTok, YouTube, Instagram & more._

*2. 🧠 AI Chat Assistant*  
_Chat with advanced AI powered by ChatGPT-style intelligence._  

*3. 🔗 Link Shortener*  
_Create, track, and analyze your links with custom aliases and detailed statistics._  

*4. ⚙️ WhatsApp Tools*  
_Check numbers, get avatars, and view user information._  

_Type *.menu* to see how to use these features!_"""
    ),
    
    # Message shown when user sends an unrecognized command
    "unknown_command": (
        "*❓ Unknown Command*\n\n"
        "_I didn't understand that_\n\n"
        "_Type_ *_.menu_* _to see what I can do_"
    ),
    
    
    # ==================== CHATGPT MESSAGES ====================
    
    # Confirmation message when ChatGPT mode is enabled
    "gpt_activated": (
        "*🤖 ChatGPT Activated*\n\n"
        "_I'm now in AI mode - all your messages come to me!_\n\n"
        "_💡 Auto-deactivates after 5 minutes of inactivity_"
    ),
    
    # Instructions for using ChatGPT on/off commands
    "gpt_usage": (
        "*🤖 ChatGPT Control*\n\n"
        "- *_.gpt on_*\n"
        "_(Activate AI mode)_\n\n"
        "- *_.gpt off_*\n"
        "_(Deactivate AI mode)_"
    ),
    
    # Confirmation message when ChatGPT mode is manually disabled
    "gpt_deactivated": (
        "*✅ ChatGPT Deactivated*\n\n"
        "_Back to normal mode_"
    ),
    
    # Simple deactivation message without extra formatting
    "gpt_deactivated_simple": (
        "✅ ChatGPT deactivated"
    ),
    
    # Message shown when ChatGPT auto-disables due to inactivity
    "gpt_auto_timeout": (
        "*⏰ Auto-Deactivated*\n\n"
        "_ChatGPT turned off after *{minutes} minutes* of inactivity_\n\n"
        "_Type_ *_.gpt on_* _to reactivate_"
    ),
    
    # Error message when ChatGPT cannot understand the input
    "gpt_no_response": (
        "Sorry, I couldn't understand that. Try again."
    ),
    
    # Error message when ChatGPT request times out
    "gpt_timeout": (
        "⏱️ Request timed out. Try again."
    ),
    
    # Error message when unable to connect to ChatGPT service
    "gpt_connection_error": (
        "❌ Error connecting to ChatGPT. Try again later."
    ),
    
    # Generic error message for ChatGPT processing failures
    "gpt_processing_error": (
        "❌ Error processing your message. Try again."
    ),
    
    # Generic error message for ChatGPT failures
    "chatgpt_error": (
        "*❌ ChatGPT Error*\n\n"
        "_I couldn't process that message_\n\n"
        "_Please try again_"
    ),
    
    
    # ==================== VIDEO DOWNLOADER MESSAGES ====================
    
    # Error message for malformed or invalid URLs
    "invalid_url": (
        "*❌ Invalid URL*\n\n"
        "_Please send a valid link starting with http:// or https://_"
    ),
    
    # Status message while downloading a video
    "downloading_video": (
        "*📥 Downloading Video...*\n\n"
        "✨ _Fetching your video, please wait..._"
    ),
    
    # Error message when video download fails
    "video_download_failed": (
        "*❌ Download Failed*\n\n"
        "*Possible reasons:*\n"
        "- URL is incorrect\n"
        "- Video is private\n"
        "- Platform temporarily unavailable\n\n"
        "_Please try again or use a different link_"
    ),
    
    # Usage instructions for video download command
    "download_usage": (
        "📥 *Video Downloader*\n\n"
        "*Usage:*\n"
        "_.download <url>_\n"
        "_.dl <url>_\n\n"
        "*Or just send any video URL!*\n\n"
        "*Examples:*\n"
        "_.dl https://tiktok.com/..._\n"
        "_https://instagram.com/reel/..._\n\n"
        "*Supported:*\n"
        "TikTok, Instagram, YouTube, Facebook, Twitter & more"
    ),
    
    # Fallback message with download link when auto-send fails
    "video_sent_fallback": (
        "*✅ Video Ready*\n\n"
        "*Download link:*\n"
        "{video_url}\n\n"
        "_Auto-send failed, but you can download from the link above_"
    ),
    
    # List of platforms supported for video downloads
    "supported_platforms": (
        "*Supported Platforms*\n"
        "TikTok, Instagram, YouTube, Facebook, Twitter and more"
    ),
    
    
    # ==================== LINK SHORTENER MESSAGES ====================
    
    # Usage instructions for link shortener command
    "shortener_usage": (
        """🔗 *Link Shortener*

- *_.short <url>_*
_Shortens any link._

- *_.short <url> <custom_alias>_*
_Shortens with a custom alias._

- *_.short <url> <custom_alias> <password>_*
_Shortens with custom alias & password._

🚀 _Easily create, customize, and manage your links — all with SnapX!_"""
    ),
    
    # Error message for invalid URL in link shortener
    "shortener_invalid_url": (
        "❌ *Invalid URL*\n\n"
        "Please provide a valid URL starting with http:// or https://"
    ),
    
    # Success message after successfully shortening a link
    "shortener_success": (
        "✅ *Link Shortened Successfully!*\n\n"
        "🔗 *Short URL:* {short_url}\n"
        "{alias_info}"
        "{password_info}"
        "🆔 *Link ID:* {link_id}\n\n"
        "_Use_ *_.stats {link_id}_* _to view detailed statistics_"
    ),
    
    # Template for alias info line when custom alias is provided
    "shortener_alias_line": (
        "🏷️ *Alias:* {alias}\n"
    ),
    
    # Template for password info line when password is provided
    "shortener_password_line": (
        "🔒 *Password:* {password}\n"
    ),
    
    # Error message when link shortening API fails
    "shortener_api_error": (
        "❌ *Link Shortening Failed*\n\n"
        "{error_message}\n\n"
        "_Please try again or contact support if the issue persists_"
    ),
    
    # Error message when shortening request times out
    "shortener_timeout": (
        "❌ *Request Timeout*\n\n"
        "The shortening service took too long to respond.\n\n"
        "_Please try again in a moment_"
    ),
    
    # Error message when unable to connect to shortening service
    "shortener_connection_error": (
        "❌ *Connection Error*\n\n"
        "Could not connect to the link shortening service.\n\n"
        "_Please check your internet connection and try again_"
    ),
    
    # Generic error message for unexpected shortening failures
    "shortener_unexpected_error": (
        "❌ *Unexpected Error*\n\n"
        "An unexpected error occurred while shortening your link.\n\n"
        "_Please try again_"
    ),
    
    # Header for user's link list showing total count
    "mylinks_header": (
        "🔗 *Your Shortened Links* ({count})\n\n"
    ),
    
    # Template for displaying a link with custom alias
    "mylinks_item_with_alias": (
        "*{number}.* 🏷️ *{alias}*\n\n"
        "- 🔗 *Short URL:* {short_url}\n"
        "- 🆔 *Link ID:* {link_id}\n"
        "- 📅 *Date:* {date}\n"
        "{password_line}"
        "- 👆 *Clicks:* {clicks}\n\n"
    ),
    
    # Template for displaying a link without custom alias
    "mylinks_item_no_alias": (
        "*{number}.*\n\n"
        "- 🔗 *Short URL:* {short_url}\n"
        "- 🆔 *Link ID:* {link_id}\n"
        "- 📅 *Date:* {date}\n"
        "{password_line}"
        "- 👆 *Clicks:* {clicks}\n\n"
    ),
    
    # Message shown when user has no shortened links
    "mylinks_no_links": (
        "📭 *No Links Found*\n\n"
        "You haven't shortened any links yet.\n\n"
        "_Use_ *_.short <url>_* _to create your first short link!_"
    ),
    
    # Error message when unable to fetch user's links
    "mylinks_api_error": (
        "❌ *Unable to Fetch Links*\n\n"
        "Could not retrieve your links at the moment.\n\n"
        "_Please try again later_"
    ),
    
    # Header for all links (admin view) showing total count
    "alllinks_header": (
        "🔗 *All Shortened Links* ({count})\n\n"
    ),
    
    # Template for displaying any user's link with alias (admin view)
    "alllinks_item_with_alias": (
        "*{number}.* 🏷️ *{alias}*\n\n"
        "- 🔗 *Short URL:* {short_url}\n"
        "- 🆔 *Link ID:* {link_id}\n"
        "- 📅 *Date:* {date}\n"
        "{password_line}"
        "- 👤 *User:* ...{user_display}\n"
        "- 👆 *Clicks:* {clicks}\n\n"
    ),
    
    # Template for displaying any user's link without alias (admin view)
    "alllinks_item_no_alias": (
        "*{number}.*\n\n"
        "- 🔗 *Short URL:* {short_url}\n"
        "- 🆔 *Link ID:* {link_id}\n"
        "- 📅 *Date:* {date}\n"
        "{password_line}"
        "- 👤 *User:* ...{user_display}\n"
        "- 👆 *Clicks:* {clicks}\n\n"
    ),
    
    # Message shown when no links exist in system (admin view)
    "alllinks_no_links": (
        "📭 *No Links Found*\n\n"
        "No users have created any links yet."
    ),
    
    # Error message when unable to fetch all links (admin view)
    "alllinks_api_error": (
        "❌ *Unable to Fetch Links*\n\n"
        "Could not retrieve links at the moment.\n\n"
        "_Please try again later_"
    ),
    
    # Pagination footer for mylinks command
    "mylinks_pagination": (
        "📂 *Page {current_page} of {total_pages}*\n\n"
        "_Type_ *_.mylinks {next_page}_* _to view the next page_"
    ),
    
    # Pagination footer for alllinks command  
    "alllinks_pagination": (
        "📂 *Page {current_page} of {total_pages}*\n\n"
        "_Type_ *_.alllinks {next_page}_* _to view the next page_"
    ),
    
    
    # ==================== LINK STATS MESSAGES ====================
    
    # Usage instructions for link stats command
    "stats_usage": (
        "📊 *Link Statistics*\n\n"
        "*Usage:*\n"
        "_.stats <link_id>_\n\n"
        "*Example:*\n"
        "_.stats 27891_\n\n"
        "_Get detailed statistics for your shortened link including clicks, countries, browsers, and operating systems_\n\n"
        "💡 _You can find your link ID using_ *_.mylinks_*"
    ),
    
    # Error message when link ID is missing
    "stats_missing_id": (
        "❌ *Missing Link ID*\n\n"
        "Please provide a link ID.\n\n"
        "*Usage:* _.stats <link_id>_\n\n"
        "*Example:* _.stats 27891_"
    ),
    
    # Error message when link ID is invalid
    "stats_invalid_id": (
        "❌ *Invalid Link ID*\n\n"
        "Please provide a valid numeric link ID.\n\n"
        "*Usage:* _.stats <link_id>_\n\n"
        "*Example:* _.stats 27891_"
    ),
    
    # Error message when link is not found
    "stats_not_found": (
        "❌ *Link Not Found*\n\n"
        "Could not find a link with ID: {link_id}\n\n"
        "_Make sure you're using the correct link ID from your links list_"
    ),
    
    # Error message when stats API fails
    "stats_api_error": (
        "❌ *Unable to Fetch Statistics*\n\n"
        "{error_message}\n\n"
        "_Please try again later_"
    ),
    
    # Error message when stats request times out
    "stats_timeout": (
        "❌ *Request Timeout*\n\n"
        "The statistics service took too long to respond.\n\n"
        "_Please try again in a moment_"
    ),
    
    # Error message when unable to connect to stats service
    "stats_connection_error": (
        "❌ *Connection Error*\n\n"
        "Could not connect to the statistics service.\n\n"
        "_Please check your internet connection and try again_"
    ),
    
    # Generic error message for unexpected stats failures
    "stats_unexpected_error": (
        "❌ *Unexpected Error*\n\n"
        "An unexpected error occurred while fetching statistics.\n\n"
        "_Please try again_"
    ),
    
    # Stats display header with link details
    "stats_header": (
        "📊 *Link Statistics*\n\n"
        "🆔 *Link ID:* {link_id}\n"
        "🔗 *Short URL:* {short_url}\n\n"
    ),
    
    # Stats click statistics section
    "stats_clicks": (
        "📈 *Click Statistics*\n"
        "- Total Clicks: {clicks}\n"
        "- Unique Clicks: {unique_clicks}\n\n"
    ),
    
    # Stats countries section header
    "stats_countries_header": (
        "🌍 *Top Countries*\n"
    ),
    
    # Stats browsers section header
    "stats_browsers_header": (
        "🌐 *Top Browsers*\n"
    ),
    
    # Stats OS section header
    "stats_os_header": (
        "💻 *Top Operating Systems*\n"
    ),
    
    # Stats footer with available stats
    "stats_footer_with_stats": (
        "_These are the available statistics: Clicks, {stats_list}_"
    ),
    
    # Stats footer when only clicks available
    "stats_footer_clicks_only": (
        "_Only click statistics are currently available for this link_"
    ),
    
    
    # ==================== ADMIN MESSAGES ====================
    
    # Developer menu showing admin-only commands
    "dev_menu": (
        "🔐 *Developer Menu* 👨‍💻\n\n"
        "*Admin-Only Commands*\n\n"
        "- *_.alllinks_*\n"
        "_(View all shortened links)_\n\n"
        "- *_.videoonly enable_*\n"
        "_(Enable silent video-only mode for a group)_\n\n"
        "- *_.videoonly disable_*\n"
        "_(Disable video-only mode)_\n\n"
        "⚠️ _Admin commands only accessible by developer_"
    ),
    
    # Error message when non-admin tries to use admin commands
    "admin_only": (
        "🔐 *Admin Only*\n\n"
        "❌ You don't have permission to use this command.\n\n"
        "_This command is restricted to the bot administrator._"
    ),
    
    # Usage instructions for video-only mode command
    "videoonly_usage": (
        "📹 *Video-Only Mode*\n\n"
        "*Usage:*\n"
        "_.videoonly enable_\n"
        "_.videoonly disable_\n\n"
        "_Enable this mode to make the bot silently download videos in a group without any messages or commands_"
    ),
    
    # Message when no groups available for video-only mode
    "videoonly_no_groups": (
        "📹 *No Groups Available*\n\n"
        "❌ No groups found in your allowed list.\n\n"
        "_Video-only mode can only be enabled for groups._"
    ),
    
    # Message when all groups are already in video-only mode
    "videoonly_all_groups_enabled": (
        "📹 *All Groups Already in Video-Only Mode*\n\n"
        "✅ All your groups are already in video-only mode.\n\n"
        "_Use_ *_.videoonly disable_* _to disable video-only mode for a group._"
    ),
    
    # Message when no groups are in video-only mode
    "videoonly_no_groups_enabled": (
        "📹 *No Groups in Video-Only Mode*\n\n"
        "❌ None of your groups have video-only mode enabled.\n\n"
        "_Use_ *_.videoonly enable_* _to enable video-only mode for a group._"
    ),
    
    # Group selection header for enable action
    "videoonly_select_group_enable": (
        "📹 *Enable Video-Only Mode*\n\n"
        "✨ Select a group to enable silent video downloading:\n\n"
        "📂 *Available Groups* ({count}):\n\n"
    ),
    
    # Group selection header for disable action
    "videoonly_select_group_disable": (
        "📹 *Disable Video-Only Mode*\n\n"
        "🔓 Select a group to disable video-only mode:\n\n"
        "📂 *Available Groups* ({count}):\n\n"
    ),
    
    # Individual group item in selection list
    "videoonly_group_item": (
        "*{number}.* 📱 {name}\n"
    ),
    
    # Footer for group selection message
    "videoonly_select_footer": (
        "\n💬 *Reply with the group number* (e.g., 1, 2, 3)"
    ),
    
    # Error message for invalid selection (not a number)
    "videoonly_invalid_selection": (
        "❌ *Invalid Selection*\n\n"
        "Please reply with a valid number.\n\n"
        "_Example: 1_"
    ),
    
    # Error message for number out of range
    "videoonly_invalid_number": (
        "❌ *Invalid Number*\n\n"
        "Please select a number between 1 and {max}."
    ),
    
    # Confirmation message when video-only mode is enabled
    "videoonly_enabled": (
        "✅ *Video-Only Mode Enabled*\n\n"
        "📹 *Group:* {group_name}\n\n"
        "🎬 Bot will now only download videos silently in this group.\n\n"
        "_No other commands or messages will be processed._"
    ),
    
    # Confirmation message when video-only mode is disabled
    "videoonly_disabled": (
        "✅ *Video-Only Mode Disabled*\n\n"
        "📹 *Group:* {group_name}\n\n"
        "🔓 Bot will now respond normally to all commands in this group."
    ),
    
    # Error message when enabling video-only mode fails
    "videoonly_enable_failed": (
        "❌ *Failed to Enable Video-Only Mode*\n\n"
        "An error occurred. Please try again."
    ),
    
    # Error message when disabling video-only mode fails
    "videoonly_disable_failed": (
        "❌ *Failed to Disable Video-Only Mode*\n\n"
        "An error occurred. Please try again."
    ),
    
    
    # ==================== WHATSAPP TOOLS MESSAGES ====================
    
    # Usage instructions for checking WhatsApp status
    "checkwa_usage": (
        "📱 *Check WhatsApp Status*\n\n"
        "*Usage:*\n"
        "_.checkwhatsapp <number>_\n"
        "_.checkwa <number>_\n\n"
        "*Examples:*\n"
        "_.checkwa 923001234567_\n\n"
        "_Check if a number has WhatsApp_"
    ),
    
    # Error message for invalid phone number format
    "checkwa_invalid_number": (
        "❌ *Invalid Phone Number*\n\n"
        "Please provide a valid phone number.\n\n"
        "*Usage:* .checkwhatsapp 923453870090"
    ),
    
    # Error message when phone number is too short
    "checkwa_number_too_short": (
        "❌ *Invalid Phone Number*\n\n"
        "Phone number too short. Please use country code.\n\n"
        "*Example:* .checkwa 923001234567"
    ),
    
    # Error message for Pakistani numbers without country code
    "checkwa_needs_country_code": (
        "❌ *Invalid Phone Number*\n\n"
        "📱 Number: {number}\n\n"
        "✗ Numbers starting with 0 must be 11 digits\n\n"
        "💡 _Please include the country code_\n\n"
        "*Example:* .checkwa 923001234567"
    ),
    
    # Generic error message for WhatsApp check failures
    "checkwa_error": (
        "❌ *Error*\n\n"
        "Failed to check WhatsApp status. Please try again."
    ),
    
    # Error message for Pakistani number check failures
    "checkwa_error_pakistani": (
        "❌ *Error*\n\n"
        "Failed to get contact info. This number might not be registered on WhatsApp.\n\n"
        "💡 _If this is not a Pakistani number, please include the country code_\n\n"
        "*Example:* .checkwhatsapp 923001234567"
    ),
    
    # Success message when number has WhatsApp account
    "checkwa_found": (
        "✅ *WhatsApp Account Found*\n\n"
        "📱 Number: {number}\n\n"
        "✓ This number has an active WhatsApp account"
    ),
    
    # Message when number doesn't have WhatsApp
    "checkwa_not_found": (
        "❌ *No WhatsApp Account*\n\n"
        "📱 Number: {number}\n\n"
        "✗ This number does not have WhatsApp"
    ),
    
    # Message for Pakistani numbers without WhatsApp with suggestion
    "checkwa_not_found_pakistani": (
        "❌ *No WhatsApp Account*\n\n"
        "📱 Number: {number}\n\n"
        "✗ This number does not have WhatsApp\n\n"
        "💡 _If this was a Pakistani number, try with country code: .checkwa 92{suggestion}_"
    ),
    
    # Usage instructions for getting user avatar
    "avatar_usage": (
        "👤 *Get Avatar*\n\n"
        "*Usage:*\n"
        "_.getavatar <number>_\n"
        "_.avatar <number>_\n\n"
        "*Examples:*\n"
        "_.avatar 923001234567_\n\n"
        "_Get user's profile picture_"
    ),
    
    # Error message when avatar retrieval fails
    "avatar_error": (
        "❌ *Error*\n\n"
        "Failed to get avatar. Please check the number and try again."
    ),
    
    # Success message when avatar is found and being sent
    "avatar_found": (
        "✅ *Avatar Found*\n\n"
        "👤 Sending profile picture..."
    ),
    
    # Success message with avatar URL
    "avatar_found_url": (
        "✅ *Avatar Found*\n\n"
        "👤 Chat ID: {chat_id}\n\n"
        "🔗 {avatar_url}"
    ),
    
    # Message when user/group has no profile picture
    "avatar_no_avatar": (
        "❌ *No Avatar*\n\n"
        "👤 Chat ID: {chat_id}\n\n"
        "This user/group does not have a profile picture."
    ),
    
    # Usage instructions for getting contact information
    "contactinfo_usage": (
        "📋 *Get Contact Info*\n\n"
        "*Usage:*\n"
        "_.userinfo <number>_\n"
        "_.contactinfo <number>_\n\n"
        "*Examples:*\n"
        "_.userinfo 923001234567_\n\n"
        "_Get detailed contact information_"
    ),
    
    # Error message when contact info retrieval fails
    "contactinfo_error": (
        "❌ *Error*\n\n"
        "Failed to get contact info. This number might not be registered on WhatsApp.\n\n"
        "💡 _Try using:_ .checkwhatsapp <number>"
    ),
    
    # Header for contact information display
    "contactinfo_header": (
        "👤 *Contact Information*\n\n"
    ),
    
    # WhatsApp link in contact info
    "contactinfo_whatsapp": (
        "📱 WhatsApp: {wa_me_link}\n"
    ),
    
    # Name field in contact info
    "contactinfo_name": (
        "👤 Name: {name}\n"
    ),
    
    # Avatar status when user has profile picture
    "contactinfo_has_avatar": (
        "🖼️ Has Avatar: Yes\n"
    ),
    
    # Avatar status when user has no profile picture
    "contactinfo_no_avatar": (
        "🖼️ Has Avatar: No\n"
    ),
}


def get_message(key, **kwargs):
    # Get a message template and format it with provided arguments
    message = MESSAGES.get(key, "")
    return message.format(**kwargs)
