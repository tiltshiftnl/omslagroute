from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import widgets
from .utils import *
from .widgets import *
from web.cases.statics import *


FIELDS = (
    ('client_first_name', forms.CharField(
        label=_('Voornaam'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=True
    ), {'step_required': True}),
    ('client_last_name', forms.CharField(
        label=_('Achternaam'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=True
    ), {'step_required': True}),
    ('geslacht', forms.ChoiceField(
        label=_('Geslacht'),
        required=False,
        widget=RadioSelect(),
        choices=GESLACHT,
    ), {}),
    ('geboortedatum', forms.DateField(
        label=_('Geboortedatum'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
    ), {}),
    ('emailadres', forms.EmailField(
        label=_('E-mailadres'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False,
    ), {}),
    ('woningnet_nummer', forms.CharField(
        label=_('Woningnetnummer'),
        widget=forms.TextInput(attrs={'placeholder': ' ', 'pattern': '^[0-9]*$'}),
        required=False,
    ), {'step_required': True}),
    ('woningnet_geldigheid', forms.DateField(
        label=_('Geldigheid woninget'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        required=False,
        help_text=_('Tot wanneer is de inschrijving bij Woningnet geldig?')
    ), {'step_required': True}),
    ('centrale_toegang_naam', forms.IntegerField(
        label=_('Naam centrale toegang'),
        widget=RadioSelect(
            choices=CENTRALE_TOEGANG,
        ),
        required=False,
    ), {'step_required': True}),
    ('jonger_dan_26', forms.IntegerField(
        label=_('Plaatsing jonger dan 26 jaar'),
        widget=RadioSelect(
            choices=JONGER_DAN_26,
        ),
        required=False,
    ), {'step_required': True}),
    ('jonger_dan_26_plaatsing_project', forms.CharField(
        label=_('In geval van plaatsing in een project'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        required=False,
    ), {}),
    ('jonger_dan_26_motivatie_contract_onbepaalde', forms.CharField(
        label=_('Motivatie voor contract onbepaalde tijd jongere'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        required=False,
        help_text='Wat is de motivatie voor aanvraag van een huurcontract voor onbepaalde tijd?'
    ), {'step_required': True}),
    ('partner_naam', forms.CharField(
        label=_('Naam partner'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False,
    ), {}),
    ('partner_geboortedatum', forms.DateField(
        label=_('Geboortedatum partner'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        required=False,
    ), {}),
    ('partner_gehuwd', forms.BooleanField(
        label=_('Gehuwd'),
        required=False,
    ), {}),
    ('partner_echtscheiding_rond', forms.BooleanField(
        label=_('Echtscheiding rond'),
        required=False,
    ), {}),
    ('partner_woonsituatie', forms.CharField(
        label=_('Woonsituatie partner'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
        help_text='Waar/bij wie/hoe?'
    ), {}),
    ('kinderen', forms.CharField(
        label=_('Kinderen'),
        help_text=_('Geef aan per kind: <ul><li>Naam + voorletters</li><li>Geboortedatum (dag-maand-jaar)</li><li>Ouderlijk gezag (ja of nee)</li><li>Mee aangemeld (ja of nee)</li></ul>'),
        widget=forms.Textarea(),
        required=False,
    ), {}),
    ('centrale_toegang_trajectwijziging_ed', forms.IntegerField(
        label=_('Toegang en trajectwijziging / doorstroom en jeugdzorg'),
        widget=RadioSelect(
            choices=CENTRALE_TOEGANG,
        ),
        required=False,
    ), {}),
    ('trajecthouder_naam', forms.CharField(
        label=_('Naam instroomfunctionaris of trajecthouder'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False,
    ), {}),
    ('aanvraag_datum', forms.DateField(
        label=_('Datum aanvraag'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        required=False,
    ), {}),
    ('omslagwoning_zorgaanbieder', forms.CharField(
        label=_('Zorgaanbieder omslagwoning'),
        widget=forms.TextInput(attrs={'placeholder': ' '}),
        required=False,
    ), {}),
    ('urgentiecriteria_zinvolle_dagbesteding', forms.CharField(
        label=_('De cliënt heeft passende zinvolle dagbesteding. Dat betekent voor deze cliënt het volgende:'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        required=False,
        help_text='Bijvoorbeeld: cliënt wil een betaalde baan die zij kan combineren met de zorg voor haar kinderen',
    ), {}),
    ('urgentiecriteria_functioneert_sociaal_stabiel', forms.CharField(
        label=_('De cliënt functioneert sociaal stabiel. Dat betekent voor deze cliënt het volgende:'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        required=False,
        help_text='Bijvoorbeeld: Het doel is om het huidige netwerk te behouden en het contact met haar ex-man te stabiliseren.',
    ), {}),
    ('urgentiecriteria_functioneert_psychisch_stabiel', forms.CharField(
        label=_('De cliënt functioneert psychisch stabiel. Dat betekent voor deze cliënt het volgende:'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        required=False,
        help_text='Bijvoorbeeld: cliënt functioneert psychisch stabiel en heeft als doel dit voort te zetten. <br /><strong>Let op! Leg geen medische informatie vast.</strong>',
    ), {}),
    ('urgentiecriteria_is_financieel_stabiel', forms.CharField(
        label=_('De cliënt is financieel stabiel. Dat betekent voor deze cliënt het volgende:'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        required=False,
        help_text='Met financieel stabiel wordt bedoeld dat deze een stabiel inkomen heeft inzage heeft gegeven in eventuele schulden op basis van informatie van Bureau KredietRegistratie.<br /><br />In het geval er schulden zijn is de cliënt financieel stabiel wanneer de cliënt aan een of meerdere van deze zaken voldoet: <ul><li>een overzicht heeft gegeven van alle schulden en betalingsverplichtingen</li><li>inzicht heeft gegeven in eventuele openstaande CJIB-boetes en heeft aangetoond dat er geen kans is op detentie vanwege openstaande boetes</li><li>in inkomensbeheer zit</li><li>een stabiel werkend budgetplan heeft</li><li>een overeenkomst heeft met een schuldhulpverleningsbureau waarbij het schuldhulpverleningstraject voorspoedig loopt</li></ul>Bijvoorbeeld: cliënt wil zelfstandig haar administratie bijhouden en haar schulden regelen.',
    ), {}),
    ('urgentiecriteria_kinderen_gezonde_omgeving', forms.CharField(
        label=_('De betrokken kinderen hebben een gezonde omgeving. Dat betekent voor deze cliënt het volgende:'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        required=False,
        help_text='De betrokken kinderen hebben een gezonde omgeving, waarmee wordt bedoeld dat deze:<ul><li>Een veilige omgeving hebben waarin zij opgroeien; en</li><li>Zich leeftijdsadequaat kunnen ontwikkelen; en</li><li>Een omgeving hebben waarin voldoende emotioneel en fysiek beschikbare opvoeder(s) zijn</li></ul>',
    ), {}),
    ('medische_problemen_mbt_traplopen', forms.BooleanField(
        label=_('Zijn er medische problemen met betrekking tot traplopen?'),
        required=False,
        help_text='',
    ), {}),
    ('medische_problemen_wooneisen', forms.CharField(
        label=_('Zo ja, benedenwoning of woning met lift? Anders?'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {}),
    ('medische_problemen_bewijslast', forms.FileField(
        label=_('Voeg medische gegevens toe met betrekking tot problematiek'),
        widget=ClearableFileInput(),
        required=False,
    ), {}),
    ('uitsluiting_stadsdeel_argumentatie', forms.CharField(
        label=_('Uitsluiting stadsdeel, argumentatie'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {}),
)

FIELDS_DICT = dict((f[0], f[1]) for f in FIELDS)
FIELDS_REQUIRED_DICT = dict((f[0], f[2].get('step_required', False)) for f in FIELDS)

BASIS_GEGEVENS = [
    {
        'title': '',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'client_first_name',
                    'client_last_name',
                    'geboortedatum',
                    'emailadres',
                ],
            },
        ]
    },
]

URGENTIE_AANVRAAG = [
    {
        'title': 'Persoonsgegevens',
        'description': 'In deze stap vult u eenmalig informatie over uw cliënt in. Deze informatie wordt in uw browser opgeslagen zodat u na invullen op een later moment van deze informatie gebruik kunt maken.',
        'section_list': [
            {
                'title': 'Basisgegevens',
                'description': 'Controleer deze gegevens eventueel samen met uw cliënt!',
                'fields': [
                    'client_first_name',
                    'client_last_name',
                    'geboortedatum',
                    'centrale_toegang_naam',
                ],
            },
            {
                'title': 'Woningnet',
                'description': '',
                'fields': [
                    'woningnet_nummer',
                    'woningnet_geldigheid',
                ],
            },
            {
                'title': 'Jonger dan 26 jaar?',
                'description': '',
                'fields': [
                    'jonger_dan_26',
                    'jonger_dan_26_plaatsing_project',
                    'jonger_dan_26_motivatie_contract_onbepaalde',
                ],
            },
            {
                'title': 'Gezinssamenstelling',
                'description': '',
                'fields': [
                    'partner_naam',
                    'partner_geboortedatum',
                    'partner_gehuwd',
                    'partner_echtscheiding_rond',
                    'partner_woonsituatie',
                    'kinderen',
                ],
            },

        ]
    },
    {
        'title': '',
        'description': '',
        'section_list': [
            {
                'title': 'Toegang',
                'description': '',
                'fields': [
                    'centrale_toegang_trajectwijziging_ed',
                    'trajecthouder_naam',
                    'aanvraag_datum',
                    'omslagwoning_zorgaanbieder',
                ],
            },
            {
                'title': 'Urgentiecriteria in de huisvestingsverordening',
                'description': '',
                'fields': [
                    'urgentiecriteria_zinvolle_dagbesteding',
                    'urgentiecriteria_functioneert_sociaal_stabiel',
                    'urgentiecriteria_functioneert_psychisch_stabiel',
                    'urgentiecriteria_is_financieel_stabiel',
                ],
            },
            {
                'title': 'Indien er kinderen gebruik maken van de opvang',
                'description': 'NB: Voor de toewijzing van een woning is de juiste samenstelling van het huishouden in WoningNet relevant. let hierop bij kinderen!',
                'fields': [
                    'urgentiecriteria_kinderen_gezonde_omgeving',
                ],
            },
            {
                'title': 'Toelichting Wooneisen',
                'description': '',
                'fields': [
                    'medische_problemen_mbt_traplopen',
                    'medische_problemen_wooneisen',
                    'medische_problemen_bewijslast',
                    'uitsluiting_stadsdeel_argumentatie',
                ],
            },

        ]
    },
]

AANVRAAG_VERLENGING_TRACJECTWIJZIGING_MOBW = [
    {
        'title': 'Persoonsgegevens',
        'description': 'In deze stap vult u eenmalig informatie over uw cliënt in. Deze informatie wordt in uw browser opgeslagen zodat u na invullen op een later moment van deze informatie gebruik kunt maken.',
        'section_list': [
            {
                'title': 'Basisgegevens',
                'description': 'Controleer deze gegevens eventueel samen met uw cliënt!',
                'fields': [
                    'naam_client',
                    'geslacht',
                    'geboortedatum',
                ],
            },
            {
                'title': 'Contactgegevens',
                'description': '',
                'fields': [
                    'email',
                ],
            },

        ]
    },
]

SECTIONS = (
    ('basis_gegevens', BASIS_GEGEVENS),
    ('urgentie_aanvraag', URGENTIE_AANVRAAG),
)
SECTIONS_DICT = dict((s[0], s[1]) for s in SECTIONS)

