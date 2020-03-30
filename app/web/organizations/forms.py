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
            'name': forms.TextInput(attrs={'placeholder': 'Naam organisatie'}),
            'name_abbreviation': forms.TextInput(attrs={'placeholder': 'NIEUW'}),
        }
