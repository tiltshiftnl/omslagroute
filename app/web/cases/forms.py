from django import forms
from .models import *
from web.forms.forms import GenericModelForm
from web.forms.widgets import RadioSelect, CheckboxSelectMultipleDocument, CheckboxSelectMultiple, CheckboxSelectMultipleUser
from .statics import GESLACHT
from web.forms.statics import FORMS_PROCESSTAP_CHOICES
from django.utils.translation import ugettext_lazy as _
from web.forms.fields import MultiSelectFormField
from web.users.models import User
from web.users.statics import BEGELEIDER, PB_FEDERATIE_BEHEERDER

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

class CaseInviteUsersForm(forms.Form):
    user = None
    instance = None
    user_list = forms.ModelMultipleChoiceField(
        label=_('Met wie wil je samenwerken aan deze cliënt?'),
        help_text=_('Selecteer één of meerdere collega’s. Wanneer je kiest voor samenwerken met een collega kan deze:<ul><li>basisgegevens en aanvraagformulieren bekijken en bewerken</li><li>bijlagen downloaden en  toevoegen</li><li>formulieren verzenden naar afdeling Wonen Gemeente Amsterdam</li>'),
        queryset=User.objects.filter(user_type__in=[BEGELEIDER, PB_FEDERATIE_BEHEERDER]),
        widget=CheckboxSelectMultiple(attrs={'class': 'u-list-style-none scroll-list-container'}),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)
        linked_users = User.objects.filter(profile__in=self.instance.profile_set.all()).values('id')
        self.fields['user_list'].queryset = self.fields['user_list'].queryset.exclude(id__in=linked_users)

    class Meta:
        model = Case
        fields = []

class CaseInviteUsersConfirmForm(forms.Form):
    message = forms.CharField(
        label=_('Bericht (optioneel)'),
        help_text=_('Als je een bericht wil meesturen met in de bevestings e-mail, dan kun je dat hier doen.'),
        widget=forms.Textarea(
            attrs={
                'rows': 4,
            }
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Case
        fields = []


class CaseRemoveInvitedUsersForm(forms.Form):
    user = None
    instance = None
    user_list = forms.ModelMultipleChoiceField(
        label=_('Met wie wil je níet meer samenwerken aan deze cliënt?'),
        help_text=_('Wanneer je de samenwerking beëindigt kunnen deze collega’s géén:<ul><li>basisgegevens en aanvraagformulieren bekijken en bewerken</li><li>bijlagen downloaden en  toevoegen</li><li>formulieren verzenden naar afdeling Wonen Gemeente Amsterdam</li>'),
        queryset=User.objects.filter(user_type__in=[BEGELEIDER, PB_FEDERATIE_BEHEERDER]),
        widget=CheckboxSelectMultipleUser(attrs={'class': 'u-list-style-none scroll-list-container'}),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)
        linked_users = User.objects.filter(
            profile__in=self.instance.profile_set.filter(
                user__user_type__in=[BEGELEIDER, PB_FEDERATIE_BEHEERDER]
            ).exclude(
                user=self.user
            )
        )
        self.fields['user_list'].queryset = linked_users

    class Meta:
        fields = []


class CaseGenericModelForm(GenericModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['document_list'] = forms.ModelMultipleChoiceField(
            label=_('Vink de bijlagen aan die je bij de aanvraag mee wilt sturen naar de afdeling Wonen van de Gemeente Amsterdam'),
            queryset=Document.objects.filter(case=kwargs.get('instance')),
            widget=CheckboxSelectMultipleDocument(
                attrs={
                    'instance_id': self.instance.id,
                    'path': self.path,
                }
            ),
            required=False,
        )

    class Meta:
        model = Case
        exclude = []


class SendCaseForm(forms.ModelForm):

    to_email = forms.EmailField(
        label=_('E-mailadres van de afdeling wonen van de gemeente Amsterdam'),
        required=False,
    )

    class Meta:
        model = Case
        fields = []


class DocumentForm(forms.ModelForm):
    forms = MultiSelectFormField(
        label=_('Formulieren'),
        help_text=_('Als er formulieren zijn waar deze bijlage aan toegevoegd moet worden, dan kun je die hier aanvinken'),
        choices=FORMS_PROCESSTAP_CHOICES,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['uploaded_file'].label = "Selecteer een bestand"
        self.fields['name'].label = "Titel van de bijlage"

    class Meta:
        model = Document
        exclude = (
            'case',
        )
        widgets = {
            'uploaded_file': forms.FileInput(attrs={'id': 'file-upload', 'required': 'required'}),
        }


class CaseDeleteRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['delete_request_message'].label = "Waarom wil je deze cliënt verwijderen?"

    class Meta:
        model = Case
        fields = [
            'delete_request_message',
        ]
        widgets={
            'delete_request_message': forms.Textarea(
            attrs={
                'rows': 4,
            }
        )}

class CaseDeleteRequestRevokeForm(forms.ModelForm):
    delete_request_revoke_message = forms.Textarea(
        label=_('E-mailadres woningcorporatie'),
        help_text="Verstuur het bericht ook naar de woningcorporatie door hier een e-mailadres in te vullen",
        required=False
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['delete_request_message'].label = "Waarom wil je deze cliënt verwijderen?"

    class Meta:
        model = Case
        fields = [
            'delete_request_message',
        ]
        widgets={
            'delete_request_message': forms.Textarea(
            attrs={
                'rows': 4,
            }
        )}


