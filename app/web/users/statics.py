REDACTIE = 1
BEGELEIDER = 5
BEHEERDER = 7
PB_FEDERATIE_BEHEERDER = 9
FEDERATIE_BEHEERDER = 8
ONBEKEND = 6
WONEN = 2
WONINGCORPORATIE_MEDEWERKER = 4

USER_TYPES = (
    (REDACTIE, 'Redactie'),
    (WONEN, 'Wonen medewerker'),
    (3, 'GGD'),
    (WONINGCORPORATIE_MEDEWERKER, 'Woningcorporatie medewerker'),
    (BEGELEIDER, 'Persoonlijk begeleider'),
    (ONBEKEND, 'Onbekend'),
    (BEHEERDER, 'Beheerder'),
    (FEDERATIE_BEHEERDER, 'Organisatie beheerder'),
    (PB_FEDERATIE_BEHEERDER, 'PB & Organisatie beheerder'),
)
USER_TYPES_DICT = dict((ut[0], ut[1]) for ut in USER_TYPES)

USER_TYPES_ACTIVE = [6, 1, 5, 4, 7, 2, 8, 9]
USER_TYPES_FEDERATIE = [6, 8]
