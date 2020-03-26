from django import forms
from .models import *


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        exclude = []
