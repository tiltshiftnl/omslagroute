from django import forms
from django.forms import widgets
from .models import *
from django.forms.models import inlineformset_factory


class DocumentVersionForm(forms.ModelForm):
    class Meta:
        model = DocumentVersion
        exclude = ()
        widgets = {
            'uploaded_file': forms.FileInput(attrs={'id': 'file-upload', 'class': 'my-upload'}),
            'document': forms.HiddenInput,
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        exclude = ()
        widgets = {
            'icon': forms.RadioSelect(attrs={'class': 'my-radio-select'})
        }


DocumentVersionFormSet = inlineformset_factory(
    parent_model=Document,
    model=DocumentVersion,
    form=DocumentVersionForm,
    can_delete=False,
    extra=1

)
