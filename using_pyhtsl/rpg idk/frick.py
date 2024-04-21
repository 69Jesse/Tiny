from pyhtsl import (
    Item,
    IfAnd,
    Enchantment,
    HasItem,
    chat,
)


for tier, pick in (
    (1, 'wooden_pickaxe'),
    (2, 'stone_pickaxe'),
    (3, 'iron_pickaxe'),
    (4, 'golden_pickaxe'),
    (5, 'diamond_pickaxe'),
):
    item = Item(
        pick,
        name=f'&bTier {tier} Pickaxe',
        lore='&6Shiny!\n\n&7Go mine some ores!',
        enchantments=[Enchantment('efficiency', tier)],
        hide_enchantments_flag=True,
    )
    with IfAnd(HasItem(item)):
        chat(f'&eYou have a Tier {tier} {item.as_title()}!')
