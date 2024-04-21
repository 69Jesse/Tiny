from pyhtsl import (
    create_function,
    chat,
    trigger_function,
    IfAnd,
    Else,
)
from everything import GlobalStats


@create_function('Update Timer')
def update_timer() -> None:
    temp = GlobalStats.time_temp
    hour = GlobalStats.time_hour
    minutes = GlobalStats.time_minutes
    day = GlobalStats.time_day
    color = GlobalStats.time_color
    temp += 3
    with IfAnd(temp >= 25):
        temp -= 25
        minutes += 1
    with IfAnd(minutes >= 6):
        minutes -= 6
        hour += 1
    with IfAnd(hour >= 24):
        hour -= 24
        day += 1
        trigger_function(on_day_change)
    with IfAnd(hour >= 8, hour < 20):
        color.value = 6
    with Else:
        color.value = 7


@create_function('On Day Change')
def on_day_change() -> None:
    trigger_function(on_day_change_everyone, trigger_for_all_players=True)


@create_function('On Day Change Everyone')
def on_day_change_everyone() -> None:
    day = GlobalStats.time_day
    chat(f'&eDay {day} has started!')
