from django import forms
from .models import DocumentVersion


class DocumentForm(forms.ModelForm):

    class Meta:
        model = DocumentVersion
        fields = ('uploaded_file', 'document',)
        widgets = {
            'uploaded_file': forms.FileInput(attrs={'id': "file-upload"}),
            'document': forms.HiddenInput,
        }
            