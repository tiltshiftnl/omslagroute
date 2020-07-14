from django import template
from ..models import CaseStatus 
from ..statics import CASE_STATUS_WONINGCORPORATIE_GOEDGEKEURD
register = template.Library()


@register.simple_tag()
def case_data(case, fields, *args, **kwargs):
    return case.to_dict(fields)


@register.simple_tag()
def case_form_data(case, organization, form, *args, **kwargs):
    if case and organization and form:
        return organization.get_case_form_data(case, form)
    return []


@register.simple_tag()
def case_data_by_field_name(data, field_name, *args, **kwargs):
    return data.get(field_name, {})


@register.simple_tag()
def get_case_versions(versions, key, *args, **kwargs):
    if not versions:
        return False
    return versions.get(key)


@register.simple_tag()
def get_case_status_list(case, form, *args, **kwargs):
    case_status_list = CaseStatus.objects.filter(
        case=case,
        form=form,
        status=CASE_STATUS_WONINGCORPORATIE_GOEDGEKEURD,
    )
    return case_status_list
