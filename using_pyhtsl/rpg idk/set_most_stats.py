from pyhtsl import (
    create_function,
    PlayerHealth,
    PlayerMaxHealth,
    IfAnd,
    IfOr,
    Else,
)
from stats.playerstats import (
    MAX_HEALTH,
    PLAYER_MAX_HEALTH,
    HEALTH,
    PLAYER_HEALTH,
)


@create_function('Set Most Stats')
def set_most_stats() -> None:
    set_player_max_health()
    set_player_health()


def set_player_max_health() -> None:
    with IfAnd(MAX_HEALTH <= 300):
        PLAYER_MAX_HEALTH.value = 20 + (MAX_HEALTH - 100) // 10
    with Else:
        PLAYER_MAX_HEALTH.value = 40 + (MAX_HEALTH - 300) // 35

    with IfAnd(PLAYER_MAX_HEALTH < 20):
        PLAYER_MAX_HEALTH.value = 20
    PLAYER_MAX_HEALTH.value = PLAYER_MAX_HEALTH // 2 * 2
    with IfOr(PlayerMaxHealth != PLAYER_MAX_HEALTH):
        PlayerMaxHealth.value = PLAYER_MAX_HEALTH


def set_player_health() -> None:
    PLAYER_HEALTH.value = HEALTH * PLAYER_MAX_HEALTH // MAX_HEALTH
    with IfOr(PlayerHealth != PLAYER_HEALTH):
        PlayerHealth.value = PLAYER_HEALTH
