from pyhtsl import (
    Team,
    GlobalStat,
    PlayerStat,
    Item,
    ALL_POSSIBLE_ITEM_KEYS,
    Enchantment,
)

from enum import Enum, auto
import re

from typing import Optional


class Teams:
    __slots__ = ()
    combat = Team('Combat')
    mining = Team('Mining')
    farming = Team('Farming')
    fishing = Team('Fishing')


class GlobalStats:
    __slots__ = ()
    last_unix = GlobalStat('last_unix')

    latest_cookies = GlobalStat('latest_cookies')
    cookie_goal = GlobalStat('cookie_goal')
    cookies_needed = GlobalStat('cookies_needed')

    time_temp = GlobalStat('time/temp')
    time_day = GlobalStat('time/day')
    time_hour = GlobalStat('time/hour')
    time_minutes = GlobalStat('time/minutes')
    time_color = GlobalStat('time/color')


class PlayerStats:
    __slots__ = ()
    pass


LINE_REGEX = re.compile(r'^(x+)(\.*)$')
def fetch_digits(
    fetch_from: PlayerStat,
    assign_to: PlayerStat,
    line: Optional[str] = None,  # 'xxx...' means number abcdefghi -> def
    *,
    size: Optional[int] = None,
    right_offset: Optional[int] = None,
) -> None:
    if line is None:
        assert size is not None and right_offset is not None
    else:
        match = LINE_REGEX.match(line)
        assert match is not None
        size = len(match.group(1))
        right_offset = len(match.group(2))
    high, low = 10 ** (size + right_offset), 10 ** right_offset
    assign_to.value = (fetch_from - (fetch_from // high * high)) // low


class ItemRarity(Enum):
    COMMON = 'f'
    UNCOMMON = 'a'
    RARE = '9'
    EPIC = '5'
    LEGENDARY = '6'
    MYTHIC = 'd'


class ItemType(Enum):
    Armor = auto()
    Weapon = auto()
    Tool = auto()
    Consumable = auto()
    Material = auto()


class CustomItem:
    name: str
    key: ALL_POSSIBLE_ITEM_KEYS
    rarity: ItemRarity
    type: ItemType
    def __init__(
        self,
        name: str,
        key: ALL_POSSIBLE_ITEM_KEYS,
        rarity: ItemRarity,
        type: ItemType,
        enchantments: Optional[list[Enchantment]] = None,
    ) -> None:
        self.name = name
        self.key = key
        self.rarity = rarity
        self.type = type
        self.enchantments = enchantments

    @property
    def item(self) -> Item:
        lore: list[str] = [f'&8{self.type.name}']
        lore.append(f'&{self.rarity.value}{self.rarity.name}')
        if len(lore) == 2:
            lore.pop(0)
            lore[-1] = f'{lore[-1]} {self.type.name.upper()}'
        return Item(
            self.key,
            name=self.name,
            lore=lore,
            hide_all_flags=True,
        )
