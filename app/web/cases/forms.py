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


class CaseGenericModeForm(GenericModelForm):
    class Meta:
        model = Case
        exclude = []
