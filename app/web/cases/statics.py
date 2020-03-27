

GESLACHT = (
    (1, 'Man'),
    (2, 'Vrouw'),
    (3, 'Overig'),
)

GESLACHT_DICT = dict((s[0], s[1]) for s in GESLACHT)

URGENTIE_AANVRAAG = [
    {
        'title': 'Persoonsgegevens',
        'description': 'Omscrhrijving persoonsgegevens',
        'section_list': [
            {
                'title': 'Basisgegevens',
                'description': 'Omscrhrijving basisgegevens',
                'fields': [
                    'client_first_name',
                    'client_last_name',
                    'geslacht',
                    'geboortedatum',
                ],
            },
            {
                'title': 'Contactgegevens',
                'description': '',
                'fields': [
                    'emailadres',
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
