from abc import ABC

from typing import reveal_type

class Stat(ABC):
    def __class_getitem__(cls, name: str) -> ...:
        return int

class PlayerStat(Stat):
    ...

def foo(p: PlayerStat['whatever']) -> None:
    reveal_type(p)

print(foo.__annotations__)
# {'p': <class 'int'>, 'return': None}
