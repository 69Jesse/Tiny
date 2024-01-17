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
    6: True,
    7: False,
    100: False,
    101: False,
    102: False,
    103: False,
    104: False,
    105: False,
    106: False,
    107: False,
}

REMOVE_NEWLINES_IN_BETWEEN: list[tuple[int, int]] = [
    (1, 2),
]



def get_value_no_type_checking(item: Import | FromImport) -> int:
    if item.name.startswith('__'):
        return 0
    if item.name.startswith('discord'):
        return 1
    if item.name.startswith('bot'):
        return 2
    if item.name.startswith('utils'):
        return 3
    if item.name.startswith('.'):
        return 4
    if item.name in ('typing', 'types', 'typing_extensions'):
        return 6
    if item.name.startswith('logging'):
        return 7
    return 5


def get_value(item: Import | FromImport) -> int:
    value = get_value_no_type_checking(item)
    if item.type_checking:
        value += 100
    return value
