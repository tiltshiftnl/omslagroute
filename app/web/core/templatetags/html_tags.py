from django import template
from django.contrib.auth.models import Group
from web.users.auth import auth_test
register = template.Library()
from datetime import datetime, date


@register.filter(name='linebreaks2html')
def linebreaks2html(txt):
    if txt:
        return txt.replace("\n", "<br />")
    return ''


@register.filter(name='is_date')
def is_date(str_date):
    try:
        return isinstance(datetime.strptime(str_date, "%Y-%m-%d"), (date, datetime))
    except:
        return False


@register.filter(name='str_date_to_date')
def str_date_to_date(str_date):
    return datetime.strptime(str_date, "%Y-%m-%d")
