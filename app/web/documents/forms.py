from django import forms
from .models import DocumentVersion


class DocumentForm(forms.ModelForm):

    class Meta:
        model = DocumentVersion
        fields = ('uploaded_file', 'document',)
        widgets = {
            'document': forms.HiddenInput,
        }
