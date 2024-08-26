from pyhtsl import (
    create_function,
    IfAnd,
    IfOr,
    Else,
    PlayerGroupPriority,
    set_player_team,
    reset_inventory,
    DateUnix,
    trigger_function,
    RequiredTeam,
    exit_function,
    teleport_player,
    play_sound,
    chat,
    HouseCookies,
    display_action_bar,
    give_item,
)
from constants import (
    TOTAL_PLAYERS_JOINED,
    LAST_UNIX,
    LATEST_COOKIES,
    COOKIE_GOAL,
    COOKIES_NEEDED,
    TIME_TEMP,
    TIME_DAY,
    TIME_HOUR,
    TIME_MINUTES,
    TIME_COLOR,
    TURF_1_GANG,
    TURF_1_HELD_FOR,
    TURF_1_HP,
    TURF_1_MAX_HP,
    TURF_1_FUNDS,
    TURF_1_FUNDS_PER_SECOND,
    TURF_2_GANG,
    TURF_2_HELD_FOR,
    TURF_2_HP,
    TURF_2_MAX_HP,
    TURF_2_FUNDS,
    TURF_2_FUNDS_PER_SECOND,
    TURF_3_GANG,
    TURF_3_HELD_FOR,
    TURF_3_HP,
    TURF_3_MAX_HP,
    TURF_3_FUNDS,
    TURF_3_FUNDS_PER_SECOND,
    LATEST_DEATH_TIME,
    LATEST_DEATH_PLAYER_ID,
    LATEST_DEATH_GANG,
    LATEST_DEATH_WAS_LEADER,
    LATEST_DEATH_FUNDS,
    LATEST_DEATH_CRED,
    PLAYER_ID,
    PLAYER_GANG,
    PLAYER_CRED,
    PLAYER_FUNDS,
    PLAYER_POWER,
    PLAYER_MAX_POWER,
    PLAYER_MINING_SPEED,
    PLAYER_FORAGING_SPEED,
    PLAYER_MINING_FORTUNE,
    PLAYER_FARMING_FORTUNE,
    PLAYER_FORAGING_FORTUNE,
    PLAYER_DAMAGE,
    DISPLAY_ID,
    DISPLAY_TIMER,
    DISPLAY_ARG_1,
    DISPLAY_ARG_2,
    DISPLAY_ARG_3,
    LOCATION_ID,
    BIG_LOCATION_ID,
    BIGGEST_LOCATION_ID,
    PREVIOUS_LOCATION_ID,
    TEAM_ID,
    TEAM_LEADER_ID,
    GangSimTeam,
    Bloods,
    Crips,
    Kings,
    Grapes,
    Guards,
    SpawnTeam,
    SPAWN,
    SPAWN_WITH_ROTATION,
    IMPORTANT_MESSAGE_PREFIX,
)
from locations import LOCATIONS, LocationInstances
from everything import Items, BuffType
from currency import add_funds
from title_action_bar import get_title_action_bars


# JOIN / LEAVE ========================================================


# NOTE have this get called by the actual event
@create_function('On Player Join')
def on_player_join() -> None:
    with IfAnd(
        PlayerGroupPriority < 20,
        PLAYER_ID == 0,
    ):
        trigger_function(on_player_join_first_time)


@create_function('On Player Join First Time')
def on_player_join_first_time() -> None:
    TOTAL_PLAYERS_JOINED.value += 1
    PLAYER_ID.value = TOTAL_PLAYERS_JOINED
    set_player_team(SpawnTeam.TEAM)
    reset_inventory()
    give_item(Items.tier_1_weapon.item)


# DEATH / KILLS ======================================================================


# NOTE have this get called by the actual event
# Seems to consistently be ran BEFORE Player Kill event so thats really nice
@create_function('On Player Death')
def on_player_death() -> None:
    LATEST_DEATH_TIME.value = DateUnix
    LATEST_DEATH_PLAYER_ID.value = PLAYER_ID
    LATEST_DEATH_GANG.value = TEAM_ID
    with IfAnd(
        TEAM_LEADER_ID == PLAYER_ID,
    ):
        LATEST_DEATH_WAS_LEADER.value = 1
    with Else:
        LATEST_DEATH_WAS_LEADER.value = 0
    LATEST_DEATH_CRED.value = PLAYER_CRED
    LATEST_DEATH_FUNDS.value = PLAYER_FUNDS


# NOTE have this get called by the actual event
@create_function('On Player Kill')
def on_player_kill() -> None:
    pass


# MISC?? =================================


@create_function('Move To Spawn')
def move_to_spawn() -> None:
    set_player_team(SpawnTeam.TEAM)
    teleport_player(SPAWN)
    play_sound('Enderman Teleport')


@create_function('Check Out Of Spawn')
def check_out_of_spawn() -> None:
    with IfOr(
        BIGGEST_LOCATION_ID != LocationInstances.spawn.biggest_id,
        RequiredTeam(SpawnTeam.TEAM),
    ):
        pass
    with Else:
        # is at spawn without spawn team
        set_player_team(SpawnTeam.TEAM)
        exit_function()

    # is not at spawn or has spawn team

    with IfAnd(
        RequiredTeam(SpawnTeam.TEAM),
    ):
        pass
    with Else:
        exit_function()

    # has spawn team

    with IfOr(
        BIGGEST_LOCATION_ID != LocationInstances.spawn.biggest_id,
    ):
        # has spawn team outside of spawn
        trigger_function(move_to_spawn)


@create_function('Set Most Stats')
def set_most_stats() -> None:
    for buff_type in BuffType:
        if buff_type.stat is None:
            continue
        buff_type.stat.value = buff_type.min
    for item in Items.all():
        with item.if_has_condition():
            if item.buffs is None:
                continue
            if not item.buffs:
                continue
            for buff in item.buffs:
                if buff.type.stat is None:
                    continue
                buff.type.stat.value += round(buff.value)
    for buff_type in BuffType:
        if buff_type.max == -1:
            continue
        if buff_type.stat is None:
            continue
        with IfAnd(
            buff_type.stat > buff_type.max,
        ):
            buff_type.stat.value = buff_type.max


# LOOPS ==========================================================


# NOTE have this run every 20 ticks
@create_function('Personal 1s')
def personal_every_second() -> None:
    ...


# NOTE have this run every 4 ticks
@create_function('Personal 0.2s')
def personal_every_4ticks() -> None:
    trigger_function(set_location_id)
    trigger_function(check_out_of_spawn)
    trigger_function(update_display_stats)
    trigger_function(display_action_bar_and_title)


# NOTE have this run every 4 ticks
@create_function('Global 1s')
def global_every_second() -> None:
    with IfAnd(DateUnix <= LAST_UNIX):
        exit_function()
    LAST_UNIX.value = DateUnix
    trigger_function(update_timer)
    trigger_function(check_cookie_goal)


# LOCATIONS ========================================


@create_function('Set Location ID')
def set_location_id() -> None:
    LOCATION_ID.value = 0
    for location in LOCATIONS.walk():
        with location.if_inside_condition():
            LOCATION_ID.value = location.id
    BIG_LOCATION_ID.value = LOCATION_ID // 100
    BIGGEST_LOCATION_ID.value = BIG_LOCATION_ID // 100
    with IfOr(
        LOCATION_ID == 0,
        PREVIOUS_LOCATION_ID == LOCATION_ID,
    ):
        pass
    with Else:
        trigger_function(on_new_location_enter)
        PREVIOUS_LOCATION_ID.value = LOCATION_ID


@create_function('On New Location Enter')
def on_new_location_enter() -> None:
    pass



# COOKIE GOAL ===================================


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
    chat('&aYou received&e +100⛁ Funds&7 (will change soon)')
    add_funds(100)


# INGAME TIME ======================


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


@create_function('Once -> On Day Change')
def on_day_change() -> None:
    trigger_function(on_day_change_everyone, trigger_for_all_players=True)


@create_function('Everyone -> On Day Change')
def on_day_change_everyone() -> None:
    chat(f'&eDay {TIME_DAY} has started!')


# ACTION BAR / TITLE ====================


@create_function('Update Display Stats')
def update_display_stats() -> None:
    with IfAnd(
        DISPLAY_TIMER > 0,
    ):
        DISPLAY_TIMER.value -= 1
    with IfAnd(
        DISPLAY_TIMER <= 0,
    ):
        DISPLAY_ID.value = 0
        DISPLAY_TIMER.value = 0
        DISPLAY_ARG_1.value = 0
        DISPLAY_ARG_2.value = 0
        DISPLAY_ARG_3.value = 0


@create_function('Regular Action Bar Display')
def regular_action_bar_display() -> None:
    for display_arg, turf_gang_args in (
        (DISPLAY_ARG_1, (TURF_1_GANG, TURF_2_GANG, TURF_3_GANG)),
        (DISPLAY_ARG_2, (TURF_2_GANG, TURF_3_GANG)),
        (DISPLAY_ARG_3, (TURF_3_GANG,)),
    ):
        with IfOr(*(turf_gang_arg == TEAM_ID for turf_gang_arg in turf_gang_args)):
            display_arg.value = TEAM_ID
        with Else:
            display_arg.value = 7

    def display_with_location(location_name: str) -> None:
        display_action_bar(
            f'&b⏣ {location_name}&4 {PLAYER_POWER}/{PLAYER_MAX_POWER}⸎&{DISPLAY_ARG_1} &l✯&{DISPLAY_ARG_2}&l✯&{DISPLAY_ARG_3}&l✯',
        )

    visited_ids: set[int] = set()
    for location in LOCATIONS.walk():
        if location.id in visited_ids:
            continue
        visited_ids.add(location.id)
        with IfAnd(
            LOCATION_ID == location.id,
        ):
            display_with_location(location.name)
            exit_function()
    display_with_location('Unknown')


@create_function('Display Action Bar & Title')
def display_action_bar_and_title() -> None:
    with IfAnd(
        DISPLAY_ID == 0,
    ):
        trigger_function(regular_action_bar_display)
    for action_bar in get_title_action_bars():
        with IfAnd(
            DISPLAY_ID == action_bar.get_id(),
        ):
            action_bar.display()
