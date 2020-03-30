from django import template
from web.forms.statics import SECTIONS_DICT
register = template.Library()


@register.simple_tag()
def client_status(client, section, *args, **kwargs):
    if not SECTIONS_DICT.get(section):
        return 0
    return client.status(SECTIONS_DICT.get(section))
