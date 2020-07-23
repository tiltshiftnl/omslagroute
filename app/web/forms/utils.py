from datetime import datetime


def birth_dates_years():
    return [y for y in range(datetime.now().year - 100, datetime.now().year)]


def future_dates_years():
    return [y for y in range(datetime.now().year + 10, datetime.now().year)]


def get_sections_fields(sections):
    sections = [] if not sections else [
        fff for f in sections for ff in f.get('section_list', []) for fff in ff.get('fields', [])
    ]
    return sections


def get_rules_reversed(form_config):
    rules = form_config.get('options', {}).get('rules', {}).items()
    return {f: [k, r.get('values', [])] for k, v in rules for r in v for f in r.get('fields', [])}
