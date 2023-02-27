from django import template

register = template.Library()

@register.simple_tag
def extend_current_url(dict, prop, value):
    d = dict.copy()
    d[prop] = value
    return d.urlencode()
