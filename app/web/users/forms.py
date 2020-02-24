from django.contrib.auth.forms import (
    AuthenticationForm as DefaultAuthenticationForm, authenticate
)


class AuthenticationForm(DefaultAuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                pass
                # raise forms.ValidationError(
                #     self.error_messages['invalid_login'],
                #     code='invalid_login',
                #     params={'username': self.username_field.verbose_name},
                # )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    # def confirm_login_allowed(self, user):
    #     pass
