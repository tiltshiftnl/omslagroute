from django.conf import settings
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)


def app_settings(request=None):
    return {
        'SOURCE_COMMIT': settings.SOURCE_COMMIT,
        'BRANCH_NAME': settings.BRANCH_NAME,
        'login_form': AuthenticationForm(),
    }
