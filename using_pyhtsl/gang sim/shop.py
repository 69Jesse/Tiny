from pyhtsl import Item
from everything import Items


SHOP_ITEM_IDS: set[int] = set()
ALL_SHOP_ITEMS: list['ShopItem'] = []


class ShopItem:
    id: int
    item: Item
    funds_cost: int
    items_cost: list[tuple[Item, int]]
    def __init__(
        self,
        id: int,
        item: Item,
        funds_cost: int,
        items_cost: list[tuple[Item, int]]
    ) -> None:
        self.id = id
        self.item = item
        self.funds_cost = funds_cost
        self.items_cost = items_cost

        ALL_SHOP_ITEMS.append(self)
        if id in SHOP_ITEM_IDS:
            raise ValueError(f'Duplicate shop item id: {id}')
        SHOP_ITEM_IDS.add(id)

    def create_item(self) -> Item:
        item = self.item.copy()

        lines: list[str] = []
        if self.funds_cost > 0:
            lines.append(f'&6{self.funds_cost:,} Funds')
        for cost_item, count in self.items_cost:
            assert cost_item.name is not None
            line = cost_item.name
            if count > 1:
                line += f'&8 x{count:,}'
            lines.append(line)

        item.lore = ((item.lore or '').rstrip('\n') +
            '\n\n&7Cost\n' + '\n'.join(lines) + '\n\n&eClick to purchase!'
        ).lstrip('\n')

        return item


WEAPON_SHOP_ITEMS = [
    ShopItem(i, item.item, cost, [(prev_item.item, 1)] if prev_item is not None else [])
    for i, (item, prev_item, cost) in enumerate([
        (Items.tier_1_weapon, None,                    100,    ),
        (Items.tier_2_weapon, Items.tier_1_weapon,     1000,   ),
        (Items.tier_3_weapon, Items.tier_2_weapon,     2500,   ),
        (Items.tier_4_weapon, Items.tier_3_weapon,     5000,   ),
        (Items.tier_5_weapon, Items.tier_4_weapon,     7500,   ),
        (Items.tier_6_weapon, Items.tier_5_weapon,     10000,  ),
        (Items.tier_7_weapon, Items.tier_6_weapon,     15000,  ),
        (Items.tier_8_weapon, Items.tier_7_weapon,     20000,  ),
        (Items.tier_9_weapon, Items.tier_8_weapon,     30000,  ),
        (Items.tier_10_weapon, Items.tier_9_weapon,    40000,  ),
        (Items.tier_11_weapon, Items.tier_10_weapon,   55000,  ),
        (Items.tier_12_weapon, Items.tier_11_weapon,   70000,  ),
        (Items.tier_13_weapon, Items.tier_12_weapon,   90000,  ),
        (Items.tier_14_weapon, Items.tier_13_weapon,   110000, ),
        (Items.tier_15_weapon, Items.tier_14_weapon,   140000, ),
        (Items.tier_16_weapon, Items.tier_15_weapon,   180000, ),
        (Items.tier_17_weapon, Items.tier_16_weapon,   230000, ),
        (Items.tier_18_weapon, Items.tier_17_weapon,   300000, ),
    ])
]


BOOTS_SHOP_ITEMS = [
    ShopItem(100 + i, item.item, cost, [(prev_item.item, 1)] if prev_item is not None else [])
    for i, (item, prev_item, cost) in enumerate([
        (Items.tier_1_boots, None,                    100,    ),
        (Items.tier_2_boots, Items.tier_1_boots,      1500,   ),
        (Items.tier_3_boots, Items.tier_2_boots,      4000,   ),
        (Items.tier_4_boots, Items.tier_3_boots,      8000,   ),
        (Items.tier_5_boots, Items.tier_4_boots,      12000,  ),
        (Items.tier_6_boots, Items.tier_5_boots,      17000,  ),
        (Items.tier_7_boots, Items.tier_6_boots,      25000,  ),
        (Items.tier_8_boots, Items.tier_7_boots,      34000,  ),
        (Items.tier_9_boots, Items.tier_8_boots,      50000,  ),
        (Items.tier_10_boots, Items.tier_9_boots,     67000,  ),
        (Items.tier_11_boots, Items.tier_10_boots,    92000,  ),
        (Items.tier_12_boots, Items.tier_11_boots,    118000, ),
        (Items.tier_13_boots, Items.tier_12_boots,    151000, ),
        (Items.tier_14_boots, Items.tier_13_boots,    185000, ),
        (Items.tier_15_boots, Items.tier_14_boots,    235000, ),
        (Items.tier_16_boots, Items.tier_15_boots,    300000, ),
    ])
]



for item in ALL_SHOP_ITEMS:
    item.create_item().save()
