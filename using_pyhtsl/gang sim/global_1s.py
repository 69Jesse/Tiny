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


# Have this run every 4 ticks
@create_function('Global 1s')
def global_every_second() -> None:
    with IfAnd(DateUnix <= LAST_UNIX):
        exit_function()
    LAST_UNIX.value = DateUnix
    trigger_function(update_timer)
    trigger_function(check_cookie_goal)
