from django import template
from web.forms.statics import FORMS_BY_KEY
register = template.Library()


@register.simple_tag()
def client_status(client, form_key, *args, **kwargs):
    if not FORMS_BY_KEY.get(form_key):
        return {}
    return client.status(FORMS_BY_KEY.get(form_key).get('sections', []))
