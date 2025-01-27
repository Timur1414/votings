from django import template

register = template.Library()


@register.filter
def is_user_voted(variant, user):
    return variant.is_user_voted(user)
