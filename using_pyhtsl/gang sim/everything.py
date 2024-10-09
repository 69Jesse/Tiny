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

from typing import Optional, Generator, Callable, Literal

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
    WEAPON_ABILITIES,
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
    Item = auto()

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
    interaction_data_key: Optional[str]
    is_cookie_item: bool
    unbreakable: bool
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
        interaction_data_key: Optional[str] = None,
        is_cookie_item: bool = False,
        unbreakable: bool = True,
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
        self.interaction_data_key = interaction_data_key
        self.is_cookie_item = is_cookie_item
        self.unbreakable = unbreakable

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

        name = self.name
        if not any(name.startswith(f'&{c}') for c in '0123456789abcdef'):
            name = f'&{self.rarity.value}{name}'

        return Item(
            self.key,
            name=name,
            lore='\n'.join(lore),
            enchantments=self.enchantments,
            hide_all_flags=True,
            unbreakable=self.unbreakable,
            color=self.color,
            interaction_data_key=self.interaction_data_key,
            is_cookie_item=self.is_cookie_item,
        )

    def if_has_condition(self) -> IfStatement:
        return IfAnd(
            HasItem(self.item, where_to_check=self.check.value),
        )


def special_ability_quote(
    mode: Literal['click', 'worn', 'held'] | None,
    description: str,
    power_cost: int | None = None,
) -> str:
    quote = '&6Special Ability'
    if mode == 'click':
        quote += '&e&l RIGHT CLICK'
    elif mode == 'worn':
        quote += '&e&l WHILE WORN'
    elif mode == 'held':
        quote += '&e&l WHILE HELD'
    quote += '\n' + description
    if power_cost is not None:
        quote += f'\n&8Power Cost:&4 {power_cost}⸎ Power'
    return quote


def weapon_ability_quote(tier: int) -> Optional[str]:
    power_cost, speed_timer, regen_timer = WEAPON_ABILITIES.get(tier, (0, 0, 0))
    if speed_timer == 0 and regen_timer == 0:
        return None

    if speed_timer > 0 and regen_timer > 0:
        description = (
            f'&7Gain&f +1 Speed&7 for&a {speed_timer} second{'s' * (speed_timer != 1)}&7,'
             + f'\n&7and&d +1 Regen&7 for&a {regen_timer} second{'s' * (regen_timer != 1)}&7.'
        )
    elif speed_timer > 0:
        description = f'&7Gain&f +1 Speed&7 for&a {speed_timer} second{'s' * (speed_timer != 1)}&7.'
    elif regen_timer > 0:
        description = f'&7Gain&d +1 Regen&7 for&a {regen_timer} second{'s' * (regen_timer != 1)}&7.'
    else:
        raise

    return special_ability_quote('click', description, power_cost)


class Items:
    __slots__ = ()
    tier_1_weapon = CustomItem(
        'Tier 1 Weapon',
        'wooden_sword',
        ItemRarity.COMMON,
        ItemType.Weapon,
        buffs=[Buff(BuffType.power, 0)],
        quote=weapon_ability_quote(1),
    )
    tier_2_weapon = CustomItem(
        'Tier 2 Weapon',
        'wooden_axe',
        ItemRarity.UNCOMMON,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 1)],
        buffs=[Buff(BuffType.power, 0)],
        quote=weapon_ability_quote(2),
    )
    tier_3_weapon = CustomItem(
        'Tier 3 Weapon',
        'stone_shovel',
        ItemRarity.UNCOMMON,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 2)],
        buffs=[Buff(BuffType.power, 5)],
        quote=weapon_ability_quote(3),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTlRRdUNRQmlFcDVSU3UzVHIyaytvVk5LamhKa1hnOXJPeTZ1N3lvSWZvZXZCZjU4VXpXa2VHSjV4QUJ0cktyVHEyc0VCc0xSZ05wMlFNSjR4bS91Z1NjT21YTlZLVDBxWVdGSFRqYTNHTDhZODBkTmJZbk81UlZrUzh5ZUxHQmJZNlY1VmxleDUyZldjNnBxL2E1cGtQOENDVlk3dDl3OTdsencvejMzM0VBanl4REVrcjVneERNOG40Zm1CRFA3eUxYdWtTUkkvK1BXVlhWaDZ6NEFQdGV5Vk9Ma0FBQUE9IiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0.IC1PDkrsW6Q0dy1SmDCoRK4Uz4PWDBWCZI1Yj_FTRf3L6TuNaWHW8-LMma8v5xepQiRO-2ltvC9GrEPXFOw78Q',
    )
    tier_4_weapon = CustomItem(
        'Tier 4 Weapon',
        'wooden_shovel',
        ItemRarity.UNCOMMON,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 3)],
        buffs=[Buff(BuffType.power, 10)],
        quote=weapon_ability_quote(4),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTlRRdUNRQmlFcDVKU3UzVHIyaytvVk5KamlGa1hBOTNPeTZ1N3lvSWZvZXZCZjU4VXpXa2VHSjZ4QVFzYktyVHEyc0VHc0RSaE5KMlFXR1VSbS91Z1NjT2lYTlZLVDBvWVdGUFRqYTNHTDhZODBkTmJZaHZlcjBrYzhZeGRHUmJZNjE1VmxleDUyZldjNnBxL2E1cGtQOENFV1k3dDl3OEhoMXd2enozbjZBdHl4U2tndDVneENDNW40WHErOVAveUhVc2ZjUnlsL1BaS1F2WjRKc0FIRGhEYTA3a0FBQUE9IiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0.Ah-X0LCjtzmnPxNyGDa80QNCyoAYMuo6rNlog6fIkIwgd_8SUBd6sVixg4l4a0pzkl_FzKMW4yiQOXs_MrRhvA',
    )
    tier_5_weapon = CustomItem(
        'Tier 5 Weapon',
        'stone_sword',
        ItemRarity.UNCOMMON,
        ItemType.Weapon,
        buffs=[Buff(BuffType.power, 15)],
        quote=weapon_ability_quote(5),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTnV3NkNRQlJFeHpkcVkyZnJKL2lBQ0NVaGlEU1k0RnB2THU1cU5sa2VXWmFDdjVkb25HcE9Nam16QXBaWTBOT3F1bXBYQU1ZT3BtVXRKQ2IzbUEyOXRXU3hwRUpwWlhzbHBwaFRXWGVWeFMrellXTDdSbUlkWGNNc2lmbWRoUXdqYksxUjc3YzAvRlViVGxyelJsTXZUUXNIenF1cnZuL1luY2oxaXNJNzdYMUJyamdFNUQ0SERJTHpVYmllTC8yL2ZNUHlORW5pbkY4ZVdjVFNXd1o4QU1ic0tEKzVBQUFBIiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0.U-khegQdfd8mgl8zp71wue4bEIf7bdFWM6rv7waQlyfim3RM2K1FQAprm38XAm9D2rpY1hK9AeteP_mf4jWtHA',
    )
    tier_6_weapon = CustomItem(
        'Tier 6 Weapon',
        'stone_axe',
        ItemRarity.RARE,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 1)],
        buffs=[Buff(BuffType.power, 20)],
        quote=weapon_ability_quote(6),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTlBRK0NNQmlFejQ4ZzZPTG02azlRZ1Fpak1ZZ3NtRUNkbXhkYVRKTktEZFNCZnkvUmVOTTl5ZVc1SmVCaFFiVlZwdTJYQUtZdTVrOGpKR1psd3NiZVc3THdxRkphMlVHSk9SeDZtbmRyOFlzelR1endrbGlkcjZjOFRYakpUZ3dUYkd5bkhnL1o4Y1owbkxUbUwwMkQ3SHE0Y0p0MysvM0QxcWNncktyUTMwV0NBckdQS2FoSGpPUGpRUVJoSktPL2ZNMktMRTJUZ2wvdStabGx0eHo0QU4vdlR0RzVBQUFBIiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0.-mY6ExqoTPlAkQuzOgAf8TEDRUfUD4trC0b_waKN59qo_VnsBkhbN-x7NvdqdQ77c9ldfp181FKCHeejyNw3uQ',
    )
    tier_7_weapon = CustomItem(
        'Tier 7 Weapon',
        'iron_shovel',
        ItemRarity.RARE,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 2)],
        buffs=[Buff(BuffType.power, 25)],
        quote=weapon_ability_quote(7),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTlBRK0NNQmlFejQ4bzZPTG02azlRZ1FpaklZZ3VtRUNkbXhkYVRKTktEWlNCZnkvUmVOTTl5ZVc1RmVCaVNaVlZwdWxXQUtZTzVpOGpKR1pGd3NiZVdiSndxVlJhMlVHSk9SYjBNbjFqOGN0eW5OamhMYkdPcitjc1RYakJ6Z3dUYkcycm5rL1o4dHEwbkxUbWIwMkRiRHM0Y09xKytmNWg1NUVmbEdYZzdVTkJ2amhFNUZjalJ0SHBLUHdnbE9GZnZtSDVMVTJUbkY4ZVdjeHU5d3o0QUJjVHZEMjVBQUFBIiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0.DZeUSkDg1GrdDMaEGdwAa-MSTmeo9OaBDBX3tQZn12anS-3ygkDnoTZsvrUEgM6oVkuWesMzVOmeAuVIXIefww',
    )
    tier_8_weapon = CustomItem(
        'Tier 8 Weapon',
        'wooden_pickaxe',
        ItemRarity.RARE,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 3), Enchantment('efficiency', 2)],
        buffs=[Buff(BuffType.power, 30)],
        quote=weapon_ability_quote(8),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTlRRdUNRQmlFcDVMYTZ0S3RheitoRHlVOWlwaDFNZER0dkx5NmF5ejRoYTRILzMxU05LZDVZSGhtQTZ5eG90em9wdTQzQU9ZTVZ0VkloVVVhOHFuM2hneldsT2xTbTFGTEMwdXFtcUUyK0lWTkV6TzJDdHZnN3NkUktGTHVjOHl3TjUxK3YxVW5pcVlUVkphaUxXbFVYUThHVmd6MTl3K0hDOWxPbGptWG95dkpsaWVQN0h4Q3o3dWVwZTI0eXYzTGR6eDVSRkdZaU5zckR2ampHUU1mNkJDZzNMa0FBQUE9IiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0.FaC1zIkpOg_tysVY-YPBLJH1296r8AruoD9dqi4DmoA9UDl4UCIAqtN6nHskwr5MGz-uCBv_P-1rFAKCrbKlAw',
    )
    tier_9_weapon = CustomItem(
        'Tier 9 Weapon',
        'golden_shovel',
        ItemRarity.RARE,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 4)],
        buffs=[Buff(BuffType.power, 35)],
        quote=weapon_ability_quote(9),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTlBRK0NNQmlFejQ4bzRPTG02ay93bzBRWWlVRjB3UVRyM0x6WVNwcFVJS1VPL0h1SnhwdnVTUzdQQllDUE9UMmNidW91QUREMk1IMDFVbUZ5Uy9uUU8wY09QcFhhYU5kck9jV01YczI3ZHZqRkh5YXVieFVXeDNPU1o2bTQ4WVJqaEpXenVxcVVGYy9HQ2pKR3RJWjZaVHQ0OEo3dit2dUg5WjVZV0piaGZoTkpZbkliRTNzTUdNZUhuV1JocEtLL2ZNbUxTNWFsaFRqZDh5Ty9YSFBnQXlEc1VqQzVBQUFBIiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0.U3Eiq1RY0tfEqEBhV8g94IEVU9RBqUuR9r0F6UNVZe1_Ls2M63bMNN7Mg8uXot_PtIUtcW-pEUBAp71GhPWaEA',
    )
    tier_10_weapon = CustomItem(
        'Tier 10 Weapon',
        'diamond_pickaxe',
        ItemRarity.EPIC,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 1)],
        buffs=[Buff(BuffType.power, 40)],
        quote=weapon_ability_quote(10),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTlRRdUNRQmlFcHc5SzdkS3RheitoVWttUEltWmRESFE3TDYvdUtndW1vdXZCZjU4VXpXa2VHSjZ4QUJOYktyUnFtOEVDc0RTd2ZyZENZcFZGYk82REpnMlRjbFVyUFNteHhvYmU3ZGhvL0dMTkV6MTFFcnZ3SGlSeHhETVdNQ3h3MEwycUt0bnpzdTA1MVRYdmFwcGtQOENBVVk3Tjl3OUhteHczejEzNzVBbHl4TmtucDVqUjk2OFg0YmllOVA3eVBVc2ZjUnlsL1BaS1F2WjRKc0FIT2U4MDNya0FBQUE9IiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0.Hq9jKAgYWJdRDlf69SgZTcZkmU5_87v8SjtOo6dOBhkW_b6LgXVePjQI-LMmPgRs3hls5pukoyGl9NdyHkPFFA',
    )
    tier_11_weapon = CustomItem(
        'Tier 11 Weapon',
        'golden_sword',
        ItemRarity.EPIC,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 2)],
        buffs=[Buff(BuffType.power, 45)],
        quote=weapon_ability_quote(11),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTlRRdUNRQmlFcDVJeXZYVHIyay9vUTBtUEltWmVESFE3TDYvdEpndCtvZXZCZjU4VXpXa2VHSjZ4Z0MwMjlOS3FiUVlMd05LRVViZENZcFZIYk82REpvMHRGYXBTZWxMQ3dKcnFkbXcwZnJIbmlaNDZDVHU4QjJrYzhad0ZEQXZzZGEvS1V2YjgzZmFjcW9wM0ZVMnlIMkRDZkkvTjl3K0hDemx1VWJpWG95ZklFU2Vmbk5lTXZuODlDOGYxcFBlWDcxaVd4SEdVOGRzekRWbnlTSUVQOFJQR01ya0FBQUE9IiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0.834fypmomhsQNkTRvRY-MxQ_pVC09AyeuiBAKNEwymZiMRt7HpiM2N9GgTFmc_eRSzKHqXBtqUIfuJw3ln3fxA',
    )
    tier_12_weapon = CustomItem(
        'Tier 12 Weapon',
        'stone_pickaxe',
        ItemRarity.EPIC,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 3), Enchantment('efficiency', 2)],
        buffs=[Buff(BuffType.power, 50)],
        quote=weapon_ability_quote(12),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTlBRK0NNQmlFejQ4b2ZneHVydjRFbFJKaEpBU1JCUk9zYy9OQ3EybUMxRUFaK1BjU2pUZmRrMXllV3dJTHpLbTAydFR0RXNEWXdmUmxwTUxrRnZPaHQ1WXNGbFRvU3R0ZXl5bG05REpkYmZITGVwalkvcTJ3aWk1aGxzVGl4a09PRWJhMjBjK25hc1RETklLcVNyd3I2bFhUd29IejZPcnZIM1l1TWE4b1BIZnZTMkx5RUJBckJ3eUMwMUV5ejFmK1g3N2hlWm9rY1M3Tzl5emk2VFVEUGtydmlkbTVBQUFBIiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0.jspCZkgP-KXZnyd4xfkciJr1Xg3OVvFL74ozuJweRQqNCSAUQ-XHjZF62c2UldVSSWVIz5FEO_qNG9oZLgsGPQ',
    )
    tier_13_weapon = CustomItem(
        'Tier 13 Weapon',
        'golden_pickaxe',
        ItemRarity.EPIC,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 4)],
        buffs=[Buff(BuffType.power, 55)],
        quote=weapon_ability_quote(13),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTlRRdUNRQmlFcHcvS2lxQmIxMzVDNVVwNkZESHpZbURiZVhsMXQxZ3dOM1E5K08rVG9qbk5BOE16UzJDQk9aVldtN3BkQWhnN21MNk1WSmpjWWo3MDFwTEZnZ3BkYWR0ck9jV01YcWFyTFg1WkR4UGJ2eFZXMFNYTWtsamNlTWd4d3RZMit2bFVqWGlZUmxCVmlYZEZ2V3BhT0hBZVhmMzl3ODRsNWhXRjUrNTlTVXdlQW1MbGdFRndPa3JtK2NyL3l6YzhUNU1renNYNW5rVTh2V2JBQjRJVGV6VzVBQUFBIiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0._lijkS0z5x-7pKsj0_UqGtzG0X-vNOwQ0TqqFc8iK2LYxqtX8FblyEB0RfSOFjS-0g3BUX-r9gBMfQMfcA_a1w',
    )
    tier_14_weapon = CustomItem(
        'Tier 14 Weapon',
        'iron_sword',
        ItemRarity.LEGENDARY,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 1)],
        buffs=[Buff(BuffType.power, 60)],
        quote=weapon_ability_quote(14),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTlRRdUNRQmlFcHcvS0NxSmIxMzVDNVVwNkZESHpZbURiZVhsMXQxZ3dOM1E5K08rVG9qbk5BOE16UzJDQk9aVldtN3BkQWhnN21MNk1WSmpjWWo3MDFwTEZnZ3BkYWR0ck9jV01YcWFyTFg1WkR4UGJ2eFZXMFNYTWtsamNlTWd4d3RZMit2bFVqWGlZUmxCVmlYZEZ2V3BhT0hBZVhmMzl3ODRsNWhXRjUrNTlTVXdlQW1MbGdFRndPa3JtK2NyL3l6YzhUNU1renNYNW5rVTh2V2JBQjVzUUhkdTVBQUFBIiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0.6aOYcF-QPGtkMYC8ZM3JdC7KcZLEQ4Gcb1Te-i8mibfKx3sQzp3abp6QQWcB5l90OJYJPWU-HCVXA2yzNjyomw',
    )
    tier_15_weapon = CustomItem(
        'Tier 15 Weapon',
        'golden_hoe',
        ItemRarity.LEGENDARY,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 6)],
        buffs=[Buff(BuffType.power, 65)],
        quote=weapon_ability_quote(15),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTlBRK0NNQmlFejQ4bzZxQ2JxejlCcFVRWUNVRmt3UVRyM0x6UWFwb2dOVkFHL3IxRTQwMzNKSmZubHNBQ2N5cXROblc3QkRCMk1IMFpxVEM1eFh6b3JTV0xCUlc2MHJiWGNvb1p2VXhYVy95eUhpYTJmeXVzb2t1WUpiRzQ4WkJqaEsxdDlQT3BHdkV3amFDcUV1K0tldFcwY09BOHV2cjdoNTFMekNzS3o5MzdrcGc4Qk1US0FZUGdkSlRNODVYL2wyOTRuaVpKbkl2elBZdDRlczJBRDFQczd6ZTVBQUFBIiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0.3om9til2AUW0YWPtSxE5VUbH_uiv-uQFCpFiTWH33cvUAzsI0xA4xRnEUNPLeYMExdCOtF0dwS3qudRjn1Hb9Q',
    )
    tier_16_weapon = CustomItem(
        'Tier 16 Weapon',
        'diamond_shovel',
        ItemRarity.LEGENDARY,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 3)],
        buffs=[Buff(BuffType.power, 70)],
        quote=weapon_ability_quote(16),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTlBRK0NNQmlFejQ4bzRPTG02azlRZ1Fnak1ZZ3VtR2lkbXhkYVNKTktDZFNCZnkvUmVOTTl5ZVU1RDNDeHBOSXEwL1FlZ0ttRCtjc0lpZGtqWldQdkxWbTRWQ2l0N0tERUhBdDZtWGRqOGN0Nm5OaWhsVmlkTGttZXBmekJFb1lKTnJaVGRTMDdYcG1PazlhODFUVElyb2NEcDNvMzN6OXNmUXJDb2dqOVhTUW9FUHVZZ25MRU9ENGVSQkJHTXZyTDEreCt6YkwwenMvUC9NU3V0eHo0QUNRUlZNSzVBQUFBIiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0.BnLyg25o67o4Be5HHSMzl2eD6197yayyjqfCd4kRYLHNksys5I2u_7oGok7XGsg7SAfOT8ks97CjFSSILEaeNg',
    )
    tier_17_weapon = CustomItem(
        'Tier 17 Weapon',
        'golden_axe',
        ItemRarity.LEGENDARY,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 4)],
        buffs=[Buff(BuffType.power, 75)],
        quote=weapon_ability_quote(17),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTlBRK0NNQmlFejQ4bzZxS1RxejlCcFVRWUNVRmt3UVRyM0x6UWFwb2dOVkFHL3IxRTQwMzNKSmZubHNBQ2N5cXROblc3QkRCMk1IMFpxVEM1eFh6b3JTV0xCUlc2MHJiWGNvb1p2VXhYVy95eUdTYTJmeXVzb2t1WUpiRzQ4WkJqaEsxdDlQT3BHdkV3amFDcUV1K0tldFcwY09BOHV2cjdoNTFMekNzS3o5MzdrcGc4Qk1US0FZUGdkSlRNODVYL2w2OTVuaVpKbkl2elBZdDRlczJBRCt6dHBpNjVBQUFBIiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0.tiZuCm5OgZh3XlY4lb1efKoStyXzLcQtUgcDprzOq2yLlUsE-7v8H6mjEikopxpGszC-Dn1AWLCfMo65pP_J0w',
    )
    tier_18_weapon = CustomItem(
        'Tier 18 Weapon',
        'diamond_sword',
        ItemRarity.MYTHIC,
        ItemType.Weapon,
        enchantments=[Enchantment('sharpness', 1)],
        buffs=[Buff(BuffType.power, 80)],
        quote=weapon_ability_quote(18),
        interaction_data_key='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJkYXRhIjoiSDRzSUFBQUFBQUFBL3pXTlRRdUNRQmlFcHcvSzZoSmR1dllUS2xmU280aVpGd1BienN1cnU4V0N1YUhyd1grZkZNMXBIaGllV1FJTHpLbTAydFR0RXNEWXdmUmxwTUxrRnZPaHQ1WXNGbFRvU3R0ZXl5bG05REpkYmZITFpwalkvcTJ3aWk1aGxzVGl4a09PRWJhMjBjK25hc1RETklLcVNyd3I2bFhUd29IejZPcnZIM1l1TWE4b1BIZnZTMkx5RUJBckJ3eUMwMUV5ejFmK1g3N21lWm9rY1M3Tzl5emk2VFVEUHZYdXdNQzVBQUFBIiwiaXNzIjoiOWNjZWM4YmYtNjBiOS00OTBjLWI2ZmYtZGRjOWI1Zjc0YWIzIiwidmVyc2lvbiI6MX0.OQsNqACc374WRN_dvPViEhIrFeg9_iIWGfy21rz-O2-9gV_cvXXkv1vzb0n05Ndo4lLdvuo4lUgTGlyJ8mp-HQ',
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

    tier_1_boots = CustomItem(
        'Tier 1 Boots',
        'leather_boots',
        ItemRarity.COMMON,
        ItemType.Armor,
        buffs=[Buff(BuffType.power, 0)],
    )
    tier_2_boots = CustomItem(
        'Tier 2 Boots',
        'leather_boots',
        ItemRarity.COMMON,
        ItemType.Armor,
        enchantments=[Enchantment('protection', 1)],
        buffs=[Buff(BuffType.power, 0)],
    )
    tier_3_boots = CustomItem(
        'Tier 3 Boots',
        'leather_boots',
        ItemRarity.COMMON,
        ItemType.Armor,
        enchantments=[Enchantment('protection', 2)],
        buffs=[Buff(BuffType.power, 0)],
    )
    tier_4_boots = CustomItem(
        'Tier 4 Boots',
        'leather_boots',
        ItemRarity.UNCOMMON,
        ItemType.Armor,
        enchantments=[Enchantment('protection', 3)],
        buffs=[Buff(BuffType.power, 0)],
    )
    tier_5_boots = CustomItem(
        'Tier 5 Boots',
        'chain_boots',
        ItemRarity.UNCOMMON,
        ItemType.Armor,
        buffs=[Buff(BuffType.power, 15)],
    )
    tier_6_boots = CustomItem(
        'Tier 6 Boots',
        'chain_boots',
        ItemRarity.UNCOMMON,
        ItemType.Armor,
        enchantments=[Enchantment('protection', 1)],
        buffs=[Buff(BuffType.power, 20)],
    )
    tier_7_boots = CustomItem(
        'Tier 7 Boots',
        'chain_boots',
        ItemRarity.RARE,
        ItemType.Armor,
        enchantments=[Enchantment('protection', 2)],
        buffs=[Buff(BuffType.power, 25)],
    )
    tier_8_boots = CustomItem(
        'Tier 8 Boots',
        'chain_boots',
        ItemRarity.RARE,
        ItemType.Armor,
        enchantments=[Enchantment('protection', 3)],
        buffs=[Buff(BuffType.power, 30)],
    )
    tier_9_boots = CustomItem(
        'Tier 9 Boots',
        'iron_boots',
        ItemRarity.RARE,
        ItemType.Armor,
        buffs=[Buff(BuffType.power, 50)],
    )
    tier_10_boots = CustomItem(
        'Tier 10 Boots',
        'iron_boots',
        ItemRarity.EPIC,
        ItemType.Armor,
        enchantments=[Enchantment('protection', 1)],
        buffs=[Buff(BuffType.power, 55)],
    )
    tier_11_boots = CustomItem(
        'Tier 11 Boots',
        'iron_boots',
        ItemRarity.EPIC,
        ItemType.Armor,
        enchantments=[Enchantment('protection', 2)],
        buffs=[Buff(BuffType.power, 60)],
    )
    tier_12_boots = CustomItem(
        'Tier 12 Boots',
        'iron_boots',
        ItemRarity.EPIC,
        ItemType.Armor,
        enchantments=[Enchantment('protection', 3)],
        buffs=[Buff(BuffType.power, 65)],
    )
    tier_13_boots = CustomItem(
        'Tier 13 Boots',
        'diamond_boots',
        ItemRarity.LEGENDARY,
        ItemType.Armor,
        buffs=[Buff(BuffType.power, 85)],
    )
    tier_14_boots = CustomItem(
        'Tier 14 Boots',
        'diamond_boots',
        ItemRarity.LEGENDARY,
        ItemType.Armor,
        enchantments=[Enchantment('protection', 1)],
        buffs=[Buff(BuffType.power, 90)],
    )
    tier_15_boots = CustomItem(
        'Tier 15 Boots',
        'diamond_boots',
        ItemRarity.LEGENDARY,
        ItemType.Armor,
        enchantments=[Enchantment('protection', 2)],
        buffs=[Buff(BuffType.power, 95)],
    )
    tier_16_boots = CustomItem(
        'Tier 16 Boots',
        'diamond_boots',
        ItemRarity.MYTHIC,
        ItemType.Armor,
        enchantments=[Enchantment('protection', 3)],
        buffs=[Buff(BuffType.power, 100)],
    )

    @staticmethod
    def boots() -> list[CustomItem]:
        return [
            Items.tier_1_boots,
            Items.tier_2_boots,
            Items.tier_3_boots,
            Items.tier_4_boots,
            Items.tier_5_boots,
            Items.tier_6_boots,
            Items.tier_7_boots,
            Items.tier_8_boots,
            Items.tier_9_boots,
            Items.tier_10_boots,
            Items.tier_11_boots,
            Items.tier_12_boots,
            Items.tier_13_boots,
            Items.tier_14_boots,
            Items.tier_15_boots,
            Items.tier_16_boots,
        ]

    long_leg_leggings = CustomItem(
        '&aLong Leg Leggings',
        'leather_pants',
        ItemRarity.EPIC,
        ItemType.Armor,
        quote='&8Super-deluxe, limited edition,\n&8unbreakable pants. Have fun!\n\n' + special_ability_quote(
            'worn',
            '&7Permanent&a +2 Jump Boost&7.',
        ),
        color='55FF55',
    )

    slash_cookie = CustomItem(
        '&6Cookies&7 (Right Click)',
        'cookie',
        ItemRarity.LEGENDARY,
        ItemType.Item,
        quote='&8Giving a&6 /cookie&8 helps us out a ton\n&8and is greatly appreciated! Love!\n\n' + special_ability_quote(
            'click',
            '&7Turns you into an amazing person.',
        ),
        is_cookie_item=True,
        unbreakable=False,
    )

    @classmethod
    def all(cls) -> Generator[CustomItem, None, None]:
        for item in cls.__dict__.values():
            if isinstance(item, CustomItem):
                yield item


for item in Items.all():
    item.item.save()


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
        self._execute = execute or self.teleport

    def teleport(self) -> None:
        teleport_player(self.coordinates)

    def apply(self) -> None:
        TELEPORTING_ID.value = self.id
        TELEPORTING_TIMER.value = self.delay + 1
        WaitingOnTeleportTitleActionBar.display()
        chat(IMPORTANT_MESSAGE_PREFIX + f'&eStand still! Teleporting to&a {self.name}&e in&c {self.delay} seconds&e.')

    def execute(self) -> None:
        self._execute()
        chat(IMPORTANT_MESSAGE_PREFIX + f'&eTeleported to&a {self.name}&e.')
        play_sound('Enderman Teleport')


class Teleports:
    SPAWN = Teleport(
        id=1,
        name='Spawn',
        delay=4,
        coordinates=(-0.5, 46, -40.5, -180, 0),
        execute=lambda: trigger_function('Move To Spawn'),
    )

    @classmethod
    def all(cls) -> Generator[Teleport, None, None]:
        for teleport in cls.__dict__.values():
            if isinstance(teleport, Teleport):
                yield teleport
