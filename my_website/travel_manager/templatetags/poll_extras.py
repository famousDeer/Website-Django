from django import template

register = template.Library()

@register.filter(name="split")
def split(value, arg):
    """Split string base on arg

    Args:
        value (string): Entire word you wanna split
        arg (string): Separator
    """
    return value.split(arg)