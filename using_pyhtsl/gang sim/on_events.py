from pyhtsl import (
    create_function,
)


@create_function('On Player Join')
def on_player_join() -> None:
    pass


# Seems to consistently be ran BEFORE Player Kill event so thats really nice
@create_function('On Player Death')
def on_player_death() -> None:
    pass


@create_function('On Player Kill')
def on_player_kill() -> None:
    pass
