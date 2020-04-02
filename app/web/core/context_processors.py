from django.conf import settings
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from constance import config


def app_settings(request=None):
    return {
        'SOURCE_COMMIT': settings.SOURCE_COMMIT,
        'BRANCH_NAME': settings.BRANCH_NAME,
        'HOMEPAGE_INTRO': config.HOMEPAGE_INTRO,
        'login_form': AuthenticationForm(),
    }
