import json

GESLACHT = (
    (1, 'Man'),
    (2, 'Vrouw'),
    (3, 'Overig'),
)

CENTRALE_TOEGANG = (
    (1, 'CTBW (Centrale Toegang Begeleid Wonen)'),
    (2, 'CTMO (Centrale Toegang Maatschappelijke Opvang)'),
    (3, 'CTMOJ (Centrale Toegang Maatschappelijke Opvang Jeugd)'),
    (4, 'CTMOG (Centrale Toegang Maatschappelijke Opvang Gezin)'),
    (5, 'Jeugdhulp'),
    (6, 'CTBWLvB (Centrale Toegang Begeleid Wonen Licht Verstandelijke Beperking)'),
)

JONGER_DAN_26 = (
    (1, 'Nee'),
    (2, 'Ja: standaard plaatsing jongerenwoning (5 jaar contract bij omklap)'),
    (3, 'Ja: plaatsing reguliere woning noodzakelijk (onbepaalde tijd bij omklap)'),
    (4, 'Ja: Plaatsing in een project (Licht dit toe bij de volgende vraag)'),
)

DEFAULT_YES_OR_NO = (
    (1, 'Ja'),
    (2, 'Nee'),
)
DEFAULT_NO_OR_YES = (
    (2, 'Nee'),
    (1, 'Ja'),
)

GESLACHT_DICT = dict((s[0], s[1]) for s in GESLACHT)
CENTRALE_TOEGANG_DICT = dict((s[0], s[1]) for s in CENTRALE_TOEGANG)
JONGER_DAN_26_DICT = dict((s[0], s[1]) for s in JONGER_DAN_26)
DEFAULT_YES_OR_NO_DICT = dict((s[0], s[1]) for s in DEFAULT_YES_OR_NO)
DEFAULT_NO_OR_YES_DICT = dict((s[0], s[1]) for s in DEFAULT_NO_OR_YES)





# case status 
CASE_STATUS_INGEDIEND = 1
CASE_STATUS_AFGEKEURD = 2
CASE_STATUS_GOEDGEKEURD = 3
CASE_STATUS_IN_BEHANDELING = 4

CASE_STATUS = (
    (CASE_STATUS_INGEDIEND, 'ingediend', 'indienen'),
    (CASE_STATUS_AFGEKEURD, 'afgekeurd', 'afkeuren'),
    (CASE_STATUS_GOEDGEKEURD, 'goedgekeurd', 'goedkeuren'),
    (CASE_STATUS_IN_BEHANDELING, 'in behandeling', 'in behandeling'),
)

def map_case_status_keys(f):
    return {
        'id': f[0],
        'current': f[1],
        'verb': f[2],
    }

CASE_STATUS_CHOICES = list((s[0], s[1]) for s in CASE_STATUS)
CASE_STATUS_DICT = dict((s[0], map_case_status_keys(s)) for s in CASE_STATUS)
CASE_STATUS_DICT_JSON = json.dumps(CASE_STATUS_DICT)






# case version
CASE_VERSION_BASE = 'basis-gegevens'
CASE_VERSION_ADDRESS = 'adres-aanpassen'
CASE_VERSION_FORM_URGENTIE = 'aanvraag-omslag-en-urgentie'
CASE_VERSION_FORM_OMKLAP = 'aanvraag-omslag-en-urgentie'

CASE_VERSION = (
    (CASE_VERSION_BASE, 'Basis gegevens'),
    (CASE_VERSION_ADDRESS, 'Adres gegevens'),
    (CASE_VERSION_FORM_URGENTIE, 'Aanvraag Urgentie onder voorwaarden'),
    (CASE_VERSION_FORM_OMKLAP, 'Aanvraag Voordracht omklap'),
)

def map_case_version_keys(f):
    return {
        'slug': f[0],
        'title': f[1],
    }

CASE_VERSION_BY_SLUG = dict((s[0], map_case_version_keys(s)) for s in CASE_VERSION)
