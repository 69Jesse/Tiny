from pyhtsl import (
    create_function,
    chat,
    trigger_function,
    HouseCookies,
    IfAnd,
    exit_function,
)
from stats.globalstats import (
    LATEST_COOKIES,
    COOKIE_GOAL,
    COOKIES_NEEDED,
)


@create_function('Check Cookie Goal')
def check_cookie_goal() -> None:
    with IfAnd(
        LATEST_COOKIES > HouseCookies,
    ):
        trigger_function(reset_cookie_goal)
        exit_function()
    COOKIES_NEEDED.value = COOKIE_GOAL - LATEST_COOKIES
    trigger_function(cookie_receive_message, trigger_for_all_players=True)
    LATEST_COOKIES.value = HouseCookies
    with IfAnd(
        LATEST_COOKIES >= COOKIE_GOAL,
    ):
        trigger_function(increment_cookie_goal)
        trigger_function(cookie_reward, trigger_for_all_players=True)


@create_function('Reset Cookie Goal')
def reset_cookie_goal() -> None:
    COOKIE_GOAL.value = 0
    trigger_function(increment_cookie_goal)


@create_function('Increment Cookie Goal')
def increment_cookie_goal() -> None:
    COOKIE_GOAL.value += 5


@create_function('Cookie Receive Message')
def cookie_receive_message() -> None:
    with IfAnd(
        COOKIES_NEEDED <= 0,
    ):
        exit_function()
    chat('&eSomeone gave cookies! Thanks so much! We only')
    chat(f'&eneed&6 {COOKIES_NEEDED} &emore to hit the &6&lCookie Goal&e!')


@create_function('Cookie Reward')
def cookie_reward() -> None:
    chat('&eWe hit the &6&lCookie Goal&e! Here is your reward!')
