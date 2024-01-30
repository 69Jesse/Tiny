"""bad very bad"""
from typing import (
    TypeAlias,
    overload,
    Literal,
    Any,
)


INDENTATION_SPACES: int = 4
# -1 for `\t` instead of spaces

JSON: TypeAlias = dict[str, Any]


def snakeify(name: str) -> str:
    return ''.join(
        f'_{char.lower()}' if char.isupper() else char
        for char in name
    ).lstrip('_')


def camelify(name: str) -> str:
    return ''.join(
        char.upper() if prev_char == '_' else char
        for prev_char, char in zip('_' + name, name)
    ).replace('_', '')


_types: dict[type | Literal['Any'], str] = {
    int: 'int',
    float: 'float',
    str: 'str',
    bool: 'bool',
    type(None): 'None',
    'Any': 'Any',
}


def valueify_all_has_valueify(data: list[JSON]) -> tuple[dict[str, list[Any]], dict[str, bool]]:
    values: dict[str, list[Any]] = {}
    for item in data:
        for key, value in item.items():
            values.setdefault(key, []).append(value)
    all_data_has_value: dict[str, bool] = {key: len(value) == len(data) for key, value in values.items()}
    for key, value in values.items():
        value.extend([None for _ in range(len(data) - len(value))])
    return values, all_data_has_value


def to_createify_typeify(
    values: dict[str, list[Any]],
) -> tuple[dict[str, list[JSON]], dict[str, list[str]]]:
    to_create: dict[str, list[JSON]] = {}
    types: dict[str, list[str]] = {}
    for key, value in values.items():
        for item in value:
            item_name: str
            if (item_type := type(item)) in _types:
                item_name = _types[item_type]
            elif item_type is list:
                t = type(item[0]) if item else 'Any'
                if not all(type(i) == t for i in item):
                    raise ValueError(f'Key {key} has multiple types: {item}')
                if t in _types:
                    item_name = f'list[{_types[t]}]'
                else:
                    camel = camelify(key)
                    item_name = f'list[{camel}]'
                    to_create.setdefault(camel, []).extend(item)
            else:
                item_name = camelify(key)
                to_create.setdefault(item_name, []).append(item)
            types.setdefault(key, []).append(item_name)
        types[key] = sorted(set(types[key]), key=lambda x: (x == 'None', x))
        if len(types[key]) > 1:
            if len(types[key]) == 2 and 'None' in types[key]:
                continue
            raise ValueError(f'Key {key} has multiple types: {types[key]}')
    return (to_create, types)


def stringify(
    name: str,
    types: dict[str, list[str]],
    all_data_has_value: dict[str, bool],
) -> str:
    arguments: str = '\n\t\t'.join(sorted((f'''{key}: {' | '.join(
        (
            t if t in _types.values() else 'dict[str, Any]' if not t.startswith('list[') else 'list[dict[str, Any]]' if t[5:-1] not in _types.values() else t
        ) for t in types[key]) + (' = None' if not all_data_has_value[key] else '')
    },''' for key in types.keys()), key=lambda x: (x.endswith(' = None'))))
    declarations: str = '\n\t\t'.join(f'''self.{snakeify(key)}: {' | '.join(types[key])} = {
        key if all(t in _types.values() for t in types[key]) else (
            (
                f'{camelify(key)}(**{key})' if not value[0].startswith('list[') else (
                    f'[{camelify(key)}(**item) for item in {key}]' if value[0][5:-1] not in _types.values() else key
                )
            ) + (
                f' if {key} is not None else None' if ('None' in types[key] and value[0].startswith('list[') and value[0][5:-1] not in _types.values()) else ''
            )
        )
    }''' for key, value in types.items())
    string = f'class {camelify(name)}:\n\tdef __init__(\n\t\tself,\n\t\t*,\n\t\t{arguments}\n\t) -> None:\n\t\t{declarations}'
    return string


@overload
def create(*, name: str, data: list[JSON], first_time: Literal[True] = True) -> None:
    ...
@overload
def create(*, name: str, data: list[JSON], first_time: Literal[False]) -> list[str]:
    ...
def create(
    *,
    name: str,
    data: list[JSON],
    first_time: bool = True,
) -> list[str] | None:
    values, all_data_has_value = valueify_all_has_valueify(data=data)
    to_create, types = to_createify_typeify(values=values)
    string = stringify(name=name, types=types, all_data_has_value=all_data_has_value)

    strings: list[str] = [string]
    for key, value in to_create.items():
        strings.extend(create(name=key, data=value, first_time=False))

    if not first_time:
        return strings

    text: str = '\n\n\n'.join(reversed(strings))
    typing_imports: list[str] = [f'{n},' for n in ('Any',) if n in text]
    text = (('from typing import (\n\t' + '\n\t'.join(typing_imports) + '\n)\n\n\n') if typing_imports else '') + text + '\n'
    if INDENTATION_SPACES != -1:
        text = text.replace('\t', ' '*INDENTATION_SPACES)
    with open(f'classes.py', 'w') as f:
        f.write(text)
    print('Done! Have fun..')
