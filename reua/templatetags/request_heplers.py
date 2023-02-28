from django import template

from reua.bleach_sanitarize import bleach_clean

register = template.Library()

@register.simple_tag
def extend_current_url(dict, prop, value):
    d = dict.copy()
    d[prop] = value
    return d.urlencode()

@register.filter()
def bleach_sanitarize(value: str) -> str:
    return bleach_clean(value)
