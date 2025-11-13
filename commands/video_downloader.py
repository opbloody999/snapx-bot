# Video Downloader
# Downloads videos from social media platforms using BatGPT API
# Supported: TikTok, Instagram, YouTube, Facebook, Twitter and more

import re
from config.messages import get_message
from core.api_requests import video_download_request
from core.logger import log_api_error, log_video_operation

# ==================== VIDEO DOWNLOAD ====================

def download_video(url):
    # Download video from social media URL
    # Returns: dict with 'success', 'media_url', 'title' or None on error
    
    log_video_operation('downloading')
    
    # Call API via centralized handler
    result = video_download_request(url)
    
    if not result.get('success'):
        # Handle different error types
        error_type = result.get('error_type')
        
        if error_type == 'timeout':
            log_api_error('Video Downloader', 'timeout', 'Request timed out after 60 seconds')
        elif error_type == 'http_error':
            log_api_error('Video Downloader', 'http_error', 
                         f"Status: {result.get('status_code')}, Response: {result.get('response_text')}")
        elif error_type == 'api_failed':
            log_api_error('Video Downloader', 'api_failed', f"Raw data: {result.get('raw_data')}")
        elif error_type == 'no_video_url':
            log_api_error('Video Downloader', 'no_video_url', f"Media info: {result.get('media_info')}")
        elif error_type == 'connection_error':
            log_api_error('Video Downloader', 'connection_error', result.get('error'))
        elif error_type == 'json_parse_error':
            log_api_error('Video Downloader', 'json_parse_error', result.get('error'))
        else:
            log_api_error('Video Downloader', 'processing_error', result.get('error'))
        
        log_video_operation('failed')
        return None
    
    log_video_operation('sent', title=result.get('title'))
    return result


# ==================== HELPER FUNCTIONS ====================

def get_supported_platforms():
    # Returns formatted text of supported platforms
    return get_message("supported_platforms")


def extract_url(text):
    # Extract URL from message text
    # Handles URLs even when WhatsApp includes embeds/thumbnails
    url_pattern = r'https?://[^\s\n]+'
    urls = re.findall(url_pattern, text)
    return urls[0] if urls else None
