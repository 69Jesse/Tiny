from pyhtsl import (
    create_function,
    chat,
    trigger_function,
    PlayerStat,
    GlobalStat,
)

@create_function('Reward')
def testing_1() -> None:
    reward = PlayerStat('reward')
    reward.value = 100
    multiplier = GlobalStat('multiplier')
    trigger_function(add_gold, parameters=(reward, multiplier))

@create_function('Add Gold')
def add_gold(
    reward: PlayerStat,
    multiplier: PlayerStat,
) -> None:
    gold = PlayerStat('gold')
    add = reward * multiplier
    gold += add
    chat(f'&eYou gained &6{add}g&e!')
