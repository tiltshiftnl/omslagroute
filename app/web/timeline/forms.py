from django import forms
from .models import *
from web.documents.widgets import *
from django.forms.widgets import *
from web.documents.models import Document
from web.documents.forms import DocumentForm
from django.forms.models import inlineformset_factory


class MomentForm(forms.ModelForm):
    # name = forms.CharField(required=False)

    class Meta:
        model = Moment
        fields = ('name',
                  'description',
        )
