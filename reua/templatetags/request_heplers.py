from django import template
from django.conf import settings
from django.urls import translate_url

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

@register.simple_tag
def gmaps_api_key():
    return settings.GMAP_API_KEY

@register.simple_tag(takes_context=True)
def full_url(context, url):
    return context.request.build_absolute_uri(url)

@register.simple_tag(takes_context=True)
def change_lang(context, lang_code):
    path = context['request'].get_full_path()
    return translate_url(path, lang_code)