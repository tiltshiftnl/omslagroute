from django.contrib.auth.forms import (
    AuthenticationForm as DefaultAuthenticationForm, authenticate
)
from django import forms
from .models import *
from web.profiles.models import Profile
from django.forms.models import inlineformset_factory
from web.organizations.models import Organization


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


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        widgets = {
            'password': forms.PasswordInput
        }


class ProfileForm(forms.ModelForm):
    user = forms.CharField(required=True, widget=forms.HiddenInput())
    organization = forms.ModelChoiceField(required=True, widget=forms.RadioSelect(), queryset=Organization.objects.all())

    class Meta:
        model = Profile
        exclude = ['cases', ]


ProfileFormSet = inlineformset_factory(
    parent_model=User,
    model=Profile,
    form=ProfileForm,
    can_delete=False,
    extra=1
)
