from django import template
from django.contrib.auth.models import Group
from web.users.auth import auth_test
register = template.Library()


@register.filter(name='linebreaks2html')
def linebreaks2html(txt):
    return txt.replace("\n", "<br>")
