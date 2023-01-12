from django import template

register = template.Library()


# These will be tags and filters tobe used inside the HTML templates
def validate_role(user, role):
    # This checks if the user is not an admin, if it's not it return True if it's part of the role, otherwise false
    if not user.is_superuser:
        return user.groups.filter(name=role).exists()


register.filter('validate_role', validate_role)
