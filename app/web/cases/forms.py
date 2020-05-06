from django import forms
from .models import *
from web.forms.forms import GenericModelForm
from web.forms.widgets import RadioSelect
from .statics import GESLACHT
from django.utils.translation import ugettext_lazy as _


class CaseForm(forms.ModelForm):
    geslacht = forms.ChoiceField(
        label=_('Geslacht'),
        required=True,
        widget=RadioSelect(),
        choices=GESLACHT
    )

    class Meta:
        model = Case
        exclude = []


class CaseGenericModelForm(GenericModelForm):
    class Meta:
        model = Case
        exclude = []


class SendCaseForm(forms.ModelForm):
    to_email = forms.EmailField(
        label=_('E-mailadres van de afdeling wonen van de gemeente Amsterdam'),
        required=False,
    )

    class Meta:
        model = Case
        fields = []


class DocumentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['uploaded_file'].label = "Selecteer een bestand"
        self.fields['name'].label = "Titel van de bijlage"

    class Meta:
        model = Document
        exclude = (
            'case',
        )
        widgets = {
            'uploaded_file': forms.FileInput(attrs={'id': 'file-upload', 'required': 'required'}),
        }


