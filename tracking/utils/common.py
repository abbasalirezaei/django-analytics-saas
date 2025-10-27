def validate_tracking_data(data, required_fields):
    """
    Validate tracking data and return validation result
    """
    errors = []

    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"{field} is required")

    return len(errors) == 0, errors


def get_client_info(request):
    """
    Extract client information from request
    """
    return {
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        'ip_address': get_client_ip(request),
        # Cloudflare country
        'country': request.META.get('HTTP_CF_IPCOUNTRY', ''),
    }


def get_client_ip(request):
    """
    Get client IP address from request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def detect_device_type(user_agent):
    """
    Detect device type from user agent
    """
    user_agent_lower = user_agent.lower()

    if any(mobile in user_agent_lower for mobile in ['mobile', 'android', 'iphone']):
        return 'mobile'
    elif any(tablet in user_agent_lower for tablet in ['tablet', 'ipad']):
        return 'tablet'
    else:
        return 'desktop'


def detect_browser(user_agent):
    """
    Detect browser from user agent
    """
    user_agent_lower = user_agent.lower()

    if 'chrome' in user_agent_lower:
        return 'chrome'
    elif 'firefox' in user_agent_lower:
        return 'firefox'
    elif 'safari' in user_agent_lower:
        return 'safari'
    elif 'edge' in user_agent_lower:
        return 'edge'
    else:
        return 'other'