from datetime import datetime


def birth_dates_years():
    return [y for y in range(datetime.now().year - 100, datetime.now().year)]


def future_dates_years():
    return [y for y in range(datetime.now().year + 10, datetime.now().year)]
