from django import template

register = template.Library()


@register.filter
def get_list(dictionary, key):
    """Get request lists, rather than last value in list."""
    return dictionary.getlist(key)
