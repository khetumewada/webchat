from django.contrib.auth.models import User


def create_username_from_names(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return

    first_name = details.get('first_name', '').strip().lower()
    last_name = details.get('last_name', '').strip().lower()

    # Create base username from first + last name
    base_username = (first_name + last_name).replace(" ", "") or "user"

    # Ensure it's unique
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    # Save to kwargs so Django creates user with this username
    kwargs['username'] = username
    return {'username': username}
