from django import template
import datetime
register = template.Library()


@register.filter
def remove(value):
    # Find the last underscore and slice from there
    return value[8:]


@register.filter
def format_unix_time(value):
    try:
        timestamp = int(value)
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return "Invalid Time"
