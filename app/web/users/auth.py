from web.profiles.models import Profile
from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from django.core.exceptions import SuspiciousOperation, ImproperlyConfigured
from keycloak_oidc.auth import OIDCAuthenticationBackend as DatapuntOIDCAuthenticationBackend
import logging
from .statics import GEBRUIKERS_BEHEERDER
from web.core.utils import validate_email_wrapper
import sendgrid
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
LOGGER = logging.getLogger(__name__)
try:
    from django.urls import reverse
except ImportError:
    # Django < 2.0.0
    from django.core.urlresolvers import reverse


def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME, user_type=None):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user, user_type):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def auth_test(user, user_type):
    if isinstance(user_type, list):
        return hasattr(user, 'user_type') and user.user_type in user_type
    return hasattr(user, 'user_type') and user.user_type == user_type


class OIDCAuthenticationBackend(DatapuntOIDCAuthenticationBackend):

    def create_user(self, claims):
        user = super().create_user(claims)
        profile = Profile()
        profile.user = user
        profile.save()
        addresses = [
            user.username for user in self.UserModel.objects.all().filter(user_type=GEBRUIKERS_BEHEERDER)
            if validate_email_wrapper(user.username)
        ]
        if settings.SENDGRID_KEY and addresses:
            current_site = get_current_site(self.request)
            data = {
                'site': current_site.domain,
                'url': reverse('update_user', kwargs={'pk': user.id})
            }
            body = render_to_string('users/mail/gebruikers_beheerders_new_user.txt', data)
            sg = sendgrid.SendGridAPIClient(settings.SENDGRID_KEY)
            email = Mail(
                from_email='no-reply@%s' % current_site.domain,
                to_emails=addresses,
                subject='Omslagroute - gebruiker aangemaakt',
                plain_text_content=body
            )
            sg.send(email)

        return user

    def get_userinfo(self, access_token, id_token, payload):
        userinfo = super().get_userinfo(access_token, id_token, payload)
        return userinfo

    def get_or_create_user(self, access_token, id_token, payload):

        user = super().get_or_create_user(access_token, id_token, payload)
        return user

    def authenticate(self, request, **kwargs):
        """Authenticates a user based on the OIDC code flow."""

        self.request = request
        if not self.request:
            return None

        state = self.request.GET.get('state')
        code = self.request.GET.get('code')
        nonce = kwargs.pop('nonce', None)

        if not code or not state:
            return None

        reverse_url = self.get_settings('OIDC_AUTHENTICATION_CALLBACK_URL',
                                        'oidc_authentication_callback')

        token_payload = {
            'client_id': self.OIDC_RP_CLIENT_ID,
            'client_secret': self.OIDC_RP_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'https://acc.omslagroute.amsterdam.nl%s' % reverse(reverse_url),
        }

        # Get the token
        token_info = self.get_token(token_payload)
        id_token = token_info.get('id_token')
        access_token = token_info.get('access_token')

        # Validate the token
        payload = self.verify_token(id_token, nonce=nonce)

        if payload:
            self.store_tokens(access_token, id_token)
            try:
                return self.get_or_create_user(access_token, id_token, payload)
            except SuspiciousOperation as exc:
                LOGGER.warning('failed to get or create user: %s', exc)
                return None

        return None
