from pyhtsl import (
    create_function,
    chat,
    trigger_function,
    IfAnd,
    Else,
)
from stats.globalstats import (
    TIME_TEMP,
    TIME_HOUR,
    TIME_MINUTES,
    TIME_DAY,
    TIME_COLOR,
)


@create_function('Update Timer')
def update_timer() -> None:
    TIME_TEMP.value += 3
    with IfAnd(TIME_TEMP >= 25):
        TIME_TEMP.value -= 25
        TIME_MINUTES.value += 1
    with IfAnd(TIME_MINUTES >= 6):
        TIME_MINUTES.value -= 6
        TIME_HOUR.value += 1
    with IfAnd(TIME_HOUR >= 24):
        TIME_HOUR.value -= 24
        TIME_DAY.value += 1
        trigger_function(on_day_change)
    with IfAnd(TIME_HOUR >= 8, TIME_HOUR < 20):
        TIME_COLOR.value = 6
    with Else:
        TIME_COLOR.value = 7


@create_function('On Day Change')
def on_day_change() -> None:
    trigger_function(on_day_change_everyone, trigger_for_all_players=True)


@create_function('On Day Change Everyone')
def on_day_change_everyone() -> None:
    chat(f'&eDay {TIME_DAY} has started!')
