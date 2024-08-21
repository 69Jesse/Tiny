from pyhtsl import (
    Team,
    PlayerStat,
    Item,
    Enchantment,
    delete_all_items_from_imports_folder,
    IfAnd,
    HasItem,
)
from pyhtsl.types import ALL_ITEM_KEYS, IfStatement

from enum import Enum, auto
import re

from typing import Optional, Generator

from stats import (
    POWER,
    MAX_POWER,
    MINING_SPEED,
    FORAGING_SPEED,
    MINING_FORTUNE,
    FARMING_FORTUNE,
    FORAGING_FORTUNE,
    DAMAGE,
)


delete_all_items_from_imports_folder()


class Teams:
    __slots__ = ()
    bloods = Team('BLOOD')
    crips = Team('CRIP')
    blacks = Team('BLACK')
    kings = Team('KING')
    guards = Team('GUARD')


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

    def better_name(self, item_key: ALL_ITEM_KEYS) -> str:
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


class ItemCheck(Enum):
    IN_INVENTORY = 'inventory'
    IN_HAND = 'hand'
    IN_HOTBAR = 'hotbar'
    WEARING = 'armor'
    ANYWHERE = 'anywhere'


class BuffType(Enum):
    damage =           (DAMAGE,             1,      -1,     lambda x: f'{x:.2f}',  '&7Attack Damage:&c +{value}',        '')
    power =            (MAX_POWER,          0,      -1,     lambda x: x,           '&7Power:&a +{value}',              '')
    mining_speed =     (MINING_SPEED,       0,      -1,     lambda x: x,           '&7Mining Speed:&a +{value}',       '')
    foraging_speed =   (FORAGING_SPEED,     0,      -1,     lambda x: x,           '&7Foraging Speed:&a +{value}',     '')
    mining_fortune =   (MINING_FORTUNE,     100,    500,    lambda x: x,           '&7Mining Fortune:&a +{value}',     '')
    farming_fortune =  (FARMING_FORTUNE,    100,    500,    lambda x: x,           '&7Farming Fortune:&a +{value}',    '')
    foraging_fortune = (FORAGING_FORTUNE,   100,    500,    lambda x: x,           '&7Foraging Fortune:&a +{value}',   '')

    @property
    def stat(self) -> PlayerStat:
        return self.value[0]

    @property
    def min(self) -> int:
        return self.value[1]

    @property
    def max(self) -> int:
        return self.value[2]

    def format_value(self, value: float) -> str | float:
        return self.value[3](value)

    def formatted_addition(self, value: float) -> str:
        v = self.format_value(value)
        if isinstance(v, float):
            if v.is_integer():
                v = int(v)
            else:
                v = f'{v:.1f}'
        try:
            v = str(v).replace(str(int(float(v))), f'{int(float(v)):,}')
        except ValueError:
            pass
        return self.value[4].format(value=v)

    @property
    def formatted_total(self) -> str:
        return self.value[5]


class Buff:
    type: BuffType
    value: float
    def __init__(
        self,
        type: BuffType,
        value: float,
    ) -> None:
        self.type = type
        self.value = value


MINING_SPEED_PER_EFF_LEVEL: int = 60
DEFAULT_MINING_SPEED: dict[ALL_ITEM_KEYS, int] = {
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

DAMAGE_PER_SHARPNESS_LEVEL: float = 1.25
DEFAULT_DAMAGE: dict[ALL_ITEM_KEYS, float] = {
    'wooden_sword': 4,
    'stone_sword': 5,
    'iron_sword': 6,
    'golden_sword': 4,
    'diamond_sword': 7,

    'wooden_pickaxe': 2,
    'stone_pickaxe': 3,
    'iron_pickaxe': 4,
    'golden_pickaxe': 2,
    'diamond_pickaxe': 5,

    'wooden_axe': 3,
    'stone_axe': 4,
    'iron_axe': 5,
    'golden_axe': 3,
    'diamond_axe': 6,

    'wooden_shovel': 1,
    'stone_shovel': 2,
    'iron_shovel': 3,
    'golden_shovel': 1,
    'diamond_shovel': 4,
}


class CustomItem:
    name: str
    key: ALL_ITEM_KEYS
    rarity: ItemRarity
    type: ItemType
    check: ItemCheck
    enchantments: Optional[list[Enchantment]]
    buffs: Optional[list[Buff]]
    def __init__(
        self,
        name: str,
        key: ALL_ITEM_KEYS,
        rarity: ItemRarity,
        type: ItemType,
        check: Optional[ItemCheck] = None,
        enchantments: Optional[list[Enchantment]] = None,
        buffs: Optional[list[Buff]] = None,
    ) -> None:
        self.name = name
        self.key = key
        self.rarity = rarity
        self.type = type
        if check is None:
            if type is ItemType.Armor:
                check = ItemCheck.WEARING
            elif type is ItemType.Weapon:
                check = ItemCheck.IN_HAND
            else:
                check = ItemCheck.ANYWHERE
        self.check = check
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
                self.find_buff(buffs, buff_type).value += MINING_SPEED_PER_EFF_LEVEL * enchantment.level
            elif enchantment.name == 'sharpness':
                self.find_buff(buffs, BuffType.damage).value += DAMAGE_PER_SHARPNESS_LEVEL * enchantment.level
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

    def if_has_condition(self) -> IfStatement:
        return IfAnd(
            HasItem(self.item, where_to_check=self.check.value),
        )


class Items:
    __slots__ = ()
    tier_1_weapon = CustomItem(
        'Tier 1 Weapon',
        'wooden_sword',
        ItemRarity.COMMON,
        ItemType.Weapon,
        buffs=[Buff(BuffType.power, 0)],
    )
    tier_2_weapon = CustomItem(
        'Tier 2 Weapon',
        'wooden_axe',
        ItemRarity.UNCOMMON,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 1)],
        buffs=[Buff(BuffType.power, 0)],
    )
    tier_3_weapon = CustomItem(
        'Tier 3 Weapon',
        'stone_shovel',
        ItemRarity.UNCOMMON,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 2)],
        buffs=[Buff(BuffType.power, 5)],
    )
    tier_4_weapon = CustomItem(
        'Tier 4 Weapon',
        'wooden_shovel',
        ItemRarity.UNCOMMON,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 3)],
        buffs=[Buff(BuffType.power, 10)],
    )
    tier_5_weapon = CustomItem(
        'Tier 5 Weapon',
        'stone_sword',
        ItemRarity.UNCOMMON,
        ItemType.Weapon,
        buffs=[Buff(BuffType.power, 15)],
    )
    tier_6_weapon = CustomItem(
        'Tier 6 Weapon',
        'stone_axe',
        ItemRarity.RARE,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 1)],
        buffs=[Buff(BuffType.power, 20)],
    )
    tier_7_weapon = CustomItem(
        'Tier 7 Weapon',
        'iron_shovel',
        ItemRarity.RARE,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 2)],
        buffs=[Buff(BuffType.power, 25)],
    )
    tier_8_weapon = CustomItem(
        'Tier 8 Weapon',
        'wooden_pickaxe',
        ItemRarity.RARE,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 3), Enchantment('efficiency', 2)],
        buffs=[Buff(BuffType.power, 30)],
    )
    tier_9_weapon = CustomItem(
        'Tier 9 Weapon',
        'golden_shovel',
        ItemRarity.RARE,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 4)],
        buffs=[Buff(BuffType.power, 35)],
    )
    tier_10_weapon = CustomItem(
        'Tier 10 Weapon',
        'diamond_pickaxe',
        ItemRarity.EPIC,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 1)],
        buffs=[Buff(BuffType.power, 40)],
    )
    tier_11_weapon = CustomItem(
        'Tier 11 Weapon',
        'golden_sword',
        ItemRarity.EPIC,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 2)],
        buffs=[Buff(BuffType.power, 45)],
    )
    tier_12_weapon = CustomItem(
        'Tier 12 Weapon',
        'stone_pickaxe',
        ItemRarity.EPIC,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 3), Enchantment('efficiency', 2)],
        buffs=[Buff(BuffType.power, 50)],
    )
    tier_13_weapon = CustomItem(
        'Tier 13 Weapon',
        'golden_pickaxe',
        ItemRarity.EPIC,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 4)],
        buffs=[Buff(BuffType.power, 55)],
    )
    tier_14_weapon = CustomItem(
        'Tier 14 Weapon',
        'iron_sword',
        ItemRarity.LEGENDARY,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 1)],
        buffs=[Buff(BuffType.power, 60)],
    )
    tier_15_weapon = CustomItem(
        'Tier 15 Weapon',
        'golden_hoe',
        ItemRarity.LEGENDARY,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 6)],
        buffs=[Buff(BuffType.power, 65)],
    )
    tier_16_weapon = CustomItem(
        'Tier 16 Weapon',
        'diamond_shovel',
        ItemRarity.LEGENDARY,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 3)],
        buffs=[Buff(BuffType.power, 70)],
    )
    tier_17_weapon = CustomItem(
        'Tier 17 Weapon',
        'golden_axe',
        ItemRarity.LEGENDARY,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 4)],
        buffs=[Buff(BuffType.power, 75)],
    )
    tier_18_weapon = CustomItem(
        'Tier 18 Weapon',
        'diamond_sword',
        ItemRarity.MYTHIC,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 1)],
        buffs=[Buff(BuffType.power, 80)],
    )

    @staticmethod
    def weapons() -> list[CustomItem]:
        return [
            Items.tier_1_weapon,
            Items.tier_2_weapon,
            Items.tier_3_weapon,
            Items.tier_4_weapon,
            Items.tier_5_weapon,
            Items.tier_6_weapon,
            Items.tier_7_weapon,
            Items.tier_8_weapon,
            Items.tier_9_weapon,
            Items.tier_10_weapon,
            Items.tier_11_weapon,
            Items.tier_12_weapon,
            Items.tier_13_weapon,
            Items.tier_14_weapon,
            Items.tier_15_weapon,
            Items.tier_16_weapon,
            Items.tier_17_weapon,
            Items.tier_18_weapon,
        ]

    @classmethod
    def all(cls) -> Generator[CustomItem, None, None]:
        for item in cls.__dict__.values():
            if isinstance(item, CustomItem):
                yield item
