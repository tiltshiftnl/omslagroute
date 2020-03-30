from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import widgets
from .utils import birth_dates_years
from .widgets import *
from web.cases.statics import *


FIELDS = (
    ('naam_client', forms.CharField(
        label=_('Naam cliënt'),
        required=True
    )),
    ('client_first_name', forms.CharField(
        label=_('Voornaam'),
        required=True
    )),
    ('client_last_name', forms.CharField(
        label=_('Achternaam'),
        required=True
    )),
    ('geslacht', forms.ChoiceField(
        label=_('Geslacht'),
        required=True,
        widget=RadioSelect(),
        choices=GESLACHT,
    )),
    ('geboortedatum', forms.DateField(
        label=_('Geboortedatum'),
        required=True,
        widget=widgets.SelectDateWidget(
            years=birth_dates_years(),
        ),
    )),
    ('emailadres', forms.EmailField(
        label=_('E-mailadres'),
        required=False,
    )),
    ('email', forms.EmailField(
        label=_('E-mailadres'),
        required=True,
    )),
    ('woningnet_nummer', forms.CharField(
        label=_('Woningnetnummer'),
        required=True,
    )),
    ('woningnet_geldigheid', forms.DateField(
        label=_('Geldigheid woninget'),
        widget=widgets.SelectDateWidget(
            years=birth_dates_years(),
        ),
        required=True,
    )),
    ('centrale_toegang_naam', forms.ChoiceField(
        label=_('Naam centrale toegang'),
        widget=RadioSelect(),
        choices=CENTRALE_TOEGANG,
        required=True,
    )),
    ('jonger_dan_26', forms.ChoiceField(
        label=_('Plaatsing jonger dan 26 jaar'),
        choices=JONGER_DAN_26,
        widget=RadioSelect(),
        required=True,
    )),
    ('jonger_dan_26_plaatsing_project', forms.CharField(
        label=_('Plaatsing jonger project'),
        widget=forms.Textarea(),
        required=False,
    )),
    ('jonger_dan_26_motivatie_contract_onbepaalde', forms.CharField(
        label=_('Motivatie voor contract onbepaalde tijd jongere'),
        widget=forms.Textarea(),
        required=False,
    )),
    ('partner_naam', forms.CharField(
        label=_('Partner naam'),
        required=True,
    )),
    ('partner_geboortedatum', forms.DateField(
        label=_('Partner geboortedatum'),
        widget=widgets.SelectDateWidget(
            years=birth_dates_years(),
        ),
        required=True,
    )),
    ('partner_gehuwd', forms.BooleanField(
        label=_('Gehuwd?'),
        required=False,
    )),
    ('partner_echtscheiding_rond', forms.BooleanField(
        label=_('Echtscheiding rond?'),
        required=False,
    )),
    ('partner_woonsituatie', forms.CharField(
        label=_('Woonsituatie partner'),
        widget=forms.Textarea(),
        required=True,
    )),
    ('centrale_toegang_trajectwijziging_ed', forms.ChoiceField(
        label=_('Toegang en trajectwijziging / doorstroom en jeugdzorg'),
        choices=CENTRALE_TOEGANG,
        widget=RadioSelect(),
        required=True,
    )),
    ('trajecthouder_naam', forms.CharField(
        label=_('Naam instroomfunctionaris of trajecthouder'),
        required=True,
    )),
    ('aanvraag_datum', forms.DateField(
        label=_('Datum aanvraag'),
        widget=widgets.SelectDateWidget(
            years=birth_dates_years(),
        ),
        required=True,
    )),
    ('omslagwoning_zorgaanbieder', forms.CharField(
        label=_('Zorgaanbieder omslagwoning'),
        required=True,
    )),
    ('urgentiecriteria_zinvolle_dagbesteding', forms.CharField(
        label=_('De cliënt heeft passende zinvolle dagbesteding'),
        widget=forms.Textarea(),
        required=True,
    )),
    ('urgentiecriteria_functioneert_sociaal_stabiel', forms.CharField(
        label=_('De cliënt functioneert sociaal stabiel'),
        widget=forms.Textarea(),
        required=True,
    )),
    ('urgentiecriteria_functioneert_psychisch_stabiel', forms.CharField(
        label=_('De cliënt functioneert psychisch stabiel'),
        widget=forms.Textarea(),
        required=True,
    )),
    ('urgentiecriteria_is_financieel_stabiel', forms.CharField(
        label=_('De cliënt is financieel stabiel'),
        widget=forms.Textarea(),
        required=True,
    )),
    ('urgentiecriteria_kinderen_gezonde_omgeving', forms.CharField(
        label=_('De betrokken kinderen hebben een gezonde omgeving'),
        widget=forms.Textarea(),
        required=True,
    )),
    ('medische_problemen_mbt_traplopen', forms.BooleanField(
        label=_('Zijn er medische problemen m.b.t. traplopen?'),
        required=False,
    )),
    ('medische_problemen_wooneisen', forms.CharField(
        label=_('Zo ja, benedenwoning of woning met lift? Anders?'),
        widget=forms.Textarea(),
        required=False,
    )),
    ('medische_problemen_bewijslast', forms.FileField(
        label=_('Voeg medische gegevens toe m.b.t. problematiek'),
        required=False,
    )),
    ('uitsluiting_stadsdeel_argumentatie', forms.CharField(
        label=_('Uitsluiting stadsdeel, argumentatie'),
        widget=forms.Textarea(),
        required=False,
    )),
)

FIELDS_DICT = dict((f[0], f[1]) for f in FIELDS)

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
                    'woningnet_nummer',
                    'woningnet_geldigheid',
                    'centrale_toegang_naam',
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
                    'partner_geboortedatum',
                    'partner_gehuwd',
                    'partner_echtscheiding_rond',
                    'partner_woonsituatie',
                ],
            },

        ]
    },
    {
        'title': '',
        'description': '',
        'section_list': [
            {
                'title': '',
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

