from pyhtsl import (
    create_function,
    PlayerHealth,
    PlayerMaxHealth,
    trigger_function,
    go_to_house_spawn,
    chat,
)
from stats.playerstats import (
    MAX_HEALTH,
    HEALTH,
    PLAYER_HEALTH,
)


@create_function('On Death')
def on_death() -> None:
    HEALTH.value = MAX_HEALTH
    PLAYER_HEALTH.value = PlayerMaxHealth
    PlayerHealth.value = PlayerMaxHealth
    go_to_house_spawn()
    chat('you died :(')
