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
