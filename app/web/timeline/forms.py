from django import forms
from .models import *
from django.utils.translation import ugettext_lazy as _
from web.documents.widgets import *
from django.forms.widgets import *
from web.documents.models import Document
from web.documents.forms import DocumentForm
from django.forms.models import inlineformset_factory


class MomentForm(forms.ModelForm):
    # name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = _('Naam processtap')
        self.fields['description'].label = _('Omschrijving processtap')

    class Meta:
        model = Moment
        fields = ('name',
                  'order',
                  'description',
                  'roles',
        )
        widgets = {
            'roles': forms.CheckboxSelectMultiple()
        }
