from django import template

register = template.Library()


@register.filter
def remove(value):
    # Find the last underscore and slice from there
    return value[9:]


