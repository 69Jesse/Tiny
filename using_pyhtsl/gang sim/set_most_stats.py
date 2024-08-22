from pyhtsl import (
    create_function,
    IfAnd,
)
from everything import Items, BuffType


@create_function('Set Most Stats')
def set_most_stats() -> None:
    for buff_type in BuffType:
        if buff_type.stat is None:
            continue
        buff_type.stat.value = buff_type.min
    for item in Items.all():
        with item.if_has_condition():
            if item.buffs is None:
                continue
            if not item.buffs:
                continue
            for buff in item.buffs:
                if buff.type.stat is None:
                    continue
                buff.type.stat.value += round(buff.value)
    for buff_type in BuffType:
        if buff_type.max == -1:
            continue
        if buff_type.stat is None:
            continue
        with IfAnd(
            buff_type.stat > buff_type.max,
        ):
            buff_type.stat.value = buff_type.max
