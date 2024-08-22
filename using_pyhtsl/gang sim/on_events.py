from pyhtsl import (
    create_function,
    IfAnd,
    PlayerGroupPriority,
    set_player_team,
    reset_inventory,
)
from stats import PLAYER_ID, TOTAL_PLAYERS_JOINED, SpawnTeam


@create_function('On Player Join')
def on_player_join() -> None:
    with IfAnd(
        PlayerGroupPriority < 20,
        PLAYER_ID == 0,
    ):
        pass


@create_function('On Player Join First Time')
def on_player_join_first_time() -> None:
    TOTAL_PLAYERS_JOINED.value += 1
    PLAYER_ID.value = TOTAL_PLAYERS_JOINED
    set_player_team(SpawnTeam.TEAM)
    reset_inventory()
    


# Seems to consistently be ran BEFORE Player Kill event so thats really nice
@create_function('On Player Death')
def on_player_death() -> None:
    pass


@create_function('On Player Kill')
def on_player_kill() -> None:
    pass
