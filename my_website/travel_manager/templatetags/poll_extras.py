from django import template
import os

register = template.Library()

@register.filter(name="split")
def split(value, arg):
    """Split string base on arg

    Args:
        value (string): Entire word you wanna split
        arg (string): Separator
    """
    return value.split(arg)

@register.filter(name="basename")
def basename(value):
    """Taking the name of file without dir

    Args:
        value (string): URL of file
    """
    return os.path.basename(value)