# WhatsApp Tools
# Public features for WhatsApp number checking and contact info
# Includes auto-detection for Pakistani numbers (11 digits starting with 0)

from core.api_requests import greenapi_check_whatsapp as check_whatsapp, greenapi_get_avatar as get_avatar, greenapi_get_contact_info as get_contact_info, greenapi_download_avatar_file as download_avatar_as_file
from config.messages import get_message
import re


def extract_phone_number(text):
    # Extract phone number from text (digits only)
    digits = re.sub(r'\D', '', text)
    return digits if digits else None


def detect_pakistani_number(phone_input):
    # Detect if it's a Pakistani number starting with 0 (11 digits)
    # Returns: formatted number with country code or None
    
    digits = extract_phone_number(phone_input)
    
    if not digits:
        return None
    
    # If 11 digits starting with 0, assume Pakistani number
    if len(digits) == 11 and digits.startswith('0'):
        return '92' + digits[1:]  # Replace 0 with 92
    
    return digits


def format_chat_id(identifier):
    # Convert phone number or partial chat_id to full chat_id format
    # Input: "923453870090" or "923453870090@c.us"
    # Output: "923453870090@c.us"
    
    if '@' in identifier:
        return identifier
    
    clean_number = re.sub(r'\D', '', identifier)
    return f"{clean_number}@c.us"


def handle_checkwhatsapp(phone_input):
    # Check if a phone number has WhatsApp
    # Auto-detects Pakistani numbers (11 digits starting with 0)
    # Returns: formatted response message
    
    if not phone_input or phone_input.strip() == '':
        return {
            'type': 'usage',
            'message': get_message("checkwa_usage")
        }
    
    phone_number = detect_pakistani_number(phone_input)
    
    if not phone_number:
        return {
            'type': 'result',
            'message': get_message("checkwa_invalid_number")
        }
    
    # Validate length
    if len(phone_number) < 10:
        return {
            'type': 'result',
            'message': get_message("checkwa_number_too_short")
        }
    
    # Check if number starts with 0 and is not 11 digits (needs country code)
    original_digits = extract_phone_number(phone_input)
    if original_digits and original_digits.startswith('0') and len(original_digits) != 11:
        return {
            'type': 'result',
            'message': get_message("checkwa_needs_country_code", number=original_digits)
        }
    
    result = check_whatsapp(phone_number)
    
    if not result:
        # Check if original input started with 0
        if original_digits and original_digits.startswith('0'):
            return {
                'type': 'result',
                'message': get_message("checkwa_error_pakistani")
            }
        else:
            return {
                'type': 'result',
                'message': get_message("checkwa_error")
            }
    
    exists = result.get('existsWhatsapp', False)
    
    # Determine display format: preserve original input if it started with 0, otherwise use + prefix
    if original_digits and original_digits.startswith('0'):
        # Show original format for numbers starting with 0
        number_display = original_digits
    else:
        # Show with + prefix for international numbers
        number_display = f"+{phone_number}"
    
    if exists:
        return {
            'type': 'result',
            'message': get_message("checkwa_found", number=number_display)
        }
    else:
        # Check if Pakistani number without country code
        extracted = extract_phone_number(phone_input)
        if phone_input and extracted and len(extracted) == 11:
            return {
                'type': 'result',
                'message': get_message("checkwa_not_found_pakistani", number=number_display, suggestion=phone_input[1:])
            }
        else:
            return {
                'type': 'result',
                'message': get_message("checkwa_not_found", number=number_display)
            }


def handle_getavatar(identifier_input):
    # Get avatar for a user or group
    # Sends avatar as file, not URL
    # Returns: dict with 'type', 'message', optional 'file_path'
    
    if not identifier_input or identifier_input.strip() == '':
        return {
            'type': 'usage',
            'message': get_message("avatar_usage")
        }
    
    # Detect Pakistani number if applicable
    phone_number = detect_pakistani_number(identifier_input)
    chat_id = format_chat_id(phone_number if phone_number else identifier_input)
    
    result = get_avatar(chat_id)
    
    if not result:
        return {
            'type': 'result',
            'message': get_message("avatar_error")
        }
    
    avatar_url = result.get('urlAvatar')
    
    if avatar_url:
        # Download avatar as file
        file_path = download_avatar_as_file(avatar_url, chat_id)
        
        if file_path:
            return {
                'type': 'result',
                'message': get_message("avatar_found"),
                'avatar_url': avatar_url,
                'file_path': file_path
            }
        else:
            # Fallback to URL if download fails
            return {
                'type': 'result',
                'message': get_message("avatar_found_url", chat_id=chat_id, avatar_url=avatar_url),
                'avatar_url': avatar_url
            }
    else:
        return {
            'type': 'result',
            'message': get_message("avatar_no_avatar", chat_id=chat_id)
        }


def handle_getcontactinfo(identifier_input):
    # Get contact information
    # Shows wa.me link format instead of chat ID
    # Returns: formatted response message
    
    if not identifier_input or identifier_input.strip() == '':
        return get_message("contactinfo_usage")
    
    # Detect Pakistani number if applicable
    phone_number = detect_pakistani_number(identifier_input)
    chat_id = format_chat_id(phone_number if phone_number else identifier_input)
    
    result = get_contact_info(chat_id)
    
    if not result:
        return get_message("contactinfo_error")
    
    name = result.get('name', 'N/A')
    avatar = result.get('avatar', 'No avatar')
    
    # Extract phone number for wa.me link
    phone_only = chat_id.replace('@c.us', '').replace('@g.us', '')
    wa_me_link = f"wa.me/{phone_only}"
    
    # Build response using message templates
    response = get_message("contactinfo_header")
    response += get_message("contactinfo_whatsapp", wa_me_link=wa_me_link)
    response += get_message("contactinfo_name", name=name)
    
    if avatar and avatar != 'No avatar':
        response += get_message("contactinfo_has_avatar")
    else:
        response += get_message("contactinfo_no_avatar")
    
    return response
