from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import widgets
from .utils import birth_dates_years


FIELDS = (
    ('naam_client', forms.CharField(
        label=_('Naam cliënt'),
        help_text=_('Voor- en achternaam'),
        required=True
    )),
    ('geslacht', forms.ChoiceField(
        label=_('Geslacht'),
        required=True,
        widget=forms.RadioSelect(),
        choices=(
            ('vrouw', 'Vrouw'),
            ('man', 'Man'),
        ),
    )),
    ('geboortedatum', forms.DateField(
        label=_('Geboortedatum'),
        required=True,
        widget=widgets.SelectDateWidget(
            years=birth_dates_years(),
        ),
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
        'description': 'Omscrhrijving persoonsgegevens',
        'section_list': [
            {
                'title': 'Basisgegevens',
                'description': 'Omscrhrijving basisgegevens',
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
        'description': 'Wat is de woonsituatie van de cliënt',
        'section_list': [
            {
                'title': 'Woningnet',
                'description': 'Inschrijfgegevens van woningnet',
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
        'description': 'Omscrhrijving persoonsgegevens',
        'section_list': [
            {
                'title': 'Basisgegevens',
                'description': 'Omscrhrijving basisgegevens',
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

