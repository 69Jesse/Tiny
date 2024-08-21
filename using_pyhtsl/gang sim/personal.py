from pyhtsl import (
    create_function,
    trigger_function,
    IfAnd,
    exit_function,
    DateUnix,
)

from stats import LOCATION_ID, BIG_LOCATION_ID, BIGGEST_LOCATION_ID

from locations import set_location_id
from title_action_bar import maybe_update_display_stats, display_action_bar_or_title


@create_function('Personal 1s')
def personal_every_second() -> None:
    ...

@create_function('Personal 4ticks')
def personal_every_4ticks() -> None:
    trigger_function(set_location_id)
    maybe_update_display_stats()
    trigger_function(display_action_bar_or_title)
