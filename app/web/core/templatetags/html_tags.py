from django import template
from django.contrib.auth.models import Group
from web.users.auth import auth_test
register = template.Library()
from datetime import datetime, date
from django.utils.html import mark_safe


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
    print(str_date)
    print(type(str_date))
    return datetime.strptime(str_date, "%Y-%m-%d")


@register.filter(name='textile')
def textile(textile_str):
    from textile import textile
    return mark_safe(textile(str(textile_str)))


@register.filter(name='range')
def _range(_min, args=None):
    _max, _step = None, None
    if args:
        if not isinstance(args, int):
            _max, _step = map(int, args.split(','))
        else:
            _max = args
    args = filter(None, (_min, _max, _step))
    return range(*args)
