from django.conf import settings
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from constance import config
import os.path

SOURCE_COMMIT = settings.SOURCE_COMMIT
BRANCH_NAME = settings.BRANCH_NAME

if not SOURCE_COMMIT:
    fname = '/.git/FETCH_HEAD'
    if os.path.isfile(fname):
        f = open(fname, 'r')
        try:
            SOURCE_COMMIT = f.read(7)
            BRANCH_NAME = f.read().split("branch '")[1].split("'")[0]
        except:
            print('FETCH_HEAD not expected')


def app_settings(request=None):
    return {
        'SOURCE_COMMIT': SOURCE_COMMIT,
        'LOGIN_URL_NAME': settings.LOGIN_URL_NAME,
        'LOGOUT_URL_NAME': settings.LOGOUT_URL_NAME,
        'LOGIN_URL': settings.LOGIN_URL,
        'BRANCH_NAME': BRANCH_NAME,
        'HOMEPAGE_INTRO': config.HOMEPAGE_INTRO,
        'login_form': AuthenticationForm(),
    }
