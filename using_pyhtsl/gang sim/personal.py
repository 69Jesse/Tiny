from pyhtsl import (
    create_function,
    trigger_function,
    IfAnd,
    exit_function,
    DateUnix,
)
from stats.globalstats import LAST_UNIX
from ingame_time import update_timer
from cookie_goal import check_cookie_goal


@create_function('Personal 1s')
def personal_every_second() -> None:
    ...

@create_function('Personal 4ticks')
def personal_every_4ticks() -> None:
    ...
