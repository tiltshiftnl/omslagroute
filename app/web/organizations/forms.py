from django import forms
from .models import *
from django.utils.translation import ugettext_lazy as _


class OrganizationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = _('Naam organisatie')
        self.fields['name_abbreviation'].label = _('Afkorting organisatie')

    class Meta:
        model = Organization
        fields = (
            'name',
            'name_abbreviation',
        )
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Naam organisatie','aria-label': 'Naam organisatie'}),
            'name_abbreviation': forms.TextInput(attrs={'placeholder': 'NIEUW','aria-label': 'Afkorting naam organisatie'}),
        }


class FederationForm(forms.ModelForm):

    class Meta:
        model = Federation
        exclude = [
            'name_abbreviation',
            'main_email',
        ]
        # # enable readonly widget when Keycloak send federation id.
        # widgets = {
        #     'federation_id': forms.TextInput(attrs={
        #         'readonly': 'readonly',
        #     }),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].label = _('Organisatie type')