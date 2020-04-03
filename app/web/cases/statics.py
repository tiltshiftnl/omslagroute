

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

GESLACHT_DICT = dict((s[0], s[1]) for s in GESLACHT)
CENTRALE_TOEGANG_DICT = dict((s[0], s[1]) for s in CENTRALE_TOEGANG)
JONGER_DAN_26_DICT = dict((s[0], s[1]) for s in JONGER_DAN_26)
DEFAULT_YES_OR_NO_DICT = dict((s[0], s[1]) for s in DEFAULT_YES_OR_NO)
