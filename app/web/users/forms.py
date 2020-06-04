from django.contrib.auth.forms import (
    AuthenticationForm as DefaultAuthenticationForm, authenticate
)
from django import forms
from django.forms import widgets
from .models import *
from django.http import HttpResponse
from web.profiles.models import Profile
from django.forms.models import inlineformset_factory
from web.organizations.models import Organization
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm
from web.forms.widgets import CheckboxSelectMultiple
from django.forms.utils import ErrorList


class FilterListForm(forms.Form):
    filter = forms.CharField(
        label='Filter lijst',
        widget=CheckboxSelectMultiple(
            choices=User.user_types,
        ),
        required=False,
    )

class FilterListFederationForm(forms.Form):
    filter = forms.CharField(
        label='Filter lijst',
        widget=CheckboxSelectMultiple(
            choices=User.federation_user_types,
        ),
        required=False,
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


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'user_type',
            'federation',
        )

class FederationUserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'user_type',
        )

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None, use_required_attribute=None,
                 renderer=None):
        

        super().__init__(data=data, files=files, auto_id=auto_id, prefix=prefix,
                 initial=initial, error_class=error_class, label_suffix=label_suffix,
                 empty_permitted=empty_permitted, instance=instance, use_required_attribute=use_required_attribute,
                 renderer=renderer)

        self.fields['user_type'].choices = User.federation_user_types


class UserCreationForm(DefaultUserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'disabled': 'disabled'}
        ),
        required=False
    )

    class Meta:
        model = User
        fields = (
            'username',
            'user_type',
        )


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        model = Profile
        exclude = [
            'cases',
            'user',
            'organization',
        ]


ProfileFormSet = inlineformset_factory(
    parent_model=User,
    model=Profile,
    form=ProfileForm,
    can_delete=False,
    extra=1
)
