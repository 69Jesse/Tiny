import re

from typing import Optional


TAB = '    '


def add_prefix(string: str, prefix: str) -> str:
    return '\n'.join(f'{prefix}{line}' for line in string.split('\n'))


class Import:
    raw: str
    name: str
    type_checking: bool
    def __init__(
        self,
        raw: str,
        name: str,
        type_checking: bool,
    ) -> None:
        self.raw = raw
        self.name = name
        self.type_checking = type_checking

    def __str__(self) -> str:
        string = f'import {self.name}'
        if self.type_checking:
            return add_prefix(string, TAB)
        return string

    __repr__ = __str__

    @classmethod
    def from_big_raw(cls, raw: str) -> Optional[tuple['Import', str]]:
        stripped = raw.strip(' ')
        match = re.match(
            r'^import (.+)',
            stripped,
        )
        if match is None:
            return None
        name = match.group(1)
        new_raw = stripped[match.end():].split('\n', 1)[-1]
        instance = cls(
            raw=match.group(0),
            name=name,
            type_checking=raw.startswith(TAB),
        )
        return (instance, new_raw)


class FromImport:
    raw: str
    name: str
    items: list[str]
    type_checking: bool
    def __init__(
        self,
        raw: str,
        name: str,
        items: list[str],
        type_checking: bool,
    ) -> None:
        self.raw = raw
        self.name = name
        self.items = items
        self.type_checking = type_checking
        self.items.sort()
        if self.name == 'typing' and 'TYPE_CHECKING' in self.items:
            self.items.remove('TYPE_CHECKING')
            self.items.insert(0, 'TYPE_CHECKING')

    def __str__(self) -> str:
        items = '\n'.join(f'{TAB}{item},' for item in self.items)
        if len(self.items) > 1:
            items = f'(\n{items}\n)'
        else:
            items = self.items[0]
        string = f'from {self.name} import {items}'
        if self.type_checking:
            return add_prefix(string, TAB)
        return string

    __repr__ = __str__

    @classmethod
    def from_big_raw(cls, raw: str) -> Optional[tuple['FromImport', str]]:
        stripped = raw.strip(' ')
        match = re.match(
            r'^from (.+?) import \(((?:.|\n)+?)\)',
            stripped,
        ) or re.match(
            r'^from (.+?) import ([a-zA-Z_0-9*, ]+)',
            stripped,
        )
        if match is None:
            return None
        name = match.group(1)
        raw_items = match.group(2)
        items: list[str] = []
        for value in raw_items.split(','):
            value = value.strip(' \n')
            if not value:
                continue
            items.append(value)
        new_raw = stripped[match.end():].split('\n', 1)[-1]
        instance = cls(
            raw=match.group(0),
            name=name,
            items=items,
            type_checking=raw.startswith(TAB),
        )
        return (instance, new_raw)


def get_import_or_line(raw: str) -> tuple[Import | FromImport | str, str]:
    result = Import.from_big_raw(raw) or FromImport.from_big_raw(raw)
    if result is None:
        line, new_raw = raw.split('\n', 1)
        return (line, new_raw)
    return result
