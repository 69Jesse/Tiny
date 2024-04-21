from pyhtsl import (
    create_function,
    trigger_function,
    IfAnd,
    exit_function,
    DateUnix,
)
from everything import GlobalStats
from ingame_time import update_timer


# Have this run every 4 ticks
@create_function('Global 1s')
def global_every_second() -> None:
    last = GlobalStats.last_unix
    with IfAnd(last <= DateUnix):
        exit_function()
    last.value = DateUnix
    trigger_function(update_timer)
