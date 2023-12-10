import re
from pathlib import Path
tab = '    '


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
            return add_prefix(string, tab)
        return string


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

    def __str__(self) -> str:
        items = '\n'.join(f'{tab}{item},' for item in self.items)
        if len(self.items) > 1:
            items = f'(\n{items}\n)'
        else:
            items = self.items[0]
        string = f'from {self.name} import {items}'
        if self.type_checking:
            return add_prefix(string, tab)
        return string


def add_prefix(string: str, prefix: str) -> str:
    return '\n'.join(f'{prefix}{line}' for line in string.split('\n'))


def sort_imports(raw: str) -> str:
    split = raw.split('\n')
    for i, line in enumerate(split):
        if not any(
            line.startswith(start)
            for start in ('if TYPE_CHECKING:', 'from ', 'import ', ' ', ')')
        ) and line != '':
            content = '\n'.join(split[:i])
            break
    else:
        content = ''

    temp_content = content

    imports: list[Import | FromImport] = []

    for match in re.finditer(r'from (.+?) import \(((?:.|\n)+?)\)', temp_content):
        name = match.group(1)
        raw_items = match.group(2)

        index = match.start()
        type_checking = (temp_content[index - 1] != '\n') if index != 0 else False

        items: list[str] = []
        for value in raw_items.split(','):
            value = value.strip(' \n')
            if not value:
                continue
            items.append(value)
        imports.append(FromImport(
            raw=match.group(0),
            name=name,
            items=items,
            type_checking=type_checking,
        ))
    for i in imports:
        temp_content = temp_content.replace(i.raw, '', 1)
    for match in re.finditer(r'from (.+?) import ([a-zA-Z_0-9*, ]+)', temp_content):
        name = match.group(1)
        raw_items = match.group(2)
        items: list[str] = []
        for value in raw_items.split(','):
            value = value.strip(' \n')
            if not value:
                continue
            items.append(value)

        index = match.start()
        type_checking = (temp_content[index - 1] != '\n') if index != 0 else False

        imports.append(FromImport(
            raw=match.group(0),
            name=name,
            items=items,
            type_checking=type_checking,
        ))
    for i in imports:
        temp_content = temp_content.replace(i.raw, '', 1)
    for match in re.finditer(r'import (.+)', temp_content):
        name = match.group(1)

        index = match.start()
        type_checking = (temp_content[index - 1] != '\n') if index != 0 else False

        imports.append(Import(
            raw=match.group(0),
            name=name,
            type_checking=type_checking,
        ))

    regular_imports: list[Import | FromImport] = []
    type_checking_imports: list[Import | FromImport] = []
    for i in imports:
        if isinstance(i, FromImport):
            i.items.sort()
            if 'TYPE_CHECKING' in i.items:
                i.items.remove('TYPE_CHECKING')
                i.items.insert(0, 'TYPE_CHECKING')
        if i.type_checking:
            type_checking_imports.append(i)
        else:
            regular_imports.append(i)

    type_checking_imports.sort(key=lambda i: i.name.removeprefix('.'))

    front: list[Import | FromImport] = []
    middle1: list[Import | FromImport] = []
    middle2: list[Import | FromImport] = []
    middle3: list[Import | FromImport] = []
    middle4: list[Import | FromImport] = []
    end: list[Import | FromImport] = []

    for i in regular_imports.copy():
        if any(
            str(i).startswith(start)
            for start in ('from discord', 'import discord', 'from bot', 'from __future__')
        ):
            front.append(i)
            continue
        if str(i) == 'import logging':
            end.append(i)
            continue
        if i.name == 'utils':
            middle1.append(i)
            continue
        if i.name.startswith('.'):
            middle2.append(i)
            continue
        if i.name in ('typing', 'types'):
            middle4.append(i)
            continue
        middle3.append(i)

    front.sort(
        key=lambda i: (-1 if i.name == '__future__' else 0 if str(i).startswith('import discord') else 1 if str(i).startswith('from discord') else 2, i.name)
    )
    middle4.sort(
        key=lambda i: (i.name == 'typing', i.name)
    )

    for lst in (middle1, middle2, middle3):
        lst.sort(key=lambda i: i.name)

    imports_string = ''

    for lst in (front, middle1, middle2, middle3, middle4):
        if lst:
            imports_string += '\n\n'
            imports_string += '\n'.join(map(str, lst))

    if type_checking_imports:
        imports_string += '\nif TYPE_CHECKING:\n'
        imports_string += '\n'.join(map(str, type_checking_imports))

    for lst in (end,):
        if lst:
            imports_string += '\n\n'
            imports_string += '\n'.join(map(str, lst))

    imports_string = imports_string.strip('\n')

    raw = imports_string + '\n\n\n' + raw.replace(content, '', 1).lstrip('\n')

    return raw


if __name__ != '__main__':
    __import__('sys').exit(1)


ignoring_folders: list[str] = [
    'legacy',
]

p = r'C:\Users\jesse\Desktop\Hackerman\GitHub\bigger\ButtersTemp'
for path in Path(p).rglob('*.py'):
    if any(path.parts[i] == folder for i in range(len(path.parts)) for folder in ignoring_folders):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    raw = sort_imports(raw)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(raw)
