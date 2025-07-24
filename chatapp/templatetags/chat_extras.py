from django import template

register = template.Library()

@register.filter
def get_other_participant(chat, user):
    """Get the other participant in a private chat"""
    return chat.get_other_participant(user)

@register.filter
def get_avatar_color(user_id):
    """Generate a consistent color for user avatar"""
    colors = [
        "linear-gradient(135deg, #ff6b6b, #ee5a24)",
        "linear-gradient(135deg, #a29bfe, #6c5ce7)", 
        "linear-gradient(135deg, #fd79a8, #e84393)",
        "linear-gradient(135deg, #fdcb6e, #e17055)",
        "linear-gradient(135deg, #74b9ff, #0984e3)",
        "linear-gradient(135deg, #55a3ff, #3742fa)",
        "linear-gradient(135deg, #26de81, #20bf6b)",
        "linear-gradient(135deg, #f7b731, #fa8231)",
    ]
    return colors[user_id % len(colors)]

@register.filter
def format_message_time(timestamp):
    """Format message timestamp to show relative time or time"""
    from django.utils import timezone
    from datetime import datetime, timedelta
    
    now = timezone.now()
    
    # If message is from today, show time
    if timestamp.date() == now.date():
        return timestamp.strftime('%I:%M %p').lstrip('0')
    
    # If message is from yesterday
    elif timestamp.date() == (now - timedelta(days=1)).date():
        return 'Yesterday'
    
    # If message is from this week
    elif (now - timestamp).days < 7:
        return timestamp.strftime('%A')  # Day name
    
    # If message is older
    else:
        return timestamp.strftime('%m/%d/%y')
