from django import template
from web.forms.statics import FORMS_BY_KEY, FORMS_BY_SLUG
from ..models import CaseVersion, CaseStatus
from ..statics import CASE_STATUS_DICT
register = template.Library()


@register.simple_tag()
def client_status(client, form_key, *args, **kwargs):
    if not FORMS_BY_SLUG.get(form_key):
        return {}
    return client.status(FORMS_BY_SLUG.get(form_key).get('sections', []))


@register.simple_tag()
def client_submitted_form(client, form_key, *args, **kwargs):
    case_versions = CaseVersion.objects.filter(case=client, version_verbose=form_key).order_by('created')
    case_status = CaseStatus.objects.filter(case=client, form=form_key).order_by('-created')
    if case_status:
        return case_status[0]
    return None


@register.filter()
def status_verbose(status):
    return CASE_STATUS_DICT.get(status).get('current')
