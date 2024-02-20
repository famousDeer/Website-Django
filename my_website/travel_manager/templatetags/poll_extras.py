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

@register.filter(name="sum")
def sum(values, field_name):
    """Sum all value in field

    Args:
        value (float): Value from field
        field_name (string): Name of filed from table
    """
    total = 0
    for value in values:
        total += getattr(value, field_name)
    return total