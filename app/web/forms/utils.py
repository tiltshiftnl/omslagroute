from datetime import datetime


def birth_dates_years():
    return [y for y in range(datetime.now().year - 100, datetime.now().year)]
