

GESLACHT = (
    (1, 'Man'),
    (2, 'Vrouw'),
    (3, 'Overig'),
)

CENTRALE_TOEGANG = (
    (1, 'CTBW'),
    (2, 'CTMO'),
    (3, 'CTMOJ'),
    (4, 'CTMOG'),
    (5, 'JEUGDHULP'),
    (6, 'CTBWLvB'),
)

JONGER_DAN_26 = (
    (1, 'Nee'),
    (2, 'Ja: standaard plaatsing jongerenwoning (5 jaar contract bij omklap)'),
    (3, 'Ja: plaatsing reguliere woning noodzakelijk (onbepaalde tijd bij omklap)'),
    (4, 'Ja: Plaatsing in een project: ……………………………'),
)

DEFAULT_YES_OR_NO = (
    (1, 'Ja'),
    (2, 'Nee'),
)

GESLACHT_DICT = dict((s[0], s[1]) for s in GESLACHT)
CENTRALE_TOEGANG_DICT = dict((s[0], s[1]) for s in CENTRALE_TOEGANG)
JONGER_DAN_26_DICT = dict((s[0], s[1]) for s in JONGER_DAN_26)
DEFAULT_YES_OR_NO_DICT = dict((s[0], s[1]) for s in DEFAULT_YES_OR_NO)
