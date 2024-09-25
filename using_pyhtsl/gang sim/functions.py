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
    apply_potion_effect,
    full_heal,
    TeamColor,
    PlayerLocationX,
    PlayerLocationY,
    PlayerLocationZ,
    remove_item,
    HasItem,
    Item,
    display_menu,
)
from pyhtsl.types import ALL_POTION_EFFECTS
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
    GangSimGang,
    Bloods,
    Crips,
    Kings,
    Grapes,
    SpawnTeam,
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
    SEND_TO_SPAWN_COUNTER,
    PREVIOUS_COORDINATE_X,
    PREVIOUS_COORDINATE_Y,
    PREVIOUS_COORDINATE_Z,
    TELEPORTING_ID,
    TELEPORTING_TIMER,
    TIP_COUNTER,
    TIP_INDEX,
    seconds_to_every_4_ticks,
    TEAM_LEADER_ID,
    TEAM_LEADER_IS_WEARING_CROWN,
    TEAM_LEADER_NOT_WORN_TIMER,
    SPEED_EFFECT_TIMER,
    RESISTANCE_EFFECT_TIMER,
    REGENERATION_EFFECT_TIMER,
    JUMPBOOST_EFFECT_TIMER,
    INVISIBILITY_EFFECT_TIMER,
    DAILY_RESET_LAST_DAY,
    DAILY_FREE_SWITCHES,
    NEW_DESIRED_GANG_ID,
)
from locations import LOCATIONS, LocationInstances
from everything import Items, BuffType, Teleports
from currency import add_funds
from title_action_bar import (
    get_title_action_bars,
    TurfDestroyedTitleActionBar,
    TurfCapturedTitleActionBar,
    OnDeathTitleActionBar,
    OnKillTitleActionBar,
    OnBadKillTitleActionBar,
    WaitingOnTeleportTitleActionBar,
    NewGangLeaderTitleActionBar,
    GangLeaderFallenTitleActionBar,
    RemoveCredTitleActionBar,
)

from typing import Literal


"""
TODO
[ ] add all locations
[ ] combat logging

[1.0] abilities
[1.0] bounties maybe
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
    PLAYER_CRED.value = 10
    PLAYER_FUNDS.value = 100
    reset_inventory()
    give_item(Items.tier_1_weapon.item)
    give_item(Items.tier_1_boots.item)


# DEATH / KILLS ======================================================================


@create_function('Send Gang Leader Fallen Chat')
def send_gang_leader_fallen_chat() -> None:
    GangLeaderFallenTitleActionBar.apply()


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
    trigger_function(clamp_cred)

    for gang, crown in (
        (Bloods, Items.bloods_leader_crown),
        (Crips, Items.crips_leader_crown),
        (Kings, Items.kings_leader_crown),
        (Grapes, Items.grapes_leader_crown),
    ):
        with IfAnd(
            gang.LEADER_ID == PLAYER_ID,
        ):
            GangLeaderFallenTitleActionBar.apply_globals(gang)
            trigger_function(send_gang_leader_fallen_chat, trigger_for_all_players=True)
            gang.LEADER_ID.value = NO_GANG_LEADER_ID
            remove_item(crown.item)

    trigger_function(move_to_spawn)
    trigger_function(check_gang_leaders_and_armor)
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

    with IfAnd(
        PLAYER_CRED < 0,
    ):
        added_funds.value /= 2
        ADD_EXPERIENCE.value /= 2

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
    removed_cred = DISPLAY_ARG_1
    with IfAnd(
        LATEST_DEATH_WAS_LEADER == 1,
    ):
        removed_cred.value = 3

    cutoff = 20
    with IfAnd(
        LATEST_DEATH_WAS_LEADER	== 0,
        PLAYER_CRED > cutoff,
    ):
        removed_cred.value = 5
    with IfAnd(
        LATEST_DEATH_WAS_LEADER == 0,
        PLAYER_CRED <= cutoff,
    ):
        removed_cred.value = 3

    PLAYER_CRED.value -= removed_cred
    trigger_function(clamp_cred)

    OnBadKillTitleActionBar.apply(removed_cred)
    with IfOr(
        *(TEAM_ID == gang.ID for gang in ALL_GANG_TEAMS),
    ):
        pass
    with Else:
        exit_function()

    with IfAnd(
        LATEST_DEATH_WAS_LEADER == 1,
    ):
        transfer_gang_leadership('BETRAYAL')


# MISC?? =================================


FREE_SWITCHES_PER_DAY = 5
SWITCH_COST = 3
MIN_CRED = -10


pay_for_switch_item = Item(
    'lime_stained_clay',
    name='&a&lARE YOU SURE?',
    lore=(
        f'&cYou have ran out of free\n&cdaily gang switches.&7 (0/{FREE_SWITCHES_PER_DAY})'
        f'\n\n&cIt will cost you&2 {SWITCH_COST} Cred&c to\n&cswitch to a different gang.'
        '\n\n&eClick to proceed.'
    ),
    hide_all_flags=True,
)
pay_for_switch_item.save()


TIPS = [
    '&eGained&3 XP&e on kill =&a min&7(&b3&a +&6 killstreak&a /&b 5&7,&b 10&7)',  # min(3 + killstreak/5, 10) + prestige
    '&eKilling an enemy gang leader gives double&3 XP&e and&6 Funds&e, and more&2 Cred&e!',
    '&eYour turf will slowly heal back to&c full health&e over time.',
    '&eKilling a friendly gang member will cause you to lose&2 Cred&e.',
    '&eYour global level is calculated by combining all your individual levels.',
    '&eThe more stars your turf has, the more&6 Funds&e it will generate.',
    '&eYour&c Power&e is used for abilities and will regenerate over time.',
    '&eLogging out during combat will count as a death with extra loss of&2 Cred&e.',  # TODO
    '&eKilling your own gang leader is discouraged, but it will promote you to leader.',
    '&eYour turf will gain more&6 Funds&e the longer you hold it without distributing.',
    '&eA new gang leader will be randomly chosen if the crown is not worn for too long.',
    '&eGiving a&6 /cookie&e is greatly appreciated and can earn everyone rewards!',
    '&eMembers of very small gangs compared to others will gain&c +1 Strength&e.',
    '&eHaving all 5 effects at the same time will give you&c +1 Strength&e.',
    '&eTurfs will not generate&6 Funds&e if all its members are at spawn.',
    f'&eYou can switch gangs for free {FREE_SWITCHES_PER_DAY} times a day, after that it will cost&2 {SWITCH_COST} Cred&e.',
    '&eIf you have negative&2 Cred&e, you gain&8 +1 Slowness&e.',
    '&eIf you have negative&2 Cred&e, you cannot switch gangs.',
    '&eIf you have negative&2 Cred&e, you will earn less&6 Funds&e and&3 XP&e.',
    f'&eYou cannot have less than&2 {MIN_CRED} Cred&e.',
]


def check_tips() -> None:
    TIP_COUNTER.value += 1
    with IfAnd(
        TIP_COUNTER >= 120,
    ):
        TIP_COUNTER.value = 0
    with Else:
        exit_function()

    TIP_INDEX.value += 1
    with IfAnd(
        TIP_INDEX >= len(TIPS),
    ):
        TIP_INDEX.value = 0
    trigger_function(show_tip, trigger_for_all_players=True)


@create_function('Show Tip')
def show_tip() -> None:
    for i, tip in enumerate(TIPS):
        with IfAnd(
            TIP_INDEX == i,
        ):
            chat('&f[&bTIP&f] ' + tip)


def apply_effects_to_max(effect: ALL_POTION_EFFECTS, max_level: int, count: PlayerStat) -> None:
    for level in range(1, max_level + 1):
        with IfAnd(
            (count == level) if level < max_level else (count >= level),
        ):
            apply_potion_effect(
                effect,
                duration=1,
                level=level,
                override_existing_effects=True,
            )


@create_function('Apply Potion Effects')
def apply_all_potion_effects() -> None:
    count = PlayerStat('temp')

    count.value = 0
    with IfAnd(
        SPEED_EFFECT_TIMER > 0,
    ):
        count.value += 1
    apply_effects_to_max('speed', 3, count)

    count.value = 0
    with IfAnd(
        RESISTANCE_EFFECT_TIMER > 0,
    ):
        count.value += 1
    apply_effects_to_max('resistance', 1, count)

    count.value = 0
    with IfAnd(
        REGENERATION_EFFECT_TIMER > 0,
    ):
        count.value += 1
    apply_effects_to_max('regeneration', 1, count)

    count.value = 0
    with IfAnd(
        JUMPBOOST_EFFECT_TIMER > 0,
    ):
        count.value += 1
    apply_effects_to_max('jump_boost', 1, count)

    count.value = 0
    with IfAnd(
        INVISIBILITY_EFFECT_TIMER > 0,
    ):
        count.value += 1
    apply_effects_to_max('invisibility', 1, count)

    count.value = 0
    with IfAnd(
        SPEED_EFFECT_TIMER > 0,
        RESISTANCE_EFFECT_TIMER > 0,
        REGENERATION_EFFECT_TIMER > 0,
        JUMPBOOST_EFFECT_TIMER > 0,
        INVISIBILITY_EFFECT_TIMER > 0,
    ):
        count.value += 1
    one_eightth = PlayerStat('temp1')
    one_eightth.value = (Bloods.TEAM.players() + Crips.TEAM.players() + Kings.TEAM.players() + Grapes.TEAM.players()) // 8
    for gang in (
        Bloods,
        Crips,
        Kings,
        Grapes,
    ):
        with IfAnd(
            PLAYER_GANG == gang.ID,
            gang.TEAM.players() <= one_eightth,
        ):
            count.value += 1
    apply_effects_to_max('strength', 2, count)

    count.value = 0
    with IfOr(
        BIGGEST_LOCATION_ID == LocationInstances.spawn.biggest_id,
        PLAYER_CRED >= 0,
    ):
        pass
    with Else:
        count.value += 1
    apply_effects_to_max('slowness', 1, count)

    apply_potion_effect(
        'night_vision',
        duration=2592000,
        level=1,
        override_existing_effects=True,
    )


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
            demotion_protection=False,
        )
        exit_function()
    for name, cred_req in (
        ('1000', 1000),
        ('500', 500),
        ('250', 250),
        ('150', 150),
        ('100', 100),
        ('75', 75),
        ('50', 50),
        ('40', 40),
        ('30', 30),
        ('25', 25),
        ('20', 20),
        ('15', 15),
        ('10', 10),
        ('5', 5),
        ('1', 1),
    ):
        with IfAnd(
            PLAYER_CRED >= cred_req,
        ):
            change_player_group(
                name,
                demotion_protection=False,
            )
            exit_function()
    change_player_group(
        '0',
        False,
    )


TEMPORARY_SPAWN = (-2.5, 106.0, -40.5)


@create_function('Teleport Into Map')
def teleport_into_map() -> None:
    teleport_player(TEMPORARY_SPAWN)
    play_sound('Enderman Teleport')


@create_function('Force Join Team')
def force_join_team() -> None:
    for gang, chestplate in zip(ALL_GANG_TEAMS, (
        Items.bloods_chestplate.item,
        Items.crips_chestplate.item,
        Items.kings_chestplate.item,
        Items.grapes_chestplate.item,
    )):
        with IfAnd(
            PLAYER_GANG == gang.ID,
        ):
            set_player_team(gang.TEAM)
            give_item(chestplate, inventory_slot='chestplate', replace_existing_item=True)
    trigger_function(check_player_gang)
    trigger_function(teleport_into_map)


def joined_gang_no_switch_message(gang: type[GangSimTeam]) -> None:
    chat(IMPORTANT_MESSAGE_PREFIX + f'&eYou are now part of the&{gang.ID}&l {gang.name().upper()}&e!')


def joined_gang_with_switch_message(gang: type[GangSimTeam]) -> None:
    chat(IMPORTANT_MESSAGE_PREFIX + f'&b&lSWITCH!&e You are now part of the&{gang.ID}&l {gang.name().upper()}&e!')


@create_function('Display Last Gang Membership')
def display_last_gang_membership() -> None:
    for gang in ALL_GANG_TEAMS:
        with IfAnd(
            PLAYER_LAST_GANG == gang.ID,
        ):
            chat(IMPORTANT_MESSAGE_PREFIX + f'&cYou were last part of the&{gang.ID}&l {gang.name().upper()}&c.')


@create_function('Pay For Gang Switch')
def pay_for_gang_switch() -> None:
    PLAYER_CRED.value -= SWITCH_COST
    RemoveCredTitleActionBar.apply(SWITCH_COST)
    trigger_function(clamp_cred)
    PLAYER_GANG.value = NEW_DESIRED_GANG_ID
    trigger_function(force_join_team)
    for gang in ALL_GANG_TEAMS:
        with IfAnd(
            PLAYER_GANG == gang.ID,
        ):
            joined_gang_with_switch_message(gang)
    NEW_DESIRED_GANG_ID.value = 0


def ON_TEAM_JOIN(
    team: type[GangSimTeam],
) -> None:
    with IfOr(
        PLAYER_LAST_GANG == 0,
        PLAYER_LAST_GANG == team.ID,
    ):
        PLAYER_GANG.value = team.ID
        trigger_function(force_join_team)
        joined_gang_no_switch_message(team)
        exit_function()

    with IfAnd(
        PLAYER_CRED < 0,
    ):
        chat(IMPORTANT_MESSAGE_PREFIX + '&cYou cannot switch gangs with negative&2 Cred&c!')
        trigger_function(display_last_gang_membership)
        trigger_function(move_to_spawn)
        exit_function()

    with IfAnd(
        DAILY_FREE_SWITCHES <= 0,
    ):
        NEW_DESIRED_GANG_ID.value = team.ID
        display_menu('ARE YOU SURE?')
        # NOTE set all green clay actions to:
        # trigger_function(pay_for_gang_switch)
        trigger_function(move_to_spawn)
        exit_function()

    DAILY_FREE_SWITCHES.value -= 1
    PLAYER_GANG.value = team.ID
    trigger_function(force_join_team)
    joined_gang_with_switch_message(team)


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


# NOTE have this get called by the actual event
@create_function('On Portal Enter')
def on_portal_enter() -> None:
    trigger_function(check_locations)
    for location, function in (
        (LocationInstances.spawn_bloods_area, on_bloods_join),
        (LocationInstances.spawn_crips_area, on_crips_join),
        (LocationInstances.spawn_kings_area, on_kings_join),
        (LocationInstances.spawn_grapes_area, on_grapes_join),
    ):
        with IfAnd(
            LOCATION_ID == location.id
        ):
            trigger_function(function)


@create_function('Move To Spawn')
def move_to_spawn() -> None:
    set_player_team(SpawnTeam.TEAM)
    PLAYER_GANG.value = EMPTY_TURF_GANG
    Teleports.SPAWN.execute()
    full_heal()


@create_function('Check Out Of Spawn')
def check_out_of_spawn() -> None:
    with IfAnd(
        GroupPriority >= 19
    ):
        SEND_TO_SPAWN_COUNTER.value = 0
        exit_function()

    with IfOr(
        BIGGEST_LOCATION_ID != LocationInstances.spawn.biggest_id,
        RequiredTeam(SpawnTeam.TEAM),
    ):
        pass
    with Else:
        # is at spawn without spawn team
        set_player_team(SpawnTeam.TEAM)
        SEND_TO_SPAWN_COUNTER.value = 0
        exit_function()

    # is not at spawn or has spawn team
    with IfAnd(
        GroupPriority >= 18
    ):
        SEND_TO_SPAWN_COUNTER.value = 0
        exit_function()

    with IfAnd(
        RequiredTeam(SpawnTeam.TEAM),
    ):
        pass
    with Else:
        SEND_TO_SPAWN_COUNTER.value = 0
        exit_function()

    # has spawn team

    with IfOr(
        BIGGEST_LOCATION_ID != LocationInstances.spawn.biggest_id,
    ):
        # has spawn team outside of spawn
        SEND_TO_SPAWN_COUNTER.value += 1

    with IfAnd(
        SEND_TO_SPAWN_COUNTER >= 5,
    ):
        trigger_function(move_to_spawn)


XP_PER_LEVEL = 10


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
        team.REQUIRED_EXPERIENCE.value = team.LEVEL * XP_PER_LEVEL
        with IfAnd(
            PLAYER_GANG == team.ID,
        ):
            PLAYER_CURRENT_LEVEL.value = team.LEVEL
            PLAYER_CURRENT_XP.value = team.EXPERIENCE
            PLAYER_CURRENT_REQUIRED_XP.value = team.REQUIRED_EXPERIENCE
        PLAYER_GLOBAL_LEVEL.value += team.LEVEL

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

    PLAYER_CURRENT_REQUIRED_XP.value = PLAYER_CURRENT_LEVEL * XP_PER_LEVEL


@create_function('Clamp Cred')
def clamp_cred() -> None:
    with IfAnd(
        PLAYER_CRED < MIN_CRED,
    ):
        PLAYER_CRED.value = MIN_CRED


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
    trigger_function(clamp_cred)


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
        # No members, dont destroy but also dont add funds/heal
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


@create_function('Update (Turf 1)')
def update_turf_1() -> None:
    UPDATE_TURF(Turf1)
@create_function('Update (Turf 2)')
def update_turf_2() -> None:
    UPDATE_TURF(Turf2)
@create_function('Update (Turf 3)')
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


@create_function('Daily Reset')
def daily_reset() -> None:
    """Reset daily things, called every day at midnight UTC"""
    DAILY_FREE_SWITCHES.value = FREE_SWITCHES_PER_DAY
    chat(IMPORTANT_MESSAGE_PREFIX + '&eYour daily free gang switches have been reset to&b {FREE_SWITCHES_PER_DAY}&e.')


# NOTE have this run every 20 ticks
@create_function('Personal 1s')
def personal_every_second() -> None:
    PLAYTIME_SECONDS.value += 1
    trigger_function(check_locations)
    trigger_function(update_teleports)
    current_utc_days = PlayerStat('temp')
    current_utc_days.value = DateUnix // (60 * 60 * 24)
    with IfAnd(
        DAILY_RESET_LAST_DAY < current_utc_days,
    ):
        DAILY_RESET_LAST_DAY.value = current_utc_days
        trigger_function(daily_reset)


# NOTE have this run every 4 ticks
@create_function('Personal 0.2s')
def personal_every_4ticks() -> None:
    trigger_function(check_player_gang)
    trigger_function(check_locations)
    trigger_function(check_out_of_spawn)
    trigger_function(check_levels)
    trigger_function(set_most_stats)
    trigger_function(update_display_stats)
    trigger_function(display_action_bar_and_title)
    trigger_function(apply_all_potion_effects)


# NOTE have this run every 4 ticks
@create_function('Global 1s')
def global_every_second() -> None:
    with IfAnd(DateUnix <= LAST_UNIX):
        exit_function()
    LAST_UNIX.value = DateUnix
    trigger_function(update_turfs)
    trigger_function(check_gang_leaders_and_armor)
    trigger_function(update_timer)
    trigger_function(check_cookie_goal)
    set_team_ids()
    check_tips()  # has to be end of function


# GANG LEADERS =====================================


@create_function('Check Is Leader Wearing Crown')
def check_is_leader_wearing_crown() -> None:
    for gang, crown in (
        (Bloods, Items.bloods_leader_crown),
        (Crips, Items.crips_leader_crown),
        (Kings, Items.kings_leader_crown),
        (Grapes, Items.grapes_leader_crown),
    ):
        with IfAnd(
            PLAYER_GANG == gang.ID,
            PLAYER_ID == gang.LEADER_ID,
            HasItem(crown.item, where_to_check='armor'),
        ):
            gang.LEADER_IS_WEARING_CROWN.value = 1
            gang.LEADER_NOT_WORN_TIMER.value = 0


SECONDS_TO_TRANSFER_LEADERSHIP = 10
NO_GANG_LEADER_ID = -1


@create_function('Put Crown On Head')
def put_crown_on_head() -> None:
    for gang, crown in (
        (Bloods, Items.bloods_leader_crown),
        (Crips, Items.crips_leader_crown),
        (Kings, Items.kings_leader_crown),
        (Grapes, Items.grapes_leader_crown),
    ):
        with IfAnd(
            PLAYER_GANG == gang.ID,
            PLAYER_ID == gang.LEADER_ID,
        ):
            give_item(crown.item, inventory_slot='helmet', replace_existing_item=True)


def transfer_gang_leadership(reason: Literal['RANDOM', 'BETRAYAL', 'TRANSFER']) -> None:
    TEAM_LEADER_ID.value = PLAYER_ID
    trigger_function(put_crown_on_head)
    NewGangLeaderTitleActionBar.apply_globals(
        PLAYER_ID,
        TEAM_ID,
        reason,
    )
    trigger_function(apply_new_gang_leader_title, trigger_for_all_players=True)


@create_function('Apply New Gang Leader Title')
def apply_new_gang_leader_title() -> None:
    NewGangLeaderTitleActionBar.apply()


@create_function('Maybe Transfer Gang Leadership (Random)')
def maybe_transfer_gang_leadership_random() -> None:
    with IfAnd(
        TEAM_LEADER_ID == PLAYER_ID,
    ):
        exit_function()

    for gang in (
        Bloods, Crips, Kings, Grapes,
    ):
        with IfAnd(
            PLAYER_GANG == gang.ID,
            gang.LEADER_IS_WEARING_CROWN == 0,
            gang.LEADER_NOT_WORN_TIMER >= SECONDS_TO_TRANSFER_LEADERSHIP,
        ):
            transfer_gang_leadership('RANDOM')


@create_function('Maybe Transfer Gang Leadership (Transfer)')
def maybe_transfer_gang_leadership_transfer() -> None:
    with IfAnd(
        TEAM_LEADER_ID == PLAYER_ID,
    ):
        exit_function()

    for gang, crown in (
        (Bloods, Items.bloods_leader_crown),
        (Crips, Items.crips_leader_crown),
        (Kings, Items.kings_leader_crown),
        (Grapes, Items.grapes_leader_crown),
    ):
        with IfAnd(
            PLAYER_GANG == gang.ID,
            gang.LEADER_IS_WEARING_CROWN == 0,
            HasItem(crown.item, where_to_check='armor'),
        ):
            transfer_gang_leadership('TRANSFER')


@create_function('Remove Illegal Gang Armor')
def remove_illegal_gang_armor() -> None:
    bloods_armor = (Items.bloods_chestplate, Items.bloods_leader_crown)
    crips_armor = (Items.crips_chestplate, Items.crips_leader_crown)
    kings_armor = (Items.kings_chestplate, Items.kings_leader_crown)
    grapes_armor = (Items.grapes_chestplate, Items.grapes_leader_crown)
    for gang, illegals, crown in (
        (Bloods, (*crips_armor, *kings_armor, *grapes_armor), Items.bloods_leader_crown),
        (Crips, (*bloods_armor, *kings_armor, *grapes_armor), Items.crips_leader_crown),
        (Kings, (*bloods_armor, *crips_armor, *grapes_armor), Items.kings_leader_crown),
        (Grapes, (*bloods_armor, *crips_armor, *kings_armor), Items.grapes_leader_crown),
    ):
        for illegal in illegals:
            with IfAnd(
                PLAYER_GANG == gang.ID,
                HasItem(illegal.item),
            ):
                remove_item(illegal.item)

        # if (PLAYER_GANG == gang.ID and gang.LEADER_IS_WEARING_CROWN == 1 and PLAYER_ID != gang.LEADER_ID):
        # means if not (PLAYER_GANG != gang.ID or gang.LEADER_IS_WEARING_CROWN == 0 or PLAYER_ID == gang.LEADER_ID)
        should_remove = PlayerStat('temp')
        with IfOr(
            PLAYER_GANG != gang.ID,
            gang.LEADER_IS_WEARING_CROWN == 0,
            PLAYER_ID == gang.LEADER_ID,
        ):
            should_remove.value = 0
        with Else:
            should_remove.value = 1
        with IfAnd(
            should_remove == 1,
            HasItem(crown.item),
        ):
            remove_item(crown.item)

    should_remove = PlayerStat('temp')
    with IfOr(
        *(PLAYER_GANG == gang.ID for gang in ALL_GANG_TEAMS),
    ):
        should_remove.value = 0
    with Else:
        should_remove.value = 1
    for illegal in (*bloods_armor, *crips_armor, *kings_armor, *grapes_armor):
        with IfAnd(
            should_remove == 1,
            HasItem(illegal.item),
        ):
            remove_item(illegal.item)

    for chestplate in (
        Items.bloods_chestplate,
        Items.crips_chestplate,
        Items.kings_chestplate,
        Items.grapes_chestplate,
    ):
        is_wearing = PlayerStat('temp')
        with IfAnd(
            HasItem(chestplate.item, where_to_check='armor'),
        ):
            is_wearing.value = 1
        with Else:
            is_wearing.value = 0
        with IfAnd(
            is_wearing == 0,
            HasItem(chestplate.item),
        ):
            remove_item(chestplate.item)


@create_function('Check Gang Leaders & Armor')
def check_gang_leaders_and_armor() -> None:
    for gang in (
        Bloods, Crips, Kings, Grapes,
    ):
        gang.LEADER_IS_WEARING_CROWN.value = 0

    trigger_function(check_is_leader_wearing_crown, trigger_for_all_players=True)

    trigger_function(maybe_transfer_gang_leadership_transfer, trigger_for_all_players=True)
    for gang in (
        Bloods, Crips, Kings, Grapes,
    ):
        with IfAnd(
            gang.LEADER_IS_WEARING_CROWN == 1,
        ):
            gang.LEADER_NOT_WORN_TIMER.value = 0
        with Else:
            gang.LEADER_NOT_WORN_TIMER.value += 1

    trigger_function(maybe_transfer_gang_leadership_random, trigger_for_all_players=True)
    for gang in (
        Bloods, Crips, Kings, Grapes,
    ):
        with IfAnd(
            gang.LEADER_NOT_WORN_TIMER >= SECONDS_TO_TRANSFER_LEADERSHIP,
        ):
            # no players in gang and timer is up
            gang.LEADER_ID.value = NO_GANG_LEADER_ID

    trigger_function(remove_illegal_gang_armor, trigger_for_all_players=True)
    # todo check if is wearing crown and id != gang leader id then transfer leadership


# LOCATIONS ========================================


@create_function('Check Locations')
def check_locations() -> None:
    with IfOr(
        PREVIOUS_COORDINATE_X != PlayerLocationX,
        PREVIOUS_COORDINATE_Y != PlayerLocationY,
        PREVIOUS_COORDINATE_Z != PlayerLocationZ,
    ):
        trigger_function(on_move_coordinates)
        PREVIOUS_COORDINATE_X.value = PlayerLocationX
        PREVIOUS_COORDINATE_Y.value = PlayerLocationY
        PREVIOUS_COORDINATE_Z.value = PlayerLocationZ

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


def cancel_teleport(
    send_message: bool,
) -> None:
    if send_message:
        chat(IMPORTANT_MESSAGE_PREFIX + '&cTeleport canceled.')
    TELEPORTING_ID.value = 0
    TELEPORTING_TIMER.value = 0
    DISPLAY_ID.value = 0


@create_function('On Move Coordinates')
def on_move_coordinates() -> None:
    with IfAnd(
        TELEPORTING_ID > 0,
    ):
        cancel_teleport(send_message=True)


@create_function('Update Teleports')
def update_teleports() -> None:
    with IfAnd(
        TELEPORTING_ID > 0,
        BIGGEST_LOCATION_ID == LocationInstances.spawn.biggest_id,
    ):
        cancel_teleport(send_message=False)
        exit_function()

    with IfAnd(
        TELEPORTING_ID == 0,
        DISPLAY_ID == WaitingOnTeleportTitleActionBar.get_id(),
    ):
        DISPLAY_ID.value = 0
    with IfAnd(
        TELEPORTING_ID == 0,
    ):
        exit_function()

    with IfAnd(
        TELEPORTING_TIMER > 0,
    ):
        TELEPORTING_TIMER.value -= 1
        play_sound('Note Sticks')
    with IfAnd(
        TELEPORTING_TIMER > 0,
    ):
        exit_function()

    for teleport in Teleports.all():
        with IfAnd(
            TELEPORTING_ID == teleport.id,
        ):
            teleport.execute()
    TELEPORTING_ID.value = 0


# NOTE have this get called by the actual command
@create_function('Run Spawn Command')
def run_spawn_command() -> None:
    with IfAnd(
        BIGGEST_LOCATION_ID == LocationInstances.spawn.biggest_id,
    ):
        trigger_function(move_to_spawn)
        cancel_teleport(send_message=False)
        exit_function()

    with IfAnd(
        TELEPORTING_ID == Teleports.SPAWN.id,
    ):
        cancel_teleport(send_message=True)
        exit_function()

    Teleports.SPAWN.apply()


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
    seconds_per = 4
    messages = [
        f'&6&l{PLAYER_KILL_STREAK}&6-Streak&7 (&a{PLAYER_KILLS}K&7/&c{PLAYER_DEATHS}D&7)&3 {PLAYER_CURRENT_XP}/{PLAYER_CURRENT_REQUIRED_XP}xp',
        f'&7(&{Turf1.GANG}&l✯✯✯&e {Turf1.FUNDS}⛁&7) (&{Turf2.GANG}&l✯✯&e {Turf2.FUNDS}⛁&7) (&{Turf3.GANG}&l✯&e {Turf3.FUNDS}⛁&7)',
    ]

    modulo_by = seconds_per * len(messages)
    did_modulo_on = PlayerStat('temp')
    did_modulo_on.value = DateUnix
    did_modulo_on.value -= did_modulo_on // modulo_by * modulo_by
    for i, message in enumerate(messages):
        with IfAnd(
            did_modulo_on == i * seconds_per,
        ):
            display_action_bar(message)
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

    for (turf_gang, stars) in (
        (Turf1.GANG, '✯✯✯'),
        (Turf2.GANG, '✯✯'),
        (Turf3.GANG, '✯'),
    ):
        with IfAnd(
            payout > 0,
            turf_gang == PAYOUT_GANG,
        ):
            display_title(
                title=f'&{TEAM_ID}Funds Distributed',
                subtitle=f'&aYou received&e +{payout}⛁&7 (&{TEAM_ID}&l{stars}&7)',
                fadein=0,
                stay=1,
                fadeout=0,
            )


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

    funds = PlayerStat('temp')
    funds.value = turf.FUNDS
    with IfAnd(
        PLAYER_CRED < 0,
    ):
        funds.value /= 2
    PLAYER_FUNDS.value += funds
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


@create_function('Destroy (Turf 1)')
def destroy_turf_1() -> None:
    DESTROY_TURF(Turf1)
@create_function('Try Claim (Turf 1)')
def claim_turf_1() -> None:
    CLAIM_TURF(Turf1)
@create_function('On Click (Turf 1)')
def on_click_turf_1() -> None:
    ON_CLICK_TURF(Turf1, claim_turf_1, destroy_turf_1)
@create_function('Destroy (Turf 2)')
def destroy_turf_2() -> None:
    DESTROY_TURF(Turf2)
@create_function('Try Claim (Turf 2)')
def claim_turf_2() -> None:
    CLAIM_TURF(Turf2)
@create_function('On Click (Turf 2)')
def on_click_turf_2() -> None:
    ON_CLICK_TURF(Turf2, claim_turf_2, destroy_turf_2)
@create_function('Destroy (Turf 3)')
def destroy_turf_3() -> None:
    DESTROY_TURF(Turf3)
@create_function('Try Claim (Turf 3)')
def claim_turf_3() -> None:
    CLAIM_TURF(Turf3)
@create_function('On Click (Turf 3)')
def on_click_turf_3() -> None:
    ON_CLICK_TURF(Turf3, claim_turf_3, destroy_turf_3)
