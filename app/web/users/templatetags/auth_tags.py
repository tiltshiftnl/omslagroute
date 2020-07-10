from django import template
from django.contrib.auth.models import Group
from web.users.auth import auth_test
register = template.Library()
from web.users.statics import *

@register.filter()
def user_type_verbose(user_type):
    return USER_TYPES_DICT.get(user_type)

@register.filter()
def has_group(user, group_name):
    return auth_test(user, group_name)


@register.filter()
def is_user_type(user, user_type):
    return auth_test(user, user_type)


@register.filter()
def is_redactie(user):
    return auth_test(user, REDACTIE)


@register.filter()
def is_begeleider(user):
    return auth_test(user, BEGELEIDER)


@register.filter()
def is_beheerder(user):
    return auth_test(user, BEHEERDER)


@register.filter()
def is_wonen_medewerker(user):
    return auth_test(user, WONEN)


@register.filter()
def is_federatie_beheerder(user):
    return auth_test(user, FEDERATIE_BEHEERDER)


@register.filter()
def is_pb_federatie_beheerder(user):
    return auth_test(user, PB_FEDERATIE_BEHEERDER)


@register.filter()
def is_woningcorporatie_medewerker(user):
    return auth_test(user, WONINGCORPORATIE_MEDEWERKER)


@register.filter()
def is_onbekent(user):
    return auth_test(user, ONBEKEND)


