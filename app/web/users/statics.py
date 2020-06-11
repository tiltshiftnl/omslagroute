USER_TYPES = (
    (1, 'Redactie'),
    (2, 'Wonen medewerker'),
    (3, 'GGD'),
    (4, 'Woningcorporatie'),
    (5, 'Persoonlijk begeleider'),
    (6, 'Onbekend'),
    (7, 'Gebruikers beheerder'),
    (8, 'Organisatie beheerder'),
)
USER_TYPES_DICT = dict((ut[0], ut[1]) for ut in USER_TYPES)

USER_TYPES_ACTIVE = [6, 1, 5, 7, 2, 8]
USER_TYPES_FEDERATIE = [6, 5, 8]

REDACTIE = 1
BEGELEIDER = 5
GEBRUIKERS_BEHEERDER = 7
FEDERATIE_BEHEERDER = 8
ONBEKEND = 6
WONEN = 2
