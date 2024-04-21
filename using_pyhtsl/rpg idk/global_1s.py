from pyhtsl import (
    create_function,
    chat,
    trigger_function,
    HouseCookies,
    IfAnd,
    exit_function,
)
from everything import GlobalStats


@create_function('Global 1s')
def global_every_second() -> None:
    pass
