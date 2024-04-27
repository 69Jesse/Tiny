from pyhtsl import (
    Team,
    PlayerStat,
    Item,
    ALL_POSSIBLE_ITEM_KEYS,
    Enchantment,
    delete_all_items_from_imports_folder,
)
from stats.playerstats import (
    MAX_HEALTH,
    INTELLIGENCE,
    MAX_MANA,
    SPEED,
    MINING_SPEED,
    FORAGING_SPEED,
    MINING_FORTUNE,
    FARMING_FORTUNE,
    FORAGING_FORTUNE,
    DAMAGE,
    STRENGTH,
    STRENGTH_BIG,
    STRENGTH_SMALL,
    DEFENSE,
    DEFENSE_BIG,
    DEFENSE_SMALL,
)

from enum import Enum, auto
import re

from typing import Optional


delete_all_items_from_imports_folder()


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

    def better_name(self, item_key: ALL_POSSIBLE_ITEM_KEYS) -> str:
        if self is ItemType.Tool:
            if item_key.endswith('_pickaxe'):
                return 'Pickaxe'
            if item_key.endswith('_axe'):
                return 'Axe'
            if item_key.endswith('_shovel'):
                return 'Shovel'
            if item_key.endswith('_hoe'):
                return 'Hoe'
            if item_key == 'fishing_rod':
                return 'Fishing Rod'
        return self.name


class BuffType(Enum):
    max_health =       (MAX_HEALTH,         100,    1000,   lambda x: x,        '&7Health:&a +{value:,}',             f'&c❤ Health&f {MAX_HEALTH}',                       )
    defense =          (DEFENSE,            0,      -1,     lambda x: x / 10,   '&7Defense:&a +{value}%',         f'&a❈ Defense&f {DEFENSE_BIG}.{DEFENSE_SMALL}',     )
    speed =            (SPEED,              100,    300,    lambda x: x,        '&7Speed:&a +{value:,}',              f'&f✦ Speed&f {SPEED}',                             )  # Speed x where x = value // 20
    damage =           (DAMAGE,             1,      -1,     lambda x: x,        '&7Damage:&c +{value:,}',             f'&c❁ Damage&f {DAMAGE}',                           )
    strength =         (STRENGTH,           1000,   -1,     lambda x: x / 10,   '&7Strength:&c +{value}%',        f'&c❁ Strength&f {STRENGTH_BIG}.{STRENGTH_SMALL}',  )  # Strength x where x = value // 50
    intelligence =     (INTELLIGENCE,       0,      -1,     lambda x: x,        '&7Intelligence:&a +{value:,}',       f'&b✎ Intelligence&f {INTELLIGENCE}',               )
    max_mana =         (MAX_MANA,           100,    -1,     lambda x: x,        '',                                   '',                                                  )
    mining_speed =     (MINING_SPEED,       0,      -1,     lambda x: x,        '&7Mining Speed:&a +{value:,}',       f'&6⸕ Mining Speed&f {MINING_SPEED}',                )
    foraging_speed =   (FORAGING_SPEED,     0,      -1,     lambda x: x,        '&7Foraging Speed:&a +{value:,}',     f'&6⸕ Foraging Speed&f {FORAGING_SPEED}',            )
    mining_fortune =   (MINING_FORTUNE,     100,    500,    lambda x: x,        '&7Mining Fortune:&a +{value:,}',     f'&6☘ Mining Fortune&f {MINING_FORTUNE}',            )
    farming_fortune =  (FARMING_FORTUNE,    100,    500,    lambda x: x,        '&7Farming Fortune:&a +{value:,}',    f'&6☘ Farming Fortune&f {FARMING_FORTUNE}',          )
    foraging_fortune = (FORAGING_FORTUNE,   100,    500,    lambda x: x,        '&7Foraging Fortune:&a +{value:,}',   f'&6☘ Foraging Fortune&f {FORAGING_FORTUNE}',        )

    @property
    def stat(self) -> PlayerStat:
        return self.value[0]

    @property
    def min(self) -> int:
        return self.value[1]

    @property
    def max(self) -> int:
        return self.value[2]

    def format_value(self, value: int) -> float:
        return self.value[3](value)

    def formatted_addition(self, value: int) -> str:
        v = self.format_value(value)
        if v.is_integer():
            v = int(v)
        else:
            v = f'{v:.1f}'
        return self.value[4].format(value=v)

    @property
    def formatted_total(self) -> str:
        return self.value[5]


class Buff:
    type: BuffType
    value: int
    def __init__(
        self,
        type: BuffType,
        value: int,
    ) -> None:
        self.type = type
        self.value = value


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
    enchantments: Optional[list[Enchantment]]
    buffs: Optional[list[Buff]]
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
        self.buffs = self.updated_buffs(buffs)

    def find_buff(self, buffs: list[Buff], buff_type: BuffType) -> Buff:
        for buff in buffs:
            if buff.type is buff_type:
                return buff
        buff = Buff(buff_type, 0)
        buffs.append(buff)
        return buff

    def updated_buffs(self, buffs: Optional[list[Buff]]) -> list[Buff]:
        buffs = buffs or []
        value = DEFAULT_MINING_SPEED.get(self.key, 0)
        if value > 0:
            buff_type = BuffType.foraging_speed if self.key.endswith('_axe') else BuffType.mining_speed
            self.find_buff(buffs, buff_type).value += value
        value = DEFAULT_DAMAGE.get(self.key, 0)
        if value > 0:
            self.find_buff(buffs, BuffType.damage).value += value
        for enchantment in self.enchantments or []:
            assert enchantment.level is not None
            if enchantment.name == 'efficiency':
                buff_type = BuffType.foraging_speed if self.key.endswith('_axe') else BuffType.mining_speed
                self.find_buff(buffs, buff_type).value += int(MINING_SPEED_PER_EFF_LEVEL * enchantment.level + 0.5)
            elif enchantment.name == 'sharpness':
                self.find_buff(buffs, BuffType.damage).value += int(DAMAGE_PER_SHARPNESS_LEVEL * enchantment.level + 0.5)
        buffs.sort(key=lambda buff: list(BuffType).index(buff.type))
        return buffs

    @property
    def item(self) -> Item:
        type_name = self.type.better_name(self.key)
        lore: list[str] = [f'&8{type_name}']

        if self.buffs:
            lore.append('')
            for buff in self.buffs:
                lore.append(buff.type.formatted_addition(buff.value))
            lore.append('')

        lore.append(f'&{self.rarity.value}&l{self.rarity.name}')
        if len(lore) == 2:
            lore.pop(0)
            lore[-1] = f'{lore[-1]} {type_name.upper()}'
        return Item(
            self.key,
            name=f'&{self.rarity.value}{self.name}',
            lore=lore,
            enchantments=self.enchantments,
            hide_all_flags=True,
            unbreakable=True,
        )


class Items:
    __slots__ = ()
    wooden_pickaxe = CustomItem(
        'Wooden Pickaxe',
        'wooden_pickaxe',
        ItemRarity.COMMON,
        ItemType.Tool,
    )
    stone_pickaxe = CustomItem(
        'Stone Pickaxe',
        'stone_pickaxe',
        ItemRarity.COMMON,
        ItemType.Tool,
    )


Items.wooden_pickaxe.item.save()
Items.stone_pickaxe.item.save()
