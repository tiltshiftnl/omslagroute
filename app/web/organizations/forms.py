from django import forms
from .models import *
from django.utils.translation import ugettext_lazy as _


class OrganizationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = _('Naam organisatie')

    class Meta:
        model = Organization
        fields = (
            'name',
        )

