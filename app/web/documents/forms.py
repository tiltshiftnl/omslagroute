from django import forms
from django.forms.widgets import RadioSelect
from .models import *
from django.forms.models import inlineformset_factory


class DocumentVersionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['uploaded_file'].label = "Selecteer een bestand"

    class Meta:
        model = DocumentVersion
        exclude = ()
        widgets = {
            'uploaded_file': forms.FileInput(attrs={'id': 'file-upload', 'required': 'required'}),
            'document': forms.HiddenInput,
        }


class DocumentForm(forms.ModelForm):
    # moment_id = forms.IntegerField(label='Moment id', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.empty_label=None
        self.fields['name'].label = "Titel van het document:"
        self.fields['document_type'].label = "Om wat voor soort document gaat het?"

        # Removes the first choice (meant to clean up select)

        # for field_name in self.fields:
        #     field = self.fields.get(field_name)
        #     if field and isinstance(field , forms.TypedChoiceField):
        #         field.choices = field.choices[1:]

    class Meta:
        model = Document
        exclude = ()
        widgets = {
            # 'name': forms.TextInput(attrs={'placeholder': 'Bestandsnaam'}),
            'document_type': forms.RadioSelect(attrs={'class': 'form-field__radio'})
        }


DocumentVersionFormSet = inlineformset_factory(
    parent_model=Document,
    model=DocumentVersion,
    form=DocumentVersionForm,
    can_delete=False,
    extra=1
)
