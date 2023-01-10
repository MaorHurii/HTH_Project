from django import template

register = template.Library()


def validate_role(user, role):
    if not user.is_superuser:
        return user.groups.filter(name=role).exists


register.filter('validate_role', validate_role)
