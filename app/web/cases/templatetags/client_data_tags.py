from django import template
from web.forms.statics import SECTIONS_DICT
register = template.Library()


@register.simple_tag()
def case_data(case, fields, *args, **kwargs):
    return case.to_dict(fields)
