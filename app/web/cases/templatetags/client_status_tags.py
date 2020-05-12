from django import template
from web.forms.statics import FORMS_BY_KEY, FORMS_BY_SLUG
from ..models import CaseVersion
register = template.Library()


@register.simple_tag()
def client_status(client, form_key, *args, **kwargs):
    if not FORMS_BY_SLUG.get(form_key):
        return {}
    return client.status(FORMS_BY_SLUG.get(form_key).get('sections', []))


@register.simple_tag()
def client_submitted_form(client, form_key, *args, **kwargs):
    case_versions = CaseVersion.objects.filter(case=client, version_verbose=form_key).order_by('created')
    if case_versions:
        return case_versions[0]
    return None
