from pyhtsl import (
    create_function,
    PlayerHealth,
    PlayerMaxHealth,
    IfAnd,
    IfOr,
    Else,
    trigger_function,
    exit_function,
)
from stats.playerstats import (
    MAX_HEALTH,
    PLAYER_MAX_HEALTH,
    HEALTH,
    PLAYER_HEALTH,
)


@create_function('Set Most Stats')
def set_most_stats() -> None:
    trigger_function(set_player_health)


@create_function('Set Player Health')
def set_player_health() -> None:
    with IfAnd(MAX_HEALTH <= 300):
        PLAYER_MAX_HEALTH.value = 20 + (MAX_HEALTH - 100) // 10
    with Else:
        PLAYER_MAX_HEALTH.value = 40 + (MAX_HEALTH - 300) // 35

    with IfAnd(PLAYER_MAX_HEALTH < 20):
        PLAYER_MAX_HEALTH.value = 20
    PLAYER_MAX_HEALTH.value = PLAYER_MAX_HEALTH // 2 * 2
    with IfOr(PlayerMaxHealth != PLAYER_MAX_HEALTH):
        PlayerMaxHealth.value = PLAYER_MAX_HEALTH

    with IfAnd(HEALTH == 0):
        from on_death import on_death
        trigger_function(on_death)
        exit_function()
    PLAYER_HEALTH.value = HEALTH * PLAYER_MAX_HEALTH // MAX_HEALTH
    with IfAnd(PLAYER_HEALTH <= 0):
        PLAYER_HEALTH.value = 1
    with IfOr(PlayerHealth != PLAYER_HEALTH):
        PlayerHealth.value = PLAYER_HEALTH
