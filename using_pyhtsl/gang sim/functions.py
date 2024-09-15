from pyhtsl import (
    create_function,
    IfAnd,
    IfOr,
    Else,
    GroupPriority,
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
    Function,
    GlobalStat,
    TeamPlayers,
    PlayerStat,
    pause_execution,
    display_title,
    rename,
    change_player_group,
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
    BaseTurf,
    Turf1,
    Turf2,
    Turf3,
    EMPTY_TURF_GANG,
    LATEST_DEATH_TIME,
    LATEST_DEATH_PLAYER_ID,
    LATEST_DEATH_GANG,
    LATEST_DEATH_WAS_LEADER,
    LATEST_DEATH_FUNDS,
    LATEST_DEATH_CRED,
    PLAYER_ID,
    PLAYER_GANG,
    PLAYER_LAST_GANG,
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
    GLOBAL_DISPLAY_ARG_1,
    GLOBAL_DISPLAY_ARG_2,
    GLOBAL_DISPLAY_ARG_3,
    GLOBAL_DISPLAY_ARG_4,
    GLOBAL_DISPLAY_ARG_5,
    GLOBAL_DISPLAY_ARG_6,
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
    TURF_DEFAULT_MAX_HP,
    PAYOUT_GANG,
    PAYOUT_REST,
    PAYOUT_WHOLE,
    PLAYTIME_SECONDS,
    PLAYER_PRESTIGE,
    TURF_HP_PER_PRESTIGE,
    PLAYER_CURRENT_LEVEL,
    PLAYER_CURRENT_XP,
    PLAYER_CURRENT_REQUIRED_XP,
    PLAYER_GLOBAL_LEVEL,
    ALL_TEAMS,
    ALL_GANG_TEAMS,
    PLAYER_KILL_STREAK,
    ADD_EXPERIENCE,
    PLAYER_KILLS,
    PLAYER_DEATHS,
    PLAYER_HIGHEST_KILL_STREAK,
)
from locations import LOCATIONS, LocationInstances
from everything import Items, BuffType
from currency import add_funds
from title_action_bar import (
    get_title_action_bars,
    TurfDestroyedTitleActionBar,
    TurfCapturedTitleActionBar,
    OnDeathTitleActionBar,
    OnKillTitleActionBar,
    OnBadKillTitleActionBar,
)


"""
TODO
[ ] potion effects
[ ] all armor
[ ] gang leader system
[ ] add all locations
[ ] on turf location enter display some message if turf is owned
"""


def play_unable_sound() -> None:
    play_sound('Note Bass Guitar')


# JOIN / LEAVE ========================================================


# NOTE have this get called by the actual event
@create_function('On Player Join')
def on_player_join() -> None:
    with IfAnd(
        GroupPriority < 20,
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
    PLAYER_CRED.value = 10
    PLAYER_FUNDS.value = 100


# DEATH / KILLS ======================================================================


# NOTE have this get called by the actual event
# Seems to consistently be ran BEFORE Player Kill event so thats really nice
@create_function('On Player Death')
def on_player_death() -> None:
    LATEST_DEATH_TIME.value = DateUnix
    LATEST_DEATH_PLAYER_ID.value = PLAYER_ID
    LATEST_DEATH_GANG.value = PLAYER_GANG
    with IfAnd(
        TEAM_LEADER_ID == PLAYER_ID,
    ):
        LATEST_DEATH_WAS_LEADER.value = 1
    with Else:
        LATEST_DEATH_WAS_LEADER.value = 0
    LATEST_DEATH_CRED.value = PLAYER_CRED
    LATEST_DEATH_FUNDS.value = PLAYER_FUNDS

    PLAYER_DEATHS.value += 1

    removing_cred = PlayerStat('temp')
    removing_cred.value = 1
    for cred_req in (
        # RULES:
        # 25 or less cred = -1 cred
        25,  # 26 - 100 cred = -2 cred
        100,  # 101 - 250 cred = -3 cred
        250,  # 251 - 500 cred = -4 cred
        500,  # 501 or more cred = -5 cred
    ):
        with IfAnd(
            PLAYER_CRED > cred_req,
        ):
            removing_cred.value += 1
    PLAYER_CRED.value -= removing_cred

    trigger_function(move_to_spawn)
    OnDeathTitleActionBar.apply(
        removing_cred,
        PLAYER_KILL_STREAK,
    )
    PLAYER_KILL_STREAK.value = 0


# NOTE have this get called by the actual event
@create_function('On Player Kill')
def on_player_kill() -> None:
    PLAYER_KILLS.value += 1
    PLAYER_KILL_STREAK.value += 1
    with IfAnd(
        PLAYER_KILL_STREAK > PLAYER_HIGHEST_KILL_STREAK,
    ):
        PLAYER_HIGHEST_KILL_STREAK.value = PLAYER_KILL_STREAK

    with IfAnd(
        PLAYER_GANG == SpawnTeam.ID,
    ):
        exit_function()

    # RULES:
    # ON BAD KILL: (killed person from same gang)
    #    -5 cred if wasnt leader
    #    -3 cred if was leader because its funny
    #    no rewards
    # ON GOOD KILL:
    #    + (
    #        min(3 + killstreak/5, 10) + prestige
    #    ) xp  -> +3xp to +10xp
    #    + (10 + prestige) funds
    #    + 3 cred
    #    if was leader:
    #        xp doubled
    #        funds doubled
    #        + 5 cred

    with IfAnd(
        PLAYER_GANG == LATEST_DEATH_GANG,
    ):
        trigger_function(on_bad_player_kill)
        exit_function()

    added_funds = PlayerStat('temp1')
    added_cred = PlayerStat('temp2')

    ADD_EXPERIENCE.value = 3 + (PLAYER_KILL_STREAK // 5)
    with IfAnd(
        ADD_EXPERIENCE > 10,
    ):
        ADD_EXPERIENCE.value = 10
    ADD_EXPERIENCE.value += PLAYER_PRESTIGE

    added_funds.value = 10 + PLAYER_PRESTIGE
    added_cred.value = 3

    with IfAnd(
        LATEST_DEATH_WAS_LEADER == 1,
    ):
        ADD_EXPERIENCE.value *= 2
        added_funds.value *= 2
        added_cred.value = 5

    trigger_function(add_experience)
    PLAYER_FUNDS.value += added_funds
    PLAYER_CRED.value += added_cred
    OnKillTitleActionBar.apply(
        added_funds,
        added_cred,
        ADD_EXPERIENCE,
    )


@create_function('On Bad Player Kill')
def on_bad_player_kill() -> None:
    removed_cred = PlayerStat('temp2')
    with IfAnd(
        LATEST_DEATH_WAS_LEADER == 1,
    ):
        removed_cred.value = 3
    with Else:
        removed_cred.value = 5
    PLAYER_CRED.value -= removed_cred
    OnBadKillTitleActionBar.apply(removed_cred)


# MISC?? =================================


@create_function('Apply Potion Effects')
def apply_potion_effects() -> None:
    pass  # TOOD night vision forever, strength etc


@create_function('Set Group')
def set_group() -> None:
    with IfAnd(
        GroupPriority >= 18,
    ):
        exit_function()
    with IfAnd(
        TEAM_LEADER_ID == PLAYER_ID,
    ):
        change_player_group(
            'Leader',
            False,
        )
        exit_function()
    for name, cred_req in (
        ('1000 Cred', 1000),
        ('500 Cred', 500),
        ('250 Cred', 250),
        ('150 Cred', 150),
        ('100 Cred', 100),
        ('75 Cred', 75),
        ('50 Cred', 50),
        ('40 Cred', 40),
        ('30 Cred', 30),
        ('25 Cred', 25),
        ('20 Cred', 20),
        ('15 Cred', 15),
        ('10 Cred', 10),
        ('5 Cred', 5),
        ('1 Cred', 1),
    ):
        with IfAnd(
            PLAYER_CRED >= cred_req,
        ):
            change_player_group(
                name,
                False,
            )
            exit_function()
    change_player_group(
        '0 Cred',
        False,
    )


TEMPORARY_SPAWN = (-2.5, 106.0, -40.5)


def ON_TEAM_JOIN(
    team: type[GangSimTeam],
) -> None:
    set_player_team(team.TEAM)
    trigger_function(check_player_gang)
    teleport_player(TEMPORARY_SPAWN)
    play_sound('Enderman Teleport')
    # TODO


@create_function('On Bloods Join')
def on_bloods_join() -> None:
    ON_TEAM_JOIN(Bloods)
@create_function('On Crips Join')
def on_crips_join() -> None:
    ON_TEAM_JOIN(Crips)
@create_function('On Kings Join')
def on_kings_join() -> None:
    ON_TEAM_JOIN(Kings)
@create_function('On Grapes Join')
def on_grapes_join() -> None:
    ON_TEAM_JOIN(Grapes)
@create_function('On Guards Join')
def on_guards_join() -> None:
    ON_TEAM_JOIN(Guards)


# NOTE have this get called by the actual event
@create_function('On Portal Enter')
def on_portal_enter() -> None:
    trigger_function(set_location_id)
    for location, function in (
        (LocationInstances.spawn_bloods_area, on_bloods_join),
        (LocationInstances.spawn_crips_area, on_crips_join),
        (LocationInstances.spawn_kings_area, on_kings_join),
        (LocationInstances.spawn_grapes_area, on_grapes_join),
        (LocationInstances.spawn_guards_area, on_guards_join),
    ):
        with IfAnd(
            LOCATION_ID == location.id
        ):
            trigger_function(function)


@create_function('Move To Spawn')
def move_to_spawn() -> None:
    set_player_team(SpawnTeam.TEAM)
    PLAYER_GANG.value = EMPTY_TURF_GANG
    teleport_player(SPAWN)
    play_sound('Enderman Teleport')


@create_function('Check Out Of Spawn')
def check_out_of_spawn() -> None:
    with IfAnd(
        GroupPriority >= 19
    ):
        exit_function()

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
        GroupPriority >= 18
    ):
        exit_function()

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


@create_function('Check Levels')
def check_levels() -> None:
    PLAYER_GLOBAL_LEVEL.value = -len(ALL_TEAMS) + 1
    PLAYER_CURRENT_LEVEL.value = 0
    PLAYER_CURRENT_XP.value = 0
    for team in ALL_TEAMS:
        with IfAnd(
            team.LEVEL <= 0,
        ):
            team.LEVEL.value = 1
        with IfAnd(
            PLAYER_GANG == team.ID,
        ):
            PLAYER_CURRENT_LEVEL.value = team.LEVEL
            PLAYER_CURRENT_XP.value = team.EXPERIENCE
        PLAYER_GLOBAL_LEVEL.value += team.LEVEL

    PLAYER_CURRENT_REQUIRED_XP.value = PLAYER_CURRENT_LEVEL * 100
    with IfAnd(
        PLAYER_CURRENT_XP >= PLAYER_CURRENT_REQUIRED_XP,
    ):
        trigger_function(level_up)


@create_function('Add Experience')
def add_experience() -> None:
    """Make sure to set ADD_EXPERIENCE before triggering this"""
    for team in ALL_TEAMS:
        with IfAnd(
            PLAYER_GANG == team.ID,
        ):
            team.EXPERIENCE.value += ADD_EXPERIENCE
            PLAYER_CURRENT_XP.value = team.EXPERIENCE


@create_function('Level Up')
def level_up() -> None:
    for team in ALL_TEAMS:
        with IfAnd(
            PLAYER_GANG == team.ID,
        ):
            team.LEVEL.value += 1
            team.EXPERIENCE.value -= PLAYER_CURRENT_REQUIRED_XP
            PLAYER_CURRENT_LEVEL.value = team.LEVEL
            PLAYER_CURRENT_XP.value = team.EXPERIENCE
    
    PLAYER_CURRENT_REQUIRED_XP.value = PLAYER_CURRENT_LEVEL * 100


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


@create_function('Remove Illegal Items')
def remove_illegal_items() -> None:
    pass  # TODO remove leader helmet if youre not leader + other gang armor


@create_function('Check Player Gang')
def check_player_gang() -> None:
    with IfOr(*(
        RequiredTeam(team.TEAM)
        for team in ALL_TEAMS
    )):
        PLAYER_GANG.value = TEAM_ID
    with IfOr(*(
        PLAYER_GANG == team.ID
        for team in ALL_TEAMS
    )):
        pass
    with Else:
        trigger_function(move_to_spawn)
    with IfAnd(
        PLAYER_GANG == SpawnTeam.ID
    ):
        pass
    with Else:
        PLAYER_LAST_GANG.value = PLAYER_GANG
    trigger_function(remove_illegal_items)


def set_team_ids() -> None:
    for team in ALL_TEAMS:
        team.TEAM.stat('id').value = team.ID


def quiet_reset_turf(turf: type[BaseTurf]) -> None:
    turf.GANG.value = EMPTY_TURF_GANG
    turf.FUNDS.value = 0
    turf.FUNDS_PER_SECOND.value = 0


def UPDATE_TURF(turf: type[BaseTurf]) -> None:
    turf.HIT_COOLDOWN -= 1
    turf.HEAL_COOLDOWN -= 1

    with IfOr(*(
        turf.GANG == gang_number
        for gang_number in (
            Bloods.ID,
            Crips.ID,
            Kings.ID,
            Grapes.ID,
        )
    )):
        pass
    with Else:
        quiet_reset_turf(turf)
        exit_function()

    for team in ALL_GANG_TEAMS:
        with IfAnd(
            turf.GANG == team.ID
        ):
            turf.MEMBERS.value = team.TEAM.players()

    with IfAnd(
        turf.MEMBERS <= 0,
    ):
        exit_function()

    with IfAnd(
        turf.HEAL_COOLDOWN <= 0,
    ):
        add_hp = turf.MAX_HP // 20
        turf.HP.value += add_hp
        turf.HEAL_COOLDOWN.value = 4
    with IfAnd(
        turf.HP > turf.MAX_HP,
    ):
        turf.HP.value = turf.MAX_HP

    turf.HELD_FOR += 1
    turf.FUNDS_PER_SECOND.value = turf.DEFAULT_FUNDS_PER_SECOND
    for amount in (200, 400, 800, 1200):
        with IfAnd(
            turf.HELD_FOR >= amount
        ):
            turf.FUNDS_PER_SECOND.value += turf.DEFAULT_FUNDS_PER_SECOND
    turf.FUNDS.value += turf.FUNDS_PER_SECOND


@create_function('Update Turf 1')
def update_turf_1() -> None:
    UPDATE_TURF(Turf1)
@create_function('Update Turf 2')
def update_turf_2() -> None:
    UPDATE_TURF(Turf2)
@create_function('Update Turf 3')
def update_turf_3() -> None:
    UPDATE_TURF(Turf3)


@create_function('Add Onto Turf Max HP')
def add_onto_turf_max_hp() -> None:
    with IfAnd(
        PLAYER_GANG == EMPTY_TURF_GANG
    ):
        exit_function()
    max_hp_addition = PlayerStat('temp')
    max_hp_addition.value = PLAYER_PRESTIGE * TURF_HP_PER_PRESTIGE
    for turf in (Turf1, Turf2, Turf3):
        with IfAnd(
            turf.GANG == PLAYER_GANG
        ):
            turf.MAX_HP += max_hp_addition


@create_function('Update Turfs')
def update_turfs() -> None:
    # set max hp
    Turf1.MAX_HP.value = TURF_DEFAULT_MAX_HP
    Turf2.MAX_HP.value = TURF_DEFAULT_MAX_HP
    Turf3.MAX_HP.value = TURF_DEFAULT_MAX_HP
    trigger_function(add_onto_turf_max_hp, trigger_for_all_players=True)

    # reset / heal, add held for and funds
    trigger_function(update_turf_1)
    trigger_function(update_turf_2)
    trigger_function(update_turf_3)

    # check duplicates
    with IfAnd(
        Turf2.GANG == Turf3.GANG,
    ):
        quiet_reset_turf(Turf3)
    with IfAnd(
        Turf1.GANG == Turf3.GANG,
    ):
        quiet_reset_turf(Turf3)
    with IfAnd(
        Turf1.GANG == Turf2.GANG,
    ):
        quiet_reset_turf(Turf2)


# LOOPS ==========================================================


# NOTE have this run every 20 ticks
@create_function('Personal 1s')
def personal_every_second() -> None:
    PLAYTIME_SECONDS.value += 1


# NOTE have this run every 4 ticks
@create_function('Personal 0.2s')
def personal_every_4ticks() -> None:
    trigger_function(check_player_gang)
    trigger_function(set_location_id)
    trigger_function(check_out_of_spawn)
    trigger_function(check_levels)
    trigger_function(set_most_stats)
    trigger_function(update_display_stats)
    trigger_function(display_action_bar_and_title)


# NOTE have this run every 4 ticks
@create_function('Global 1s')
def global_every_second() -> None:
    with IfAnd(DateUnix <= LAST_UNIX):
        exit_function()
    LAST_UNIX.value = DateUnix
    trigger_function(update_turfs)
    trigger_function(update_timer)
    trigger_function(check_cookie_goal)
    set_team_ids()


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
        trigger_function(destroy_cookie_goal)
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


@create_function('Destroy Cookie Goal')
def destroy_cookie_goal() -> None:
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
    chat('&aYou received&e +1,000⛁ Funds&7 (will change soon)')
    add_funds(1000)


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
    modulo_by = 5
    did_modulo_on = PlayerStat('temp')
    did_modulo_on.value = DateUnix
    did_modulo_on.value -= did_modulo_on // modulo_by * modulo_by
    with IfAnd(
        did_modulo_on == 0,
    ):
        display_action_bar(
            f'&6&l{PLAYER_KILL_STREAK}&6-Streak&7 (&a{PLAYER_KILLS}K&7/&c{PLAYER_DEATHS}D&7)&3 {PLAYER_CURRENT_XP}/{PLAYER_CURRENT_REQUIRED_XP}xp'
        )
        exit_function()

    for display_arg, turf_gang_args in (
        (DISPLAY_ARG_1, (Turf1.GANG, Turf2.GANG, Turf3.GANG)),
        (DISPLAY_ARG_2, (Turf1.GANG, Turf2.GANG)),
        (DISPLAY_ARG_3, (Turf1.GANG,)),
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
        if action_bar.is_regular():
            with IfAnd(action_bar.get_condition()):
                action_bar.display()
        else:
            action_bar.display_irregular()


# TURFS ===============================


@create_function('Apply Turf Destroyed Title')
def apply_turf_destroyed_title() -> None:
    TurfDestroyedTitleActionBar.apply(0)


@create_function('Apply Turf Captured Title')
def apply_turf_captured_title() -> None:
    TurfCapturedTitleActionBar.apply()


@create_function('Payout Turf Funds')
def payout_turf_funds() -> None:
    with IfAnd(
        PLAYER_GANG == PAYOUT_GANG,
    ):
        pass
    with Else:
        exit_function()
    payout = PlayerStat('temp')
    payout.value = PAYOUT_WHOLE
    with IfAnd(
        PAYOUT_REST > 0,
    ):
        PAYOUT_REST.value -= 1
        payout += 1

    is_leader = TEAM_LEADER_ID == PLAYER_ID
    with IfAnd(
        is_leader,
    ):
        payout.value += PAYOUT_WHOLE
    with IfAnd(
        PAYOUT_REST > 0,
        is_leader,
    ):
        PAYOUT_REST.value -= 1
        payout += 1

    with IfAnd(
        payout > 0,
    ):
        add_funds(payout)


def DESTROY_TURF(turf: type[BaseTurf]) -> None:
    TurfDestroyedTitleActionBar.apply_globals(
        turf.ID,
        turf.GANG,
        PLAYER_ID,
        PLAYER_GANG,
        turf.FUNDS,
        turf.HELD_FOR,
    )
    trigger_function(apply_turf_destroyed_title, trigger_for_all_players=True)
    TurfDestroyedTitleActionBar.apply(turf.FUNDS)
    turf.GANG.value = EMPTY_TURF_GANG
    PLAYER_FUNDS.value += turf.FUNDS
    turf.FUNDS.value = 0
    turf.HP.value = TURF_DEFAULT_MAX_HP
    turf.MAX_HP.value = TURF_DEFAULT_MAX_HP
    turf.FUNDS.value = 0
    turf.FUNDS_PER_SECOND.value = 0
    turf.HELD_FOR.value = 0
    turf.HIT_COOLDOWN.value = 6


def CLAIM_TURF(turf: type[BaseTurf]) -> None:
    with IfOr(*(
        PLAYER_GANG == team.ID
        for team in ALL_GANG_TEAMS
    )):
        pass
    with Else:
        chat(IMPORTANT_MESSAGE_PREFIX + '&cFailed to capture. You must be part of a gang to capture turf.')
        play_unable_sound()
        exit_function()

    def cannot_downgrade() -> None:
        chat(IMPORTANT_MESSAGE_PREFIX + '&cFailed to capture. You cannot downgrade your gangs turf.')
        play_unable_sound()
        exit_function()

    if turf.ID == Turf2.ID:
        with IfAnd(
            Turf1.GANG == PLAYER_GANG,
        ):
            cannot_downgrade()
    elif turf.ID == Turf3.ID:
        with IfAnd(
            Turf1.GANG == PLAYER_GANG,
        ):
            cannot_downgrade()
        with IfAnd(
            Turf2.GANG == PLAYER_GANG,
        ):
            cannot_downgrade()

    did_promote = PlayerStat('temp')
    did_promote.value = 0

    if turf.ID == Turf2.ID:
        with IfAnd(
            Turf3.GANG == PLAYER_GANG
        ):
            did_promote.value = 1
    elif turf.ID == Turf1.ID:
        with IfAnd(
            Turf2.GANG == PLAYER_GANG
        ):
            did_promote.value = 1
        with IfAnd(
            Turf3.GANG == PLAYER_GANG
        ):
            did_promote.value = 1

    turf.GANG.value = PLAYER_GANG
    turf.HELD_FOR.value = 0
    turf.HP.value = TURF_DEFAULT_MAX_HP
    turf.MAX_HP.value = TURF_DEFAULT_MAX_HP
    turf.FUNDS.value = 0
    turf.FUNDS_PER_SECOND.value = turf.DEFAULT_FUNDS_PER_SECOND
    TurfCapturedTitleActionBar.apply_globals(
        turf.ID,
        turf.GANG,
        PLAYER_ID,
        turf.FUNDS_PER_SECOND,
        did_promote,
    )
    turf.HIT_COOLDOWN.value = 6
    trigger_function(apply_turf_captured_title, trigger_for_all_players=True)


def ON_CLICK_TURF(
    turf: type[BaseTurf],
    claim_turf: Function,
    destroy_turf: Function,
) -> None:
    with IfAnd(
        turf.GANG == PLAYER_GANG
    ):
        # clicked own gang turf, claim funds
        PAYOUT_GANG.value = turf.GANG
        members_plus_1 = PlayerStat('temp')
        members_plus_1.value = turf.MEMBERS + 1
        PAYOUT_WHOLE.value = turf.FUNDS // members_plus_1
        PAYOUT_REST.value = turf.FUNDS - (PAYOUT_WHOLE * members_plus_1)
        turf.FUNDS.value = 0
        turf.HELD_FOR.value = 0
        trigger_function(payout_turf_funds, trigger_for_all_players=True)
        exit_function()

    with IfAnd(
        turf.HIT_COOLDOWN > 0
    ):
        exit_function()

    def cannot_downgrade() -> None:
        chat(IMPORTANT_MESSAGE_PREFIX + '&cFailed to damage. You cannot downgrade your gangs turf.')
        play_unable_sound()
        exit_function()

    if turf.ID == Turf2.ID:
        with IfAnd(
            turf.GANG == EMPTY_TURF_GANG,
            Turf1.GANG == PLAYER_GANG,
        ):
            cannot_downgrade()
    elif turf.ID == Turf3.ID:
        with IfAnd(
            turf.GANG == EMPTY_TURF_GANG,
            Turf1.GANG == PLAYER_GANG,
        ):
            cannot_downgrade()
        with IfAnd(
            turf.GANG == EMPTY_TURF_GANG,
            Turf2.GANG == PLAYER_GANG,
        ):
            cannot_downgrade()

    with IfAnd(
        turf.HP > 0
    ):
        trigger_function(set_most_stats)
        turf.HP.value -= PLAYER_DAMAGE
        turf.HEAL_COOLDOWN.value = 8
        play_sound('Zombie Metal', pitch=2.0)
    with IfAnd(
        turf.HP < 0
    ):
        turf.HP.value = 0

    with IfAnd(
        turf.HP > 0
    ):
        display_title(
            '&r',
            f'&c{turf.HP}/{turf.MAX_HP}❤ -{PLAYER_DAMAGE}',
            fadein=0,
            stay=1,
            fadeout=0,
        )
        exit_function()

    with IfAnd(
        turf.GANG == EMPTY_TURF_GANG
    ):
        trigger_function(claim_turf)
    with Else:
        trigger_function(destroy_turf)


@create_function('Destroy Turf 1')
def destroy_turf_1() -> None:
    DESTROY_TURF(Turf1)
@create_function('Try Claim Turf 1')
def claim_turf_1() -> None:
    CLAIM_TURF(Turf1)
@create_function('On Click Turf 1')
def on_click_turf_1() -> None:
    ON_CLICK_TURF(Turf1, claim_turf_1, destroy_turf_1)
@create_function('Destroy Turf 2')
def destroy_turf_2() -> None:
    DESTROY_TURF(Turf2)
@create_function('Try Claim Turf 2')
def claim_turf_2() -> None:
    CLAIM_TURF(Turf2)
@create_function('On Click Turf 2')
def on_click_turf_2() -> None:
    ON_CLICK_TURF(Turf2, claim_turf_2, destroy_turf_2)
@create_function('Destroy Turf 3')
def destroy_turf_3() -> None:
    DESTROY_TURF(Turf3)
@create_function('Try Claim Turf 3')
def claim_turf_3() -> None:
    CLAIM_TURF(Turf3)
@create_function('On Click Turf 3')
def on_click_turf_3() -> None:
    ON_CLICK_TURF(Turf3, claim_turf_3, destroy_turf_3)
