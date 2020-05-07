USER_TYPES = (
    (1, 'Redactie'),
    (2, 'Afedeling Wonen beheer'),
    (3, 'GGD'),
    (4, 'Woningcorporatie'),
    (5, 'Persoonlijk begeleider'),
    (6, 'Onbekend'),
    (7, 'Gebruikers beheerder'),
)
USER_TYPES_DICT = dict((ut[0], ut[1]) for ut in USER_TYPES)

USER_TYPES_ACTIVE = [6, 1, 5, 7]

REDACTIE = 1
BEGELEIDER = 5
GEBRUIKERS_BEHEERDER = 7
ONBEKEND = 6
