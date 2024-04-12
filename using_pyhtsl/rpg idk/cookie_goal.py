from pyhtsl import (
    create_function,
    chat,
    trigger_function,
    HouseCookies,
    IfAnd,
    exit_function,
)
from everything import GlobalStats


@create_function('Check Cookie Goal')
def check_cookie_goal() -> None:
    with IfAnd(
        GlobalStats.latest_cookies > HouseCookies,
    ):
        trigger_function(reset_cookie_goal)
    GlobalStats.cookies_needed.value = GlobalStats.cookie_goal - GlobalStats.latest_cookies
    trigger_function(cookie_receive_message, trigger_for_all_players=True)
    GlobalStats.latest_cookies.value = HouseCookies
    with IfAnd(
        GlobalStats.latest_cookies >= GlobalStats.cookie_goal,
    ):
        trigger_function(cookie_reward, trigger_for_all_players=True)


@create_function('Reset Cookie Goal')
def reset_cookie_goal() -> None:
    GlobalStats.cookie_goal.value = 0
    trigger_function(increment_cookie_goal)


@create_function('Increment Cookie Goal')
def increment_cookie_goal() -> None:
    GlobalStats.cookie_goal += 5


@create_function('Cookie Receive Message')
def cookie_receive_message() -> None:
    with IfAnd(
        GlobalStats.cookies_needed <= 0,
    ):
        exit_function()
    chat('&eSomeone gave cookies! Thanks so much! We only')
    chat(f'&eneed&6 {GlobalStats.cookies_needed} &emore to hit the &6&lCookie Goal&e!')


@create_function('Cookie Reward')
def cookie_reward() -> None:
    chat('&eWe hit the &6&lCookie Goal&e! Here is your reward!')
