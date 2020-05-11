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
        localize=True,
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
        localize=True,
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
        localize=True,
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
        localize=True,
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
    ('organisatie', forms.CharField(
        label=_('Organisatie'),
        required=False,
    ), {'step_required': True}),
    ('persoonlijk_begeleider', forms.CharField(
        label=_('Persoonlijk begeleider'),
        required=False,
    ), {'step_required': True}),
    ('start_zelfstandig_wonen', forms.CharField(
        label=_('Start zelfstandig wonen (intermediair)'),
        required=False,
    ), {'step_required': True}),
    ('datum_voordracht', forms.DateField(
        label=_('Datum voordracht'),
        required=False,
    ), {'step_required': True}),
    ('woningcorporatie_akkoord_met_omklap', forms.IntegerField(
        label=_('Woningcorporatie akkoord met omklap'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('datum_evaluatie_moment', forms.DateField(
        label=_('Datum evaluatie moment'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        localize=True,
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_zinvolle_dagbesteding_behaald_omdat', forms.CharField(
        label=_('Deze doelen zijn behaald omdat'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_zinvolle_dagbesteding_beoordeeld_door', forms.CharField(
        label=_('Deze doelen zijn beoordeeld door'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_zinvolle_dagbesteding_akkoord', forms.IntegerField(
        label=_('Akkoord'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_zinvolle_dagbesteding_datum_evaluatiemoment', forms.DateField(
        label=_('Datum evaluatiemoment'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        localize=True,
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_sociaal_behaald_omdat', forms.CharField(
        label=_('Deze doelen zijn behaald omdat'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_sociaal_beoordeeld_door', forms.CharField(
        label=_('Deze doelen zijn beoordeeld door'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_sociaal_akkoord', forms.IntegerField(
        label=_('Akkoord'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_sociaal_datum_evaluatiemoment', forms.DateField(
        label=_('Datum evaluatiemoment'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        localize=True,
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_psychisch_behaald_omdat', forms.CharField(
        label=_('Deze doelen zijn behaald omdat'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_psychisch_beoordeeld_door', forms.CharField(
        label=_('Deze doelen zijn beoordeeld door'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_psychisch_akkoord', forms.IntegerField(
        label=_('Akkoord'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_functioneert_psychisch_datum_evaluatiemoment', forms.DateField(
        label=_('Datum evaluatiemoment'),
         widget=forms.TextInput(
             attrs={
                 'placeholder': 'dd-mm-jjjj',
             }
         ),
         localize=True,
         required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_is_financieel_stabiel_behaald_omdat', forms.CharField(
        label=_('Deze doelen zijn behaald omdat'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_is_financieel_stabiel_beoordeeld_door', forms.CharField(
        label=_('Deze doelen zijn beoordeeld door'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_is_financieel_stabiel_akkoord', forms.IntegerField(
        label=_('Akkoord'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_is_financieel_stabiel_datum_evaluatiemoment', forms.DateField(
        label=_('Datum evaluatiemoment'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        localize=True,
        required=False,
    ), {'step_required': True}),
    ('urgentiecriteria_kinderen_gezonde_behaald_omdat', forms.CharField(
        label=_('Deze doelen zijn behaald omdat'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {}),
    ('urgentiecriteria_kinderen_gezonde_beoordeeld_door', forms.CharField(
        label=_('Deze doelen zijn beoordeeld door'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
    ), {}),
     ('urgentiecriteria_kinderen_gezonde_akkoord', forms.IntegerField(
        label=_('Akkoord'),
        widget=RadioSelect(
            choices=DEFAULT_YES_OR_NO,
        ),
        required=False,
     ), {}),
     ('urgentiecriteria_kinderen_gezonde_datum_evaluatiemoment', forms.DateField(
        label=_('Datum evaluatiemoment'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        localize=True,
        required=False,
     ), {'step_required': True}),
     ('omklap_client_openstaande_vragen', forms.CharField(
        label=_('Voor deze cliënt staan de volgende vragen nog open'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
     ), {}),
     ('omklap_client_volgende_stappen_gezet', forms.CharField(
        label=_('Hiervoor worden de volgende stappen gezet (zowel formeel als informeel)'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        required=False,
     ), {}),
     ('omklap_beoordeeld_door', forms.CharField(
        label=_('Dit is beoordeeld door'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
             required = False,
    ), {'step_required': True}),
    ('omklap_datum_evaluatiemoment', forms.DateField(
        label=_('Datum evaluatiemoment'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        localize=True,
        required=False,
    ), {}),
    ('omklap_toelichting', forms.CharField(
        label=_('Toelichting'),
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15, 'placeholder': ' '}),
        help_text='Bijvoorbeeld: doelen niet behaald maar geen risico voor zelfstandig wonen',
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
        'title': 'Aanvraag',
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

OMKLAP_AANVRAAG = [
    {
        'title': 'Basisgegevens',
        'description': '',
        'section_list': [
            {
                'title': 'Persoonsgegevens',
                'description': 'Controleer deze gegevens eventueel samen met uw cliënt!',
                'fields': [
                    'client_first_name',
                    'client_last_name',
                    'geboortedatum',
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
                'title': '',
                'description': '',
                'fields': [
                    'organisatie',
                    'persoonlijk_begeleider',
                    'start_zelfstandig_wonen',
                    'datum_voordracht',
                ],
            },
        ]
    },
    {
        'title': 'Woonevaluatie gesprek',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'woningcorporatie_akkoord_met_omklap',
                    'datum_evaluatie_moment',
                ],
            },
        ]
    },
    {
        'title': 'Jonger dan 26 jaar?',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'jonger_dan_26',
                    'jonger_dan_26_plaatsing_project',
                    'jonger_dan_26_motivatie_contract_onbepaalde',
                ],
            },
        ]
    },
    {
        'title': 'Urgentiecriteria in de huisvestingsverordening',
        'description': '',
        'section_list': [
            {
                'title': 'Zinvolle dagbesteding',
                'description': '',
                'fields': [
                    'urgentiecriteria_zinvolle_dagbesteding',
                    'urgentiecriteria_zinvolle_dagbesteding_behaald_omdat',
                    'urgentiecriteria_zinvolle_dagbesteding_beoordeeld_door',
                    'urgentiecriteria_zinvolle_dagbesteding_akkoord',
                    'urgentiecriteria_zinvolle_dagbesteding_datum_evaluatiemoment',
                ],
            },
            {
                'title': 'Sociaal',
                'description': '',
                'fields': [
                    'urgentiecriteria_functioneert_sociaal_stabiel',
                    'urgentiecriteria_functioneert_sociaal_behaald_omdat',
                    'urgentiecriteria_functioneert_sociaal_beoordeeld_door',
                    'urgentiecriteria_functioneert_sociaal_akkoord',
                    'urgentiecriteria_functioneert_sociaal_datum_evaluatiemoment',
                ],
            },
            {
                'title': 'Psychisch',
                'description': '',
                'fields': [
                    'urgentiecriteria_functioneert_psychisch_stabiel',
                    'urgentiecriteria_functioneert_psychisch_behaald_omdat',
                    'urgentiecriteria_functioneert_psychisch_beoordeeld_door',
                    'urgentiecriteria_functioneert_psychisch_akkoord',
                    'urgentiecriteria_functioneert_psychisch_datum_evaluatiemoment',
                ],
            },
            {
                'title': 'Financieel',
                'description': '',
                'fields': [
                    'urgentiecriteria_is_financieel_stabiel',
                    'urgentiecriteria_is_financieel_stabiel_behaald_omdat',
                    'urgentiecriteria_is_financieel_stabiel_beoordeeld_door',
                    'urgentiecriteria_is_financieel_stabiel_akkoord',
                    'urgentiecriteria_is_financieel_stabiel_datum_evaluatiemoment',
                ],
            },
            {
                'title': 'En, indien er kinderen gebruik maken van de opvang',
                'description': '',
                'fields': [
                    'urgentiecriteria_kinderen_gezonde_omgeving',
                    'urgentiecriteria_kinderen_gezonde_behaald_omdat',
                    'urgentiecriteria_kinderen_gezonde_beoordeeld_door',
                    'urgentiecriteria_kinderen_gezonde_akkoord',
                    'urgentiecriteria_kinderen_gezonde_datum_evaluatiemoment',
                ],
            },
        ]
    },
    {
        'title': 'Afspraken na de omklap',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'omklap_client_openstaande_vragen',
                    'omklap_client_volgende_stappen_gezet',
                    'omklap_beoordeeld_door',
                    'omklap_datum_evaluatiemoment',
                ],
            }
        ],
    },
    {
        'title': 'Toelichting',
        'description': '',
        'section_list': [
            {
                'title': '',
                'description': '',
                'fields': [
                    'omklap_toelichting',
                ],
            }
        ],
    },
]

FORMS = (
    (
        'basis_gegevens',
        BASIS_GEGEVENS,
        'basis-gegevens',
        'Basisgegevens cliënt',
        'Nieuwe cliënt',
        False,
        False,
    ),
    (
        'urgentie_aanvraag',
        URGENTIE_AANVRAAG,
        'aanvraag-omslag-en-urgentie',
        'Aanvraag omslag en urgentie',
        'Nieuwe aanvraag omslag en urgentie',
        True,
        True,
    ),
    (
        'omklap_aanvraag',
        OMKLAP_AANVRAAG,
        'aanvraag-omklap',
        'Aanvraag omklap',
        'Nieuwe aanvraag omklap',
        True,
        True,
    ),
)


def map_form_keys(f):
    return {
        'key': f[0],
        'sections': f[1],
        'slug': f[2],
        'title': f[3],
        'title_new': f[4],
        'inpage_navigation': f[5],
        'share': f[6],
    }


FORMS_BY_KEY = dict((s[0], map_form_keys(s)) for s in FORMS)
FORMS_BY_SLUG = dict((s[2], map_form_keys(s)) for s in FORMS)
FORMS_CHOICES = [[s[2], s[3]] for s in FORMS]



