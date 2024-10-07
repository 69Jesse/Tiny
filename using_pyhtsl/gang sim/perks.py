from pyhtsl import Item, PlayerStat, delete_all_items_from_imports_folder, Enchantment
from pyhtsl.types import ALL_ITEM_KEYS
from constants import (
    SELECTED_PERK_A,
    SELECTED_PERK_B,
    PERK_1_TIER,
    PERK_2_TIER,
    PERK_3_TIER,
    PERK_4_TIER,
    PERK_5_TIER,
    PERK_6_TIER,
    PERK_7_TIER,
    PERK_8_TIER,
    PERK_9_TIER,
    PERK_1_COLOR,
    PERK_2_COLOR,
    PERK_3_COLOR,
    PERK_4_COLOR,
    PERK_5_COLOR,
    PERK_6_COLOR,
    PERK_7_COLOR,
    PERK_8_COLOR,
    PERK_9_COLOR,
)


class Perk:
    index: int
    item_key: ALL_ITEM_KEYS
    name: str
    description: str
    tiers: list[tuple[str, int]]
    unlocked_tier_stat: PlayerStat
    color_stat: PlayerStat
    def __init__(
        self,
        index: int,
        item_key: ALL_ITEM_KEYS,
        name: str,
        description: str,
        tiers: list[tuple[str, int]],
        unlocked_tier_stat: PlayerStat,
        color_stat: PlayerStat,
    ) -> None:
        self.index = index
        self.item_key = item_key
        self.name = name
        self.description = description
        self.tiers = tiers
        self.unlocked_tier_stat = unlocked_tier_stat
        self.color_stat = color_stat

    def item_last_line(
        self,
        last_line: str,
    ) -> Item:
        name = f'&e{self.index}. {self.name}'
        lore = self.description + f'\n\n&{self.color_stat}&lSELECTED\n\n&6Perk Tiers\n' + (
            '\n'.join(
                f'&a{i}. {desc}&7 (' + (f'&e{cost:,}⛁ Funds' if cost > 0 else '&a&lFREE') + '&7)'
                for i, (desc, cost) in enumerate(self.tiers, start=1)
            )
        ) + '\n\n' + (
            f'&6Unlocked Tier: &a{self.unlocked_tier_stat}'
        ) + '\n\n' + last_line
        return Item(self.item_key, name=name, lore=lore, hide_all_flags=True)

    @property
    def item_upgrade(self) -> Item:
        return self.item_last_line('&eClick to upgrade!')

    @property
    def item_select_or_upgrade(self) -> Item:
        return self.item_last_line('&eClick to select/upgrade!')


'''
1. regen on kill:
    1. +2 regen on kill for 4s   FREE
    2. +2 regen on kill for 5s   1,000 Funds
    3. +3 regen on kill for 4s   5,000 Funds
    4. +3 regen on kill for 5s   10,000 Funds
    5. +3 regen on kill for 6s   30,000 Funds

2. xp on kill:
    1. +1 xp on kill   FREE
    2. +2 xp on kill   5,000 Funds
    3. +3 xp on kill   50,000 Funds

3. funds on kill:
    1. +2 funds on kill   1,000 Funds
    2. +4 funds on kill   3,000 Funds
    3. +6 funds on kill   5,000 Funds

4. strength on kill:
    1. +1 strength on kill for 1s   5,000 Funds
    2. +1 strength on kill for 2s   10,000 Funds
    3. +1 strength on kill for 3s   15,000 Funds
    4. +1 strength on kill for 4s   20,000 Funds
    5. +1 strength on kill for 5s   25,000 Funds

5. speed:
    1. permanent +1 speed   20,000 Funds
    2. permanent +2 speed   1,000,000 Funds

6. max power on kill:
    1. restore power to max on kill   15,000 Funds

7. additional power:
    1. +20 power   1,000 Funds
    2. +40 power   2,500 Funds
    3. +60 power   5,000 Funds
    4. +80 power   10,000 Funds
    5. +100 power   30,000 Funds

8. more turf damage:
    1. +1 turf damage   1,000 Funds
    2. +2 turf damage   2,500 Funds
    3. +3 turf damage   5,000 Funds
    4. +4 turf damage   10,000 Funds
    5. +5 turf damage   30,000 Funds

9. extra distribution funds:
    1. +2% distribution funds   1,000 Funds
    2. +4% distribution funds   2,500 Funds
    3. +6% distribution funds   10,000 Funds
    4. +8% distribution funds   50,000 Funds
    5. +10% distribution funds   100,000 Funds
'''


ALL_PERKS: list[Perk] = [
    Perk(
        1,
        'golden_apple',
        'Regen On Kill',
        '&7Gain extra&d Regen&7 for a short period\n&7of time after killing a player.',
        [
            ('&d+2 Regen&7 for&b 4s', 0),
            ('&d+2 Regen&7 for&b 5s', 1000),
            ('&d+3 Regen&7 for&b 4s', 5000),
            ('&d+3 Regen&7 for&b 5s', 10000),
            ('&d+3 Regen&7 for&b 6s', 30000),
        ],
        PERK_1_TIER,
        PERK_1_COLOR,
    ),
    Perk(
        2,
        'cyan_dye',
        'Extra XP On Kill',
        '&7Gain extra&3 XP&7 after killing a player.',
        [
            ('&3+1 XP&7 on kill', 0),
            ('&3+2 XP&7 on kill', 5000),
            ('&3+3 XP&7 on kill', 50000),
        ],
        PERK_2_TIER,
        PERK_2_COLOR,
    ),
    Perk(
        3,
        'gold_ingot',
        'Extra Funds On Kill',
        '&7Gain extra&e Funds&7 after killing a player.',
        [
            ('&e+2⛁ Funds&7 on kill', 1000),
            ('&e+4⛁ Funds&7 on kill', 3000),
            ('&e+6⛁ Funds&7 on kill', 5000),
        ],
        PERK_3_TIER,
        PERK_3_COLOR,
    ),
    Perk(
        4,
        'redstone_dust',
        'Strength On Kill',
        '&7Gain extra&c Strength&7 for a short period\n&7of time after killing a player.',
        [
            ('&c+1 Strength&7 for&b 1s', 5000),
            ('&c+1 Strength&7 for&b 2s', 10000),
            ('&c+1 Strength&7 for&b 3s', 15000),
            ('&c+1 Strength&7 for&b 4s', 20000),
            ('&c+1 Strength&7 for&b 5s', 25000),
        ],
        PERK_4_TIER,
        PERK_4_COLOR,
    ),
    Perk(
        5,
        'iron_boots',
        'Permanent Speed',
        '&7Permanently gain extra&f Speed&7 effect.',
        [
            ('&7Permanent&f +1 Speed', 20000),
            ('&7Permanent&f +2 Speed', 1000000),
        ],
        PERK_5_TIER,
        PERK_5_COLOR,
    ),
    Perk(
        6,
        'rose_bush',
        'Max Power On Kill',
        '&7Restore your&4 Power&7 to max after killing a player.',
        [
            ('&7Max&4 Power&7 on kill', 15000),
        ],
        PERK_6_TIER,
        PERK_6_COLOR,
    ),
    Perk(
        7,
        'poppy',
        'Additional Power',
        '&7Permanently gain extra&4 Power&7.',
        [
            ('&4+20⸎ Power', 1000),
            ('&4+40⸎ Power', 2500),
            ('&4+60⸎ Power', 5000),
            ('&4+80⸎ Power', 10000),
            ('&4+100⸎ Power', 30000),
        ],
        PERK_7_TIER,
        PERK_7_COLOR,
    ),
    Perk(
        8,
        'wooden_axe',
        'Additional Turf Damage',
        '&7Deal extra&9 Turf Damage&7 to enemy turfs.',
        [
            ('&9+1 Turf Damage', 1000),
            ('&9+2 Turf Damage', 2500),
            ('&9+3 Turf Damage', 5000),
            ('&9+4 Turf Damage', 10000),
            ('&9+5 Turf Damage', 30000),
        ],
        PERK_8_TIER,
        PERK_8_COLOR,
    ),
    Perk(
        9,
        'gold_ore',
        'Extra Distribution Funds',
        '&7Gain extra&e Funds&7 from turf distributions.',
        [
            ('&e+2% Distribution Funds', 1000),
            ('&e+4% Distribution Funds', 2500),
            ('&e+6% Distribution Funds', 10000),
            ('&e+8% Distribution Funds', 50000),
            ('&e+10% Distribution Funds', 100000),
        ],
        PERK_9_TIER,
        PERK_9_COLOR,
    ),
]


def perk_block_lore(perk_stat: PlayerStat) -> str:
    whichone = '1st' if perk_stat is SELECTED_PERK_A else '2nd'
    lore = f'&7You can have&4 two&7 perks active at a time.\n&7Click to change your {whichone} selected perk.'
    lore += f'\n\n&6Selected Perk:&a {perk_stat}'
    lore += '\n\n&eClick to change!'
    return lore


PERK_A_ITEM = Item(
    'red_stained_clay',
    name='&eSelected Perk A',
    lore=perk_block_lore(SELECTED_PERK_A),
    hide_all_flags=True,
)
PERK_A_ITEM_ENCHANTED = PERK_A_ITEM.copy()
PERK_A_ITEM_ENCHANTED.enchantments = [Enchantment('infinity', 1)]


PERK_B_ITEM = Item(
    'blue_stained_clay',
    name='&eSelected Perk B',
    lore=perk_block_lore(SELECTED_PERK_B),
    hide_all_flags=True,
)
PERK_B_ITEM_ENCHANTED = PERK_B_ITEM.copy()
PERK_B_ITEM_ENCHANTED.enchantments = [Enchantment('infinity', 1)]


if __name__ == '__main__':
    delete_all_items_from_imports_folder()

    for perk in ALL_PERKS:
        perk.item_upgrade.save()
        # perk.item_select_or_upgrade.save()

    PERK_A_ITEM.save()
    PERK_A_ITEM_ENCHANTED.save()
    PERK_B_ITEM.save()
    PERK_B_ITEM_ENCHANTED.save()
