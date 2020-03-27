from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import widgets
from .utils import birth_dates_years
from .widgets import RadioSelect
from web.cases.statics import GESLACHT


FIELDS = (
    ('naam_client', forms.CharField(
        label=_('Naam cliënt'),
        help_text=_('Voor- en achternaam'),
        required=True
    )),
    ('client_first_name', forms.CharField(
        label=_('Naam cliënt'),
        help_text=_('Voor- en achternaam'),
        required=True
    )),
    ('client_last_name', forms.CharField(
        label=_('Naam cliënt'),
        help_text=_('Voor- en achternaam'),
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
        required=True,
    )),
    ('email', forms.EmailField(
        label=_('E-mailadres'),
        required=True,
    )),
    ('woningnetnummer', forms.IntegerField(
        label=_('Woningnetnummer'),
        required=True,
    )),
    ('woonsituatie', forms.CharField(
        label=_('Woonsituatie'),
        help_text=_('Geef in het kort aan wat de huidige woonsituatie is'),
        required=True,
        widget=forms.Textarea(),
    )),
)

FIELDS_DICT = dict((f[0], f[1]) for f in FIELDS)

URGENTIE_AANVRAAG = [
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
    {
        'title': 'Woonsituatie',
        'description': 'Informatie over de woonsituatie van uw cliënt.',
        'section_list': [
            {
                'title': 'Woningnet',
                'description': 'De inschrijfgegevens van de cliënt in woningnet.',
                'fields': [
                    'woningnetnummer',
                ],
            },
            {
                'title': 'Huidige woonsituatie',
                'description': '',
                'fields': [
                    'woonsituatie',
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

