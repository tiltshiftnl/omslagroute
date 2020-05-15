from django import forms
from .models import *
from web.forms.forms import GenericModelForm
from web.forms.widgets import RadioSelect, CheckboxSelectMultipleDocument, CheckboxSelectMultiple
from .statics import GESLACHT
from web.forms.statics import FORMS_PROCESSTAP_CHOICES
from django.utils.translation import ugettext_lazy as _
from web.forms.fields import MultiSelectFormField


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['document_list'] = forms.ModelMultipleChoiceField(
            label=_('Bijlagen'),
            queryset=Document.objects.filter(case=kwargs.get('instance')),
            widget=CheckboxSelectMultipleDocument(
                attrs={
                    'instance_id': self.instance.id,
                    'path': self.path,
                }
            ),
            required=False,
        )

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
    forms = MultiSelectFormField(
        label=_('Formulieren'),
        help_text=_('Als er formulieren zijn waar deze bijlage aan toegevoegd moet worden, dan kun je die hier aanvinken'),
        choices=FORMS_PROCESSTAP_CHOICES,
        required=False
    )

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


