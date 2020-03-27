from django import forms
from .models import *
from web.forms.forms import GenericModelForm


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        exclude = []


class CaseGenericModeForm(GenericModelForm):
    class Meta:
        model = Case
        exclude = []
