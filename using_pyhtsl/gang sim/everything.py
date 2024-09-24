from pyhtsl import (
    Team,
    PlayerStat,
    Item,
    Enchantment,
    delete_all_items_from_imports_folder,
    IfAnd,
    HasItem,
    teleport_player,
    trigger_function,
    chat,
    play_sound,
)
from pyhtsl.types import ALL_ITEM_KEYS, IfStatement, LEATHER_ARMOR_KEYS

from enum import Enum, auto
import re

from typing import Optional, Generator, Callable

from constants import (
    PLAYER_POWER,
    PLAYER_MAX_POWER,
    PLAYER_MINING_SPEED,
    PLAYER_FORAGING_SPEED,
    PLAYER_MINING_FORTUNE,
    PLAYER_FARMING_FORTUNE,
    PLAYER_FORAGING_FORTUNE,
    PLAYER_DAMAGE,
    Bloods,
    Crips,
    Kings,
    Grapes,
    IMPORTANT_MESSAGE_PREFIX,
    TELEPORTING_ID,
    TELEPORTING_TIMER,
)
from title_action_bar import WaitingOnTeleportTitleActionBar


delete_all_items_from_imports_folder()


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
        if self is ItemType.Armor:
            if item_key.endswith('_helmet') or item_key.endswith('_cap'):
                return 'Helmet'
            if item_key.endswith('_chestplate') or item_key.endswith('_tunic'):
                return 'Chestplate'
            if item_key.endswith('_leggings') or item_key.endswith('_pants'):
                return 'Leggings'
            if item_key.endswith('_boots'):
                return 'Boots'
        return self.name


class ItemCheck(Enum):
    IN_INVENTORY = 'inventory'
    IN_HAND = 'hand'
    IN_HOTBAR = 'hotbar'
    WEARING = 'armor'
    ANYWHERE = 'anywhere'


ROMAN_NUMERALS: dict[int, str] = {
    1: 'I',
    2: 'II',
    3: 'III',
    4: 'IV',
    5: 'V',
    6: 'VI',
    7: 'VII',
    8: 'VIII',
    9: 'IX',
    10: 'X',
}


class BuffType(Enum):
    damage =           (PLAYER_DAMAGE,             1,      -1,     lambda x: f'{x:.2f}',         '&7Damage:&c +{value}',        '')
    protection =       (None,               0,      -1,     lambda x: ROMAN_NUMERALS[x],  '&7Protection:&a {value}',          '')
    power =            (PLAYER_MAX_POWER,          100,      -1,     lambda x: x,                  '&7Power:&4 +{value}',              '')
    # mining_speed =     (PLAYER_MINING_SPEED,       0,      -1,     lambda x: x,                  '&7Mining Speed:&a +{value}',       '')
    # foraging_speed =   (PLAYER_FORAGING_SPEED,     0,      -1,     lambda x: x,                  '&7Foraging Speed:&a +{value}',     '')
    # mining_fortune =   (PLAYER_MINING_FORTUNE,     100,    500,    lambda x: x,                  '&7Mining Fortune:&a +{value}',     '')
    # farming_fortune =  (PLAYER_FARMING_FORTUNE,    100,    500,    lambda x: x,                  '&7Farming Fortune:&a +{value}',    '')
    # foraging_fortune = (PLAYER_FORAGING_FORTUNE,   100,    500,    lambda x: x,                  '&7Foraging Fortune:&a +{value}',   '')

    @property
    def stat(self) -> PlayerStat | None:
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


# MINING_SPEED_PER_EFF_LEVEL: int = 60
# DEFAULT_MINING_SPEED: dict[ALL_ITEM_KEYS, int] = {
#     'wooden_pickaxe': 70,
#     'stone_pickaxe': 110,
#     'iron_pickaxe': 160,
#     'golden_pickaxe': 250,
#     'diamond_pickaxe': 220,

#     'wooden_axe': 70,
#     'stone_axe': 110,
#     'iron_axe': 160,
#     'golden_axe': 250,
#     'diamond_axe': 220,
# }

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
    color: Optional[str]
    quote: Optional[str]
    def __init__(
        self,
        name: str,
        key: ALL_ITEM_KEYS,
        rarity: ItemRarity,
        type: ItemType,
        check: Optional[ItemCheck] = None,
        enchantments: Optional[list[Enchantment]] = None,
        buffs: Optional[list[Buff]] = None,
        color: Optional[str] = None,
        quote: Optional[str] = None,
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
        self.color = color
        self.quote = quote

    def find_buff(self, buffs: list[Buff], buff_type: BuffType) -> Buff:
        for buff in buffs:
            if buff.type is buff_type:
                return buff
        buff = Buff(buff_type, 0)
        buffs.append(buff)
        return buff

    def updated_buffs(self, buffs: Optional[list[Buff]]) -> list[Buff]:
        buffs = buffs or []
        # value = DEFAULT_MINING_SPEED.get(self.key, 0)
        # if value > 0:
        #     buff_type = BuffType.foraging_speed if self.key.endswith('_axe') else BuffType.mining_speed
        #     self.find_buff(buffs, buff_type).value += value
        value = DEFAULT_DAMAGE.get(self.key, 0)
        if value > 0:
            self.find_buff(buffs, BuffType.damage).value += value
        for enchantment in self.enchantments or []:
            assert enchantment.level is not None
            # if enchantment.name == 'efficiency':
            #     buff_type = BuffType.foraging_speed if self.key.endswith('_axe') else BuffType.mining_speed
            #     self.find_buff(buffs, buff_type).value += MINING_SPEED_PER_EFF_LEVEL * enchantment.level
            if enchantment.name == 'sharpness':
                self.find_buff(buffs, BuffType.damage).value += DAMAGE_PER_SHARPNESS_LEVEL * enchantment.level
            if enchantment.name == 'protection':
                self.find_buff(buffs, BuffType.protection).value += enchantment.level
        for i in range(len(buffs) - 1, -1, -1):
            buff = buffs[i]
            if buff.value == 0:
                buffs.pop(i)
        buffs.sort(key=lambda buff: list(BuffType).index(buff.type))
        return buffs

    @property
    def item(self) -> Item:
        lore: list[str] = []

        if self.buffs:
            for buff in self.buffs:
                lore.append(buff.type.formatted_addition(buff.value))
            lore.append('')

        if self.quote is not None:
            lore.append(self.quote)
            lore.append('')

        type_name = self.type.better_name(self.key)
        lore.append(f'&{self.rarity.value}&l{self.rarity.name} {type_name.upper()}')

        return Item(
            self.key,
            name=f'&{self.rarity.value}{self.name}',
            lore=lore,
            enchantments=self.enchantments,
            hide_all_flags=True,
            unbreakable=True,
            color=self.color,
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

    LEADER_HELMET_QUOTE: str = (
        '&eTo transfer leadership, take this'
        '\n&eoff and give it to your successor.'
        '\n\n&eHowever, do not wait too long or a'
        '\n&enew leader will randomly be chosen.'
    )

    bloods_chestplate = CustomItem(
        f'&{Bloods.ID}Bloods Identity',
        'leather_tunic',
        ItemRarity.RARE,
        ItemType.Armor,
        color='85221C',
        quote=(
            '&8Red runs through the veins,'
            '\n&8and loyalty through the soul.'
            '\n&8 - Bloods for life'
        ),
    )
    bloods_leader_crown = CustomItem(
        f'&{Bloods.ID}Bloods Gang Leader',
        'golden_helmet',  # 'leather_cap',
        ItemRarity.LEGENDARY,
        ItemType.Armor,
        buffs=[Buff(BuffType.power, 25)],
        enchantments=[Enchantment('protection', 3)],
        # color='611814',
        quote=LEADER_HELMET_QUOTE,
    )

    crips_chestplate = CustomItem(
        f'&{Crips.ID}Crips Identity',
        'leather_tunic',
        ItemRarity.RARE,
        ItemType.Armor,
        color='2B88A5',
        quote=(
            '&8Blue waves crash hard,'
            '\n&8we\'re loyal to the soil.'
            '\n&8 - Crip \'til I rest'
        ),
    )
    crips_leader_crown = CustomItem(
        f'&{Crips.ID}Crips Gang Leader',
        'golden_helmet',  # 'leather_cap',
        ItemRarity.LEGENDARY,
        ItemType.Armor,
        buffs=[Buff(BuffType.power, 25)],
        enchantments=[Enchantment('protection', 3)],
        # color='1F6378',
        quote=LEADER_HELMET_QUOTE,
    )

    kings_chestplate = CustomItem(
        f'&{Kings.ID}Kings Identity',
        'leather_tunic',
        ItemRarity.RARE,
        ItemType.Armor,
        color='DFC33E',
        quote=(
            '&8Crown on the head,'
            '\n&8and fire in the chest.'
            '\n&8 - Kings don\'t break'
        ),
    )
    kings_leader_crown = CustomItem(
        f'&{Kings.ID}Kings Gang Leader',
        'golden_helmet',  # 'leather_cap',
        ItemRarity.LEGENDARY,
        ItemType.Armor,
        buffs=[Buff(BuffType.power, 25)],
        enchantments=[Enchantment('protection', 3)],
        # color='A28E2D',
        quote=LEADER_HELMET_QUOTE,
    )

    grapes_chestplate = CustomItem(
        f'&{Grapes.ID}Grapes Identity',
        'leather_tunic',
        ItemRarity.RARE,
        ItemType.Armor,
        color='973A8F',
        quote=(
            '&8We don\'t just rep'
            '\n&8purple, we bleed it.'
            '\n&8 - Grapes take it all'
        ),
    )
    grapes_leader_crown = CustomItem(
        f'&{Grapes.ID}Grapes Gang Leader',
        'golden_helmet',  # 'leather_cap',
        ItemRarity.LEGENDARY,
        ItemType.Armor,
        buffs=[Buff(BuffType.power, 25)],
        enchantments=[Enchantment('protection', 3)],
        # color='6E2A68',
        quote=LEADER_HELMET_QUOTE,
    )

    @staticmethod
    def gang_armor() -> list[CustomItem]:
        return [
            Items.bloods_chestplate,
            Items.bloods_leader_crown,
            Items.crips_chestplate,
            Items.crips_leader_crown,
            Items.kings_chestplate,
            Items.kings_leader_crown,
            Items.grapes_chestplate,
            Items.grapes_leader_crown,
        ]

    @classmethod
    def all(cls) -> Generator[CustomItem, None, None]:
        for item in cls.__dict__.values():
            if isinstance(item, CustomItem):
                yield item


class Teleport:
    id: int
    name: str
    delay: int
    coordinates: tuple[float, float, float] | tuple[float, float, float, float, float]
    _execute: Callable[[], None]
    def __init__(
        self,
        id: int,
        name: str,
        delay: int,
        coordinates: tuple[float, float, float] | tuple[float, float, float, float, float],
        execute: Optional[Callable[[], None]] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.delay = delay
        self.coordinates = coordinates
        self._execute = execute or (lambda: teleport_player(self.coordinates))

    def apply(self) -> None:
        TELEPORTING_ID.value = self.id
        TELEPORTING_TIMER.value = self.delay
        WaitingOnTeleportTitleActionBar.apply()
        chat(IMPORTANT_MESSAGE_PREFIX + f'&eStand still! Teleporting to&a {self.name}&e in&c {self.delay} seconds&e.')

    def execute(self) -> None:
        self._execute()
        chat(IMPORTANT_MESSAGE_PREFIX + f'&eTeleported to&a {self.name}&e.')
        play_sound('Enderman Teleport')


class Teleports:
    SPAWN = Teleport(
        id=1,
        name='Spawn',
        delay=5,
        coordinates=(-0.5, 46, -40.5, -180, 0),
        execute=lambda: trigger_function('Move to Spawn'),
    )

    @classmethod
    def all(cls) -> Generator[Teleport, None, None]:
        for teleport in cls.__dict__.values():
            if isinstance(teleport, Teleport):
                yield teleport
