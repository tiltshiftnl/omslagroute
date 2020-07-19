from django import template
from web.forms.statics import FORMS_BY_KEY, FORMS_BY_SLUG
from ..models import CaseVersion, CaseStatus
from ..statics import * 
register = template.Library()


@register.simple_tag()
def client_status(client, form_key, *args, **kwargs):
    if not FORMS_BY_SLUG.get(form_key):
        return {}
    return client.status(FORMS_BY_SLUG.get(form_key).get('sections', []))


@register.simple_tag()
def client_submitted_form(client, form_key, *args, **kwargs):
    case_status = CaseStatus.objects.filter(case=client, form=form_key).order_by('-created')
    if case_status:
        return case_status[0]
    return None


@register.simple_tag()
def case_status_list_latest(case, *args, **kwargs):
    case_status_list = CaseStatus.objects.filter(
        case=case,
        status__in=[
            CASE_STATUS_INGEDIEND,
            CASE_STATUS_AFGEKEURD,
            CASE_STATUS_IN_BEHANDELING,
            CASE_STATUS_GOEDGEKEURD,
        ]
    ).order_by('-created')
    return case_status_list


@register.filter()
def status_verbose(status):
    return CASE_STATUS_DICT.get(status, {}).get('current')


@register.filter()
def form_verbose(form):
    return FORMS_BY_SLUG.get(form, {}).get('title')


@register.filter()
def form_federation_type(form):
    return FORMS_BY_SLUG.get(form, {}).get('federation_type')
