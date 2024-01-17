from classes import (
    Import,
    FromImport,
    get_import_or_line,
)
from configurable import (
    ADD_NEWLINES_AFTER,
    get_value,
)


Section = list[Import | FromImport | str]

MAX_NON_IMPORT_CUTOFF: int = 8


def sort_section(section: list[Import | FromImport]) -> None:
    values: dict[Import | FromImport, int] = {
        item: get_value(item)
        for item in section
    }
    section.sort(key=lambda item: (
        values[item],
        item.name,
    ))
    last_value: int = values[section[-1]]
    for i in range(len(section) - 1, -1, -1):
        current = section[i]
        value = values[current]
        if value == last_value:
            continue
        last_value = value
        if ADD_NEWLINES_AFTER.get(value, False):
            section.insert(i + 1, '')  # type: ignore
            continue


def sort_imports(raw: str) -> str:
    sections: list[Section] = []
    current_section: Section = []
    before_remove_line = raw
    most_recent_raw = raw
    after_append_raw = raw
    while (
        len(current_section) == 0
        or (
            len(current_section) <= MAX_NON_IMPORT_CUTOFF
            if isinstance(current_section[0], str)
            else True
        )
    ):
        before_remove_line = most_recent_raw
        result, most_recent_raw = get_import_or_line(most_recent_raw)
        if isinstance(result, str):
            result = result.rstrip(' ')
        if len(current_section) == 0:
            current_section.append(result)
            continue
        if result != '' and ((
            isinstance(current_section[0], str)
            and not isinstance(result, str)
        ) or (
            not isinstance(current_section[0], str)
            and isinstance(result, str)
        )):
            sections.append(current_section)
            current_section = [result]
            after_append_raw = before_remove_line
            continue
        current_section.append(result)
    if len(current_section) > 0 and not all(
        isinstance(item, str)
        for item in current_section
    ):
        sections.append(current_section)
        after_append_raw = before_remove_line

    if len(sections) == 0:
        return raw

    for i in range(len(sections)):
        section = sections[i]
        if all(
            isinstance(item, str)
            for item in section
        ):
            continue
        if section[-1] == '':
            section.pop()
            if i + 1 < len(sections):
                next_section = sections[i + 1]
                next_section.insert(0, '')
        if section[0] == '':
            section.pop(0)
            if i - 1 >= 0:
                prev_section = sections[i - 1]
                prev_section.append('')

    for section in sections:
        if all(
            isinstance(item, str)
            for item in section
        ):
            continue
        for i in range(len(section) - 1, -1, -1):
            item = section[i]
            if isinstance(item, str):
                assert item == ''
                section.pop(i)
        sort_section(section)  # type: ignore

    while sections[0][0] == '':
        sections[0].pop(0)
    while sections[-1][-1] == '':
        sections[-1].pop()
    if not after_append_raw.startswith(' '):
        after_append_raw = '\n\n' + after_append_raw.lstrip('\n')

    return '\n'.join(
        '\n'.join(str(item) for item in section)
        for section in sections
    ) + '\n' + after_append_raw
