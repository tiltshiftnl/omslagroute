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
CASE_STATUS = (
    (1, 'ingediend', 'indienen'),
    (2, 'afgekeurd', 'afkeuren'),
    (3, 'goedgekeurd', 'goedkeuren'),
    (4, 'in behandeling', 'in behandeling'),
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

CASE_STATUS_INGEDIEND = 1
CASE_STATUS_AFGEKEURD = 2
CASE_STATUS_GOEDGEKEURD = 3
CASE_STATUS_IN_BEHANDELING = 4

GESLACHT_DICT = dict((s[0], s[1]) for s in GESLACHT)
CENTRALE_TOEGANG_DICT = dict((s[0], s[1]) for s in CENTRALE_TOEGANG)
JONGER_DAN_26_DICT = dict((s[0], s[1]) for s in JONGER_DAN_26)
DEFAULT_YES_OR_NO_DICT = dict((s[0], s[1]) for s in DEFAULT_YES_OR_NO)
DEFAULT_NO_OR_YES_DICT = dict((s[0], s[1]) for s in DEFAULT_NO_OR_YES)
