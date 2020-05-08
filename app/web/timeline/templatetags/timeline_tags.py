from django import template
from django.contrib.auth.models import Group
from web.users.auth import auth_test
register = template.Library()


@register.simple_tag(takes_context=True)
def doc_added(context, moment_id, added_str):
    request = context['request']
    referer = request.META.get('HTTP_REFERER')

    if referer and referer.split('/')[-1] == str(moment_id):
        return added_str
    if request.GET.get('m') and request.GET.get('m') == str(moment_id):
        return added_str
    return ''
