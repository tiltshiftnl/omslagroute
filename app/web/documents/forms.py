from django import forms
from django.forms.widgets import RadioSelect
from .models import *
from django.forms.models import inlineformset_factory


class DocumentVersionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['uploaded_file'].label = "New Email Label"

    class Meta:
        model = DocumentVersion
        exclude = ()
        widgets = {
            'uploaded_file': forms.FileInput(attrs={'id': 'file-upload', 'class': 'my-upload'}),
            'document': forms.HiddenInput,
        }


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.empty_label=None
        self.fields['name'].label = "Naam"
        self.fields['icon'].label = "Icon"

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]

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
