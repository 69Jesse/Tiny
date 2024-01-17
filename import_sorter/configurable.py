from classes import (
    Import,
    FromImport,
)


ADD_NEWLINES_AFTER: dict[int, bool] = {
    0: False,
    1: True,
    2: True,
    3: True,
    4: True,
    5: True,
    6: False,
    100: False,
    101: False,
    102: False,
    103: False,
    104: False,
    105: False,
    106: False,
}


def get_value_no_type_checking(item: Import | FromImport) -> int:
    if item.name.startswith('__'):
        return 0
    if item.name.startswith('discord') or item.name.startswith('bot'):
        return 1
    if item.name == 'utils':
        return 2
    if item.name.startswith('.'):
        return 3
    if item.name in ('typing', 'types'):
        return 5
    if item.name == 'logging':
        return 6
    return 4


def get_value(item: Import | FromImport) -> int:
    value = get_value_no_type_checking(item)
    if item.type_checking:
        value += 100
    return value
