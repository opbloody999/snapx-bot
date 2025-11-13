# External API Requests Handler
# Centralizes all external API calls (ChatGPT, Video Downloader, Link Shortener, Green API)
# Only database calls remain in database.py

import os
import requests
import tempfile
from threading import Lock
from urllib.parse import quote

# Import logging functions
from core.logger import (
    log_chatgpt_request, log_chatgpt_response, log_chatgpt_error,
    log_video_request, log_video_response, log_video_error,
    log_link_shorten_request, log_link_shorten_response, log_link_error,
    log_link_list_request, log_link_list_response,
    log_link_stats_request, log_link_stats_response,
    log_greenapi_send, log_greenapi_response
)

# ==================== GREEN API CREDENTIALS ====================

# Thread-safe credential storage for Green API
_green_api_credentials = {
    'instance_id': None,
    'token': None
}
_credentials_lock = Lock()

# Environment variable fallback
GREEN_API_INSTANCE_ID = os.getenv("GREEN_API_INSTANCE_ID", "")
GREEN_API_TOKEN = os.getenv("GREEN_API_TOKEN", "")


def greenapi_set_credentials(instance_id, token):
    # Set Green API credentials (thread-safe)
    # Args: instance_id (str), token (str)
    with _credentials_lock:
        _green_api_credentials['instance_id'] = instance_id
        _green_api_credentials['token'] = token


def _get_greenapi_credentials():
    # Get current Green API credentials (internal use only)
    # Returns: (instance_id, token) tuple
    with _credentials_lock:
        instance_id = _green_api_credentials.get('instance_id') or GREEN_API_INSTANCE_ID
        token = _green_api_credentials.get('token') or GREEN_API_TOKEN
        return instance_id, token


# ==================== CHATGPT API ====================

BATGPT_API_BASE = "https://batgpt.vercel.app/api/gpt"


def chatgpt_send_message(message, gpt_chat_id=None):
    # Send message to ChatGPT API and get response
    # Args: message (str), gpt_chat_id (str, optional) - for conversation continuity
    # Returns: dict with 'success', 'response', 'chat_id' or error details
    
    log_chatgpt_request(gpt_chat_id)
    
    try:
        encoded_message = quote(message)
        
        if gpt_chat_id:
            url = f"{BATGPT_API_BASE}?chatid={gpt_chat_id}&message={encoded_message}"
        else:
            url = f"{BATGPT_API_BASE}?message={encoded_message}"
        
        response = requests.get(url, timeout=30)
        
        if response.status_code != 200:
            log_chatgpt_error('http', status_code=response.status_code)
            return {
                'success': False,
                'error_type': 'http_error',
                'status_code': response.status_code
            }
        
        data = response.json()
        
        # Extract response and chat ID
        gpt_response = data.get('reply') or data.get('response') or data.get('message')
        new_chat_id = data.get('chatid') or data.get('chat_id')
        
        if not gpt_response:
            log_chatgpt_error('no_response')
            return {
                'success': False,
                'error_type': 'no_response',
                'raw_data': data
            }
        
        log_chatgpt_response(gpt_response)
        return {
            'success': True,
            'response': gpt_response,
            'chat_id': new_chat_id
        }
        
    except requests.exceptions.Timeout:
        log_chatgpt_error('timeout')
        return {
            'success': False,
            'error_type': 'timeout'
        }
    except requests.exceptions.RequestException as e:
        log_chatgpt_error('connection', error=str(e))
        return {
            'success': False,
            'error_type': 'connection_error',
            'error': str(e)
        }
    except Exception as e:
        log_chatgpt_error('processing', error=str(e))
        return {
            'success': False,
            'error_type': 'processing_error',
            'error': str(e)
        }


# ==================== VIDEO DOWNLOADER API ====================

BATGPT_DOWNLOADER_API = "https://batgpt.vercel.app/api/alldl"


def video_download_request(url):
    # Download video from social media URL using BatGPT API
    # Args: url (str) - social media video URL
    # Returns: dict with 'success', 'media_url', 'title' or error details
    
    log_video_request(url)
    
    try:
        encoded_url = quote(url, safe='')
        api_url = f"{BATGPT_DOWNLOADER_API}?url={encoded_url}"
        
        response = requests.get(api_url, timeout=60)
        
        if response.status_code != 200:
            log_video_error('http', status_code=response.status_code, response_text=response.text[:200])
            return {
                'success': False,
                'error_type': 'http_error',
                'status_code': response.status_code,
                'response_text': response.text[:200]
            }
        
        data = response.json()
        
        # Check if download was successful
        if not data.get('success') and data.get('success') is not None:
            log_video_error('api_failed', raw_data=str(data)[:200])
            return {
                'success': False,
                'error_type': 'api_failed',
                'raw_data': data
            }
        
        media_info = data.get('mediaInfo', {})
        
        # Extract video URL and title
        if isinstance(media_info, dict):
            video_url = media_info.get('videoUrl')
            title = media_info.get('title', 'Downloaded Video')
        else:
            video_url = None
            title = 'Downloaded Video'
        
        if not video_url:
            log_video_error('no_url', media_info=str(media_info)[:200])
            return {
                'success': False,
                'error_type': 'no_video_url',
                'media_info': media_info
            }
        
        log_video_response(title)
        return {
            'success': True,
            'media_url': video_url,
            'title': title
        }
        
    except requests.exceptions.Timeout:
        log_video_error('timeout')
        return {
            'success': False,
            'error_type': 'timeout'
        }
    except requests.exceptions.RequestException as e:
        log_video_error('connection', error=str(e))
        return {
            'success': False,
            'error_type': 'connection_error',
            'error': str(e)
        }
    except ValueError as e:
        log_video_error('json', error=str(e))
        return {
            'success': False,
            'error_type': 'json_parse_error',
            'error': str(e)
        }
    except Exception as e:
        log_video_error('processing', error=str(e))
        return {
            'success': False,
            'error_type': 'processing_error',
            'error': str(e)
        }


# ==================== LINK SHORTENER API ====================

ICE_BIO_API_KEY = os.getenv("ICE_BIO_API_KEY", "")
ICE_BIO_API_URL = "https://ice.bio/api/url/add"
ICE_BIO_LIST_URL = "https://ice.bio/api/urls"


def link_shorten_request(url, custom_alias=None, password=None):
    # Shorten URL using ice.bio API
    # Args: url (str), custom_alias (str, optional), password (str, optional)
    # Returns: dict with 'success', 'link_id', 'short_url' or error details
    
    log_link_shorten_request(url)
    
    try:
        headers = {
            'Authorization': f'Bearer {ICE_BIO_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'url': url,
            'channel': 159,
        }
        
        if custom_alias:
            payload['custom'] = custom_alias
        
        if password:
            payload['password'] = password
        
        response = requests.post(ICE_BIO_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            log_link_error('http', status_code=response.status_code)
            return {
                'success': False,
                'error_type': 'http_error',
                'status_code': response.status_code
            }
        
        data = response.json()
        
        if data.get('error') == 0:
            link_id = data.get('id')
            short_url = data.get('shorturl')
            
            if not link_id or not short_url:
                log_link_error('incomplete', raw_data=str(data)[:200])
                return {
                    'success': False,
                    'error_type': 'incomplete_response',
                    'raw_data': data
                }
            
            log_link_shorten_response(short_url, link_id)
            return {
                'success': True,
                'link_id': link_id,
                'short_url': short_url
            }
        else:
            log_link_error('api', error_code=data.get('error', 'Unknown'), error_message=data.get('msg', 'An error occurred'))
            return {
                'success': False,
                'error_type': 'api_error',
                'error_code': data.get('error', 'Unknown'),
                'error_message': data.get('msg', 'An error occurred')
            }
            
    except requests.exceptions.Timeout:
        log_link_error('timeout')
        return {
            'success': False,
            'error_type': 'timeout'
        }
    except requests.exceptions.ConnectionError as e:
        log_link_error('connection', error=str(e))
        return {
            'success': False,
            'error_type': 'connection_error',
            'error': str(e)
        }
    except Exception as e:
        log_link_error('unexpected', error=str(e))
        return {
            'success': False,
            'error_type': 'unexpected_error',
            'error': str(e)
        }


def link_list_request(limit=1000, page=1):
    # Fetch all shortened links from ice.bio API
    # Args: limit (int), page (int)
    # Returns: dict with 'success', 'links' list or error details
    
    log_link_list_request()
    
    try:
        headers = {
            'Authorization': f'Bearer {ICE_BIO_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        params = {
            'limit': limit,
            'page': page,
            'order': 'date'
        }
        
        response = requests.get(ICE_BIO_LIST_URL, headers=headers, params=params, timeout=30)
        
        if response.status_code != 200:
            log_link_error('http', status_code=response.status_code)
            return {
                'success': False,
                'error_type': 'http_error',
                'status_code': response.status_code
            }
        
        data = response.json()
        
        if data.get('error') == '0' or data.get('error') == 0:
            urls = data.get('data', {}).get('urls', [])
            log_link_list_response(len(urls))
            return {
                'success': True,
                'links': urls
            }
        else:
            log_link_error('api', error_code=data.get('error', 'Unknown'), error_message=data.get('msg', 'Unknown error'))
            return {
                'success': False,
                'error_type': 'api_error',
                'error_message': data.get('msg', 'Unknown error')
            }
            
    except Exception as e:
        log_link_error('unexpected', error=str(e))
        return {
            'success': False,
            'error_type': 'unexpected_error',
            'error': str(e)
        }


def link_stats_request(link_id):
    # Fetch statistics for a specific shortened link from ice.bio API
    # Args: link_id (int or str) - the ID of the shortened link
    # Returns: dict with 'success', 'details', 'data' or error details
    
    log_link_stats_request(link_id)
    
    try:
        headers = {
            'Authorization': f'Bearer {ICE_BIO_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        url = f"https://ice.bio/api/url/{link_id}"
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            log_link_error('http', status_code=response.status_code)
            return {
                'success': False,
                'error_type': 'http_error',
                'status_code': response.status_code
            }
        
        data = response.json()
        
        if data.get('error') == 0 or data.get('error') == '0':
            details = data.get('details', {})
            stats_data = data.get('data', {})
            
            if not details or not stats_data:
                log_link_error('incomplete', raw_data=str(data)[:200])
                return {
                    'success': False,
                    'error_type': 'incomplete_response',
                    'raw_data': data
                }
            
            clicks = stats_data.get('clicks', 0)
            log_link_stats_response(link_id, clicks)
            return {
                'success': True,
                'details': details,
                'data': stats_data
            }
        else:
            log_link_error('api', error_code=data.get('error', 'Unknown'), error_message=data.get('msg', 'Link not found or error'))
            return {
                'success': False,
                'error_type': 'api_error',
                'error_message': data.get('msg', 'Link not found or error')
            }
            
    except requests.exceptions.Timeout:
        log_link_error('timeout')
        return {
            'success': False,
            'error_type': 'timeout'
        }
    except requests.exceptions.ConnectionError as e:
        log_link_error('connection', error=str(e))
        return {
            'success': False,
            'error_type': 'connection_error',
            'error': str(e)
        }
    except Exception as e:
        log_link_error('unexpected', error=str(e))
        return {
            'success': False,
            'error_type': 'unexpected_error',
            'error': str(e)
        }


# ==================== GREEN API (WHATSAPP) ====================

def greenapi_send_message(chat_id, text):
    # Send text message via Green API
    # Args: chat_id, text
    # Returns: API response JSON or None on error
    
    instance_id, token = _get_greenapi_credentials()
    
    log_greenapi_send('message', chat_id)
    
    try:
        api_subdomain = instance_id[:4]
        url = f"https://{api_subdomain}.api.green-api.com/waInstance{instance_id}/sendMessage/{token}"
        
        payload = {
            "chatId": chat_id,
            "message": text
        }
        
        response = requests.post(url, json=payload, timeout=30)
        result = response.json() if response.status_code == 200 else None
        
        if result:
            log_greenapi_response(True, result.get('idMessage', 'N/A'))
        else:
            log_greenapi_response(False)
        
        return result
        
    except Exception:
        log_greenapi_response(False)
        return None


def greenapi_send_file_by_url(chat_id, file_url, filename, caption=None):
    # Send file from URL via Green API
    # Args: chat_id, file_url, filename, caption (optional)
    # Returns: API response JSON or None on error
    
    instance_id, token = _get_greenapi_credentials()
    
    log_greenapi_send('file_url', chat_id, filename=filename)
    
    try:
        api_subdomain = instance_id[:4]
        url = f"https://{api_subdomain}.api.green-api.com/waInstance{instance_id}/sendFileByUrl/{token}"
        
        payload = {
            "chatId": chat_id,
            "urlFile": file_url,
            "fileName": filename
        }
        
        if caption:
            payload["caption"] = caption
        
        response = requests.post(url, json=payload, timeout=60)
        result = response.json() if response.status_code == 200 else None
        
        if result:
            log_greenapi_response(True, result.get('idMessage', 'N/A'))
        else:
            log_greenapi_response(False)
        
        return result
        
    except Exception:
        log_greenapi_response(False)
        return None


def greenapi_send_file_by_upload(chat_id, file_path, filename, caption=None):
    # Upload and send file via Green API
    # Args: chat_id, file_path, filename, caption (optional)
    # Returns: API response JSON or None on error
    
    instance_id, token = _get_greenapi_credentials()
    
    log_greenapi_send('file_upload', chat_id, filename=filename)
    
    try:
        api_subdomain = instance_id[:4]
        url = f"https://{api_subdomain}.api.green-api.com/waInstance{instance_id}/sendFileByUpload/{token}"
        
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f)}
            data = {'chatId': chat_id}
            if caption:
                data['caption'] = caption
            
            response = requests.post(url, files=files, data=data, timeout=60)
            result = response.json() if response.status_code == 200 else None
            
            if result:
                log_greenapi_response(True, result.get('idMessage', 'N/A'))
            else:
                log_greenapi_response(False)
            
            return result
        
    except Exception:
        log_greenapi_response(False)
        return None


def greenapi_send_poll(chat_id, message, options):
    # Send poll via Green API
    # Args: chat_id, message, options (list of dicts)
    # Returns: API response JSON or None on error
    
    instance_id, token = _get_greenapi_credentials()
    
    try:
        api_subdomain = instance_id[:4]
        url = f"https://{api_subdomain}.api.green-api.com/waInstance{instance_id}/sendPoll/{token}"
        
        payload = {
            "chatId": chat_id,
            "message": message,
            "options": options
        }
        
        response = requests.post(url, json=payload, timeout=30)
        return response.json() if response.status_code == 200 else None
        
    except Exception:
        return None


def greenapi_send_location(chat_id, latitude, longitude, name=None, address=None):
    # Send location via Green API
    # Args: chat_id, latitude, longitude, name (optional), address (optional)
    # Returns: API response JSON or None on error
    
    instance_id, token = _get_greenapi_credentials()
    
    try:
        api_subdomain = instance_id[:4]
        url = f"https://{api_subdomain}.api.green-api.com/waInstance{instance_id}/sendLocation/{token}"
        
        payload = {
            "chatId": chat_id,
            "latitude": latitude,
            "longitude": longitude
        }
        
        if name:
            payload["nameLocation"] = name
        if address:
            payload["address"] = address
        
        response = requests.post(url, json=payload, timeout=30)
        return response.json() if response.status_code == 200 else None
        
    except Exception:
        return None


def greenapi_send_contact(chat_id, phone, first_name, last_name=None, company=None):
    # Send contact card via Green API
    # Args: chat_id, phone, first_name, last_name (optional), company (optional)
    # Returns: API response JSON or None on error
    
    instance_id, token = _get_greenapi_credentials()
    
    try:
        api_subdomain = instance_id[:4]
        url = f"https://{api_subdomain}.api.green-api.com/waInstance{instance_id}/sendContact/{token}"
        
        contact = {
            "phoneContact": phone,
            "firstName": first_name
        }
        
        if last_name:
            contact["lastName"] = last_name
        if company:
            contact["company"] = company
        
        payload = {
            "chatId": chat_id,
            "contact": contact
        }
        
        response = requests.post(url, json=payload, timeout=30)
        return response.json() if response.status_code == 200 else None
        
    except Exception:
        return None


def greenapi_get_settings():
    # Get instance settings via Green API
    # Returns: API response JSON or None on error
    
    instance_id, token = _get_greenapi_credentials()
    
    try:
        api_subdomain = instance_id[:4]
        url = f"https://{api_subdomain}.api.green-api.com/waInstance{instance_id}/getSettings/{token}"
        
        response = requests.get(url, timeout=30)
        return response.json() if response.status_code == 200 else None
        
    except Exception:
        return None


def greenapi_check_whatsapp(phone_number):
    # Check if number has WhatsApp via Green API
    # Args: phone_number
    # Returns: API response JSON or None on error
    
    instance_id, token = _get_greenapi_credentials()
    
    try:
        api_subdomain = instance_id[:4]
        url = f"https://{api_subdomain}.api.green-api.com/waInstance{instance_id}/checkWhatsapp/{token}"
        
        payload = {
            "phoneNumber": int(phone_number) if isinstance(phone_number, str) else phone_number
        }
        
        response = requests.post(url, json=payload, timeout=30)
        return response.json() if response.status_code == 200 else None
        
    except Exception:
        return None


def greenapi_get_avatar(chat_id):
    # Get avatar via Green API
    # Args: chat_id
    # Returns: API response JSON or None on error
    
    instance_id, token = _get_greenapi_credentials()
    
    try:
        api_subdomain = instance_id[:4]
        url = f"https://{api_subdomain}.api.green-api.com/waInstance{instance_id}/getAvatar/{token}"
        
        payload = {
            "chatId": chat_id
        }
        
        response = requests.post(url, json=payload, timeout=30)
        return response.json() if response.status_code == 200 else None
        
    except Exception:
        return None


def greenapi_get_contact_info(chat_id):
    # Get contact info via Green API
    # Args: chat_id
    # Returns: API response JSON or None on error
    
    instance_id, token = _get_greenapi_credentials()
    
    try:
        api_subdomain = instance_id[:4]
        url = f"https://{api_subdomain}.api.green-api.com/waInstance{instance_id}/getContactInfo/{token}"
        
        payload = {
            "chatId": chat_id
        }
        
        response = requests.post(url, json=payload, timeout=30)
        return response.json() if response.status_code == 200 else None
        
    except Exception:
        return None


def greenapi_download_avatar_file(avatar_url, chat_id):
    # Download avatar from URL and save as temp file
    # Args: avatar_url, chat_id
    # Returns: temp file path or None on error
    
    try:
        response = requests.get(avatar_url, timeout=30)
        
        if response.status_code != 200:
            return None
        
        # Create temp file with unique name
        clean_chat_id = chat_id.replace('@c.us', '').replace('@g.us', '')
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.jpg',
            prefix=f'avatar_{clean_chat_id}_'
        )
        temp_file.write(response.content)
        temp_file.close()
        
        return temp_file.name
        
    except Exception:
        return None
