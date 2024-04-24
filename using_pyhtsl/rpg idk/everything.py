from pyhtsl import (
    Team,
    PlayerStat,
    Item,
    ALL_POSSIBLE_ITEM_KEYS,
    Enchantment,
)
from stats.playerstats import (
    MAX_HEALTH,
    MAX_MANA,
    SPEED,
    MINING_SPEED,
    FORAGING_SPEED,
    MINING_FORTUNE,
    FARMING_FORTUNE,
    FORAGING_FORTUNE,
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


class BuffType(Enum):
    max_health = MAX_HEALTH
    max_mana = MAX_MANA
    speed = SPEED
    mining_speed = MINING_SPEED
    foraging_speed = FORAGING_SPEED
    mining_fortune = MINING_FORTUNE
    farming_fortune = FARMING_FORTUNE
    foraging_fortune = FORAGING_FORTUNE


class Buff:

    def __init__(
        self,
        type: BuffType,
        value: int,
    ) -> None:
        ...


MINING_SPEED_PER_EFF_LEVEL: int = 60
DEFAULT_MINING_SPEED: dict[ALL_POSSIBLE_ITEM_KEYS, int] = {
    'wooden_pickaxe': 70,
    'stone_pickaxe': 110,
    'iron_pickaxe': 160,
    'golden_pickaxe': 250,
    'diamond_pickaxe': 220,

    'wooden_axe': 70,
    'stone_axe': 110,
    'iron_axe': 160,
    'golden_axe': 250,
    'diamond_axe': 220,
}

DAMAGE_PER_SHARPNESS_LEVEL: float = 6.25
DEFAULT_DAMAGE: dict[ALL_POSSIBLE_ITEM_KEYS, int] = {
    'wooden_sword': 20,
    'stone_sword': 25,
    'iron_sword': 30,
    'golden_sword': 20,
    'diamond_sword': 35,

    'wooden_pickaxe': 10,
    'stone_pickaxe': 15,
    'iron_pickaxe': 20,
    'golden_pickaxe': 10,
    'diamond_pickaxe': 25,

    'wooden_axe': 15,
    'stone_axe': 20,
    'iron_axe': 25,
    'golden_axe': 15,
    'diamond_axe': 30,

    'wooden_shovel': 5,
    'stone_shovel': 10,
    'iron_shovel': 15,
    'golden_shovel': 5,
    'diamond_shovel': 20,
}


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
        buffs: Optional[list[Buff]] = None,
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
