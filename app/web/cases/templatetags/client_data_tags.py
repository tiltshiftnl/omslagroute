from django import template
register = template.Library()


@register.simple_tag()
def case_data(case, fields, *args, **kwargs):
    return case.to_dict(fields)


@register.simple_tag()
def get_case_versions(versions, key, *args, **kwargs):
    if not versions:
        return False
    return versions.get(key)
