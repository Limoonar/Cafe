# myapp/templatetags/cart_filters.py

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Safely get an item from a dictionary. If the key does not exist,
    it returns None. This prevents key errors.
    """
    return dictionary.get(str(key), 1)  # Default to 1 if key not found
