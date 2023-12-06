import typing
from typing import (
    TypeAlias,
    Optional,
    Iterable,
    Any,
)


SingleExportTypes: TypeAlias = str | int | float
IterableExportTypes: TypeAlias = list | dict
ExportTypes: TypeAlias = SingleExportTypes | IterableExportTypes


def attr_check(attr: str) -> bool:
    return not attr.startswith('__') and not attr.endswith('__')


def validate(
    obj: Any,
    *,
    used_ids: set[int],
    depth: int = 0,
) -> ExportTypes:
    obj_id: int = id(obj)
    if not isinstance(obj, int) and (obj_id in used_ids or getattr(typing, obj.__class__.__name__, None) is obj.__class__):
        return f'REFERENCE TO {obj_id}'
    used_ids.add(obj_id)
    if isinstance(obj, SingleExportTypes):
        return obj
    if isinstance(obj, bytes):
        return str(obj)
    if not isinstance(obj, Iterable):
        return export(obj, used_ids=used_ids, depth=depth)
    return validate_iterable(obj, used_ids=used_ids)


def validate_iterable(
    obj: Iterable,
    *,
    used_ids: set[int],
) -> IterableExportTypes:
    if isinstance(obj, dict):
        return {
            str(key): validate(value, used_ids=used_ids)
            for key, value in obj.items()
        }
    return [
        validate(item, used_ids=used_ids)
        for item in obj
    ]


def export(
    obj: Any,
    *,
    used_ids: Optional[set[int]] = None,
    depth: int = 0,
) -> dict[str, ExportTypes]:
    if depth >= 3:
        return 'MAX DEPTH REACHED'  # type: ignore
    obj_id: int = id(obj)
    used_ids = used_ids or set((obj_id,))
    data: dict[str, ExportTypes] = {
        '__name': obj.__class__.__name__,
        '__id': obj_id,
    }
    for key in dir(obj):
        if not attr_check(key):
            continue
        try:
            value: Any = getattr(obj, key)
        except AttributeError:
            data[key] = 'NOT FOUND'
            continue
        try:
            data[key] = validate(value, used_ids=used_ids, depth=depth + 1)
        except Exception as e:
            data[key] = f'EXCEPTION ({e.__class__.__name__})'
    return data




# EXAMPLE

class Bar:
    a = 'hello'
    b = (1, 2, 3, 4)

class Foo:
    x = 123
    y = {
        'a': 1,
        'b': 2,
        'c': 4,
    }
    z = [1, 2, 3, y]
    def __init__(self) -> None:
        self.a = self
        self.b = self.x
        self.c = Bar()

import json
print(json.dumps(export(Foo()), indent=4))
"""
{
    "__name": "Foo",
    "__id": 2630097488400,
    "a": "REFERENCE TO 2630097488400",
    "b": 123,
    "c": {
        "__name": "Bar",
        "__id": 2630097488272,
        "a": "hello",
        "b": [
            1,
            2,
            3,
            4
        ]
    },
    "x": 123,
    "y": {
        "a": 1,
        "b": 2,
        "c": 4
    },
    "z": [
        1,
        2,
        3,
        "REFERENCE TO 2630097487808"
    ]
}
"""
