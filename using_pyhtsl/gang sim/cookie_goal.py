from pyhtsl import (
    create_function,
    chat,
    trigger_function,
    HouseCookies,
    IfAnd,
    exit_function,
)
from stats import (
    LATEST_COOKIES,
    COOKIE_GOAL,
    COOKIES_NEEDED,
)
from misc import IMPORTANT_MESSAGE_PREFIX


@create_function('Check Cookie Goal')
def check_cookie_goal() -> None:
    with IfAnd(
        LATEST_COOKIES > HouseCookies,
    ):
        trigger_function(reset_cookie_goal)
        exit_function()

    with IfAnd(
        LATEST_COOKIES == HouseCookies,
    ):
        exit_function()

    LATEST_COOKIES.value = HouseCookies
    COOKIES_NEEDED.value = COOKIE_GOAL - LATEST_COOKIES
    trigger_function(cookie_receive_message, trigger_for_all_players=True)
    with IfAnd(
        LATEST_COOKIES >= COOKIE_GOAL,
    ):
        trigger_function(increment_cookie_goal)
        trigger_function(cookie_reward, trigger_for_all_players=True)


@create_function('Reset Cookie Goal')
def reset_cookie_goal() -> None:
    COOKIE_GOAL.value = 0
    LATEST_COOKIES.value = HouseCookies
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
    chat(IMPORTANT_MESSAGE_PREFIX + '&aSomeone gave cookies!&e Thank you&a so much!')
    chat(f'&aWe only need&6 {COOKIES_NEEDED}&a more to hit the&6 Cookie Goal&a!')


@create_function('Cookie Reward')
def cookie_reward() -> None:
    chat(IMPORTANT_MESSAGE_PREFIX + '&aWe hit the&6 Cookie Goal&a!&e Thank you&a so much!!')
    chat('&aYou received&e +10⛁ Funds&7 (will change soon)')
