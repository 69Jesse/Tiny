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
    IsItem,
    RandomInt,
    IsFlying,
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
    ADD_FUNDS,
    ADD_CRED,
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
    COMBAT_TIMER,
    GLOBAL_TEMP_ARG_1,
    GLOBAL_TEMP_ARG_2,
    play_unable_sound,
    play_big_success_sound,
    play_small_success_sound,
    IS_AT_SPAWN_COUNTER,
    PLAYER_POWER_UPPER_BOUND,
    PERSONAL_EVERY_SECOND_INDEX,
    WEAPON_ABILITY_SPEED_TIMER,
    WEAPON_ABILITY_REGEN_TIMER,
    ABILITY_ID,
    ABILITY_POWER_COST,
    SHOP_BUY_ID,
    TOTAL_FUNDS_SPENT,
    SELECTED_PERK_A,
    SELECTED_PERK_B,
    PERK_1_TIER,
    PERK_2_TIER,
    PERK_3_TIER,
    PERK_4_TIER,
    PERK_5_TIER,
    PERK_6_TIER,
    PERK_7_TIER,
    PERK_8_TIER,
    PERK_9_TIER,
    PERK_1_COLOR,
    PERK_2_COLOR,
    PERK_3_COLOR,
    PERK_4_COLOR,
    PERK_5_COLOR,
    PERK_6_COLOR,
    PERK_7_COLOR,
    PERK_8_COLOR,
    PERK_9_COLOR,
    CHANGING_PERK_LETTER,
    CLICKED_PERK_INDEX,
    PERK_BUY_PRICE,
    PERK_NEW_TIER,
    REGEN_ON_KILL_TIMER,
    STRENGTH_ON_KILL_TIMER,
    MACHINE_EFFECT_INDEX,
    SPAWN_TELEPORT_INDEX,
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
    RemovePowerTitleActionBar,
    RemoveFundsTitleActionBar,
    AddFundsTitleActionBar,
)
from shop import ALL_SHOP_ITEMS
from perks import ALL_PERKS, NamedPerks

from typing import Literal


"""
TODO
[ ] add shops
[ ] add all locations
[ ] message when entering turf area
[ ] abilities
[ ] bounties maybe
"""


# ABILITIES =========================================================


@create_function('Try To Use Ability')
def try_to_use_ability() -> None:
    ABILITY_POWER_COST.value = -1
    with IfAnd(
        ABILITY_ID >= 3,  # WEAPON ABILITIES
        ABILITY_ID <= 18,
    ):
        ABILITY_POWER_COST.value = 70 + (ABILITY_ID * 10)

    with IfAnd(
        ABILITY_POWER_COST < 0,
    ):
        chat(IMPORTANT_MESSAGE_PREFIX + '&cThis ability does not seem to exist?? Contact a staff member.')
        play_unable_sound()
        exit_function()

    trigger_function(set_most_stats)
    trigger_function(update_power)
    with IfAnd(
        PLAYER_POWER < ABILITY_POWER_COST,
    ):
        chat(IMPORTANT_MESSAGE_PREFIX + f'&cYou do not have enough Power to use this ability! ({PLAYER_POWER}/{ABILITY_POWER_COST})')
        play_unable_sound()
        exit_function()

    PLAYER_POWER.value -= ABILITY_POWER_COST
    RemovePowerTitleActionBar.apply(ABILITY_POWER_COST)
    PLAYER_POWER_UPPER_BOUND.value = PLAYER_POWER
    trigger_function(force_use_ability)


@create_function('Force Trigger Weapon Ability')
def force_trigger_weapon_ability() -> None:
    WEAPON_ABILITY_SPEED_TIMER.value = ABILITY_ID + 2
    WEAPON_ABILITY_REGEN_TIMER.value = ABILITY_ID - 8
    with IfAnd(
        WEAPON_ABILITY_SPEED_TIMER > 10,
    ):
        WEAPON_ABILITY_SPEED_TIMER.value = 10
    with IfAnd(
        WEAPON_ABILITY_REGEN_TIMER < 0,
    ):
        WEAPON_ABILITY_REGEN_TIMER.value = 0
    play_sound('Wolf Howl', pitch=2.0)
    pause_execution(20)
    play_sound('Wolf Howl', pitch=2.0)
    pause_execution(20)
    play_sound('Wolf Howl', pitch=2.0)


@create_function('Force Use Ability')
def force_use_ability() -> None:
    with IfAnd(
        ABILITY_ID >= 3,  # WEAPON ABILITIES
        ABILITY_ID <= 18,
    ):
        trigger_function(force_trigger_weapon_ability)


# SHOP =========================================================


@create_function('Shop Not Enough Funds Message')
def shop_not_enough_funds_message() -> None:
    chat(IMPORTANT_MESSAGE_PREFIX + '&cYou do not have enough Funds to purchase this item!')
    play_unable_sound()


@create_function('Shop Missing Items Message')
def shop_missing_items_message() -> None:
    chat(IMPORTANT_MESSAGE_PREFIX + '&cYou are missing required item(s) to purchase this item!')
    play_unable_sound()


def item_copied_with_correct_count(item: Item, count: int) -> Item:
    item = item.copy()
    item.count = count
    return item


# NOTE: In shop menu, set SHOP_BUY_ID to the shop item id then trigger this
@create_function('Try To Buy Shop Item')
def try_to_buy_shop_item() -> None:
    for shop_item in ALL_SHOP_ITEMS:
        with IfAnd(
            SHOP_BUY_ID == shop_item.id,
            PLAYER_FUNDS < shop_item.funds_cost,
        ):
            trigger_function(shop_not_enough_funds_message)
            exit_function()
        if shop_item.items_cost:
            with IfAnd(
                SHOP_BUY_ID == shop_item.id,
                *(
                    HasItem(item_copied_with_correct_count(item, count))
                    for item, count in shop_item.items_cost
                )
            ):
                trigger_function(force_buy_shop_item)
                exit_function()
            with IfAnd(
                SHOP_BUY_ID == shop_item.id,
            ):
                trigger_function(shop_missing_items_message)
                exit_function()
    trigger_function(force_buy_shop_item)


@create_function('Force Buy Shop Item')
def force_buy_shop_item() -> None:
    for shop_item in ALL_SHOP_ITEMS:
        with IfAnd(
            SHOP_BUY_ID == shop_item.id,
        ):
            PLAYER_FUNDS.value -= shop_item.funds_cost
            RemoveFundsTitleActionBar.apply(shop_item.funds_cost)
            TOTAL_FUNDS_SPENT.value += shop_item.funds_cost
            for item, count in shop_item.items_cost:
                remove_item(item_copied_with_correct_count(item, count))
            give_item(shop_item.item, allow_multiple=True)
            assert shop_item.item.name is not None
            name = (f'&8{shop_item.item.count} ' if shop_item.item.count > 1 else '') + shop_item.item.name
            chat(IMPORTANT_MESSAGE_PREFIX + f'&b&lNICE!&e Successfully purchased {name}&e!')
    play_big_success_sound()


# PERKS =========================================================


'''
How it should work:
    - General perk menu:
        - Click on a park -> Buy / upgrade it
    - Selecting perk menu:
        - Click on a perk ->
            if unselected -> select it
            if selected by this perk letter -> upgrade it
            if selected by other perk letter -> select it, deselect other one
'''


LETTER_A = 0
LETTER_B = 1


# NOTE: In general perk menu, set CLICKED_PERK_INDEX to the perk index then trigger this, then reopen menu
@create_function('Try To Upgrade Perk')
def try_to_upgrade_perk() -> None:
    PERK_BUY_PRICE.value = -1
    for perk in ALL_PERKS:
        for tier, (_, price) in enumerate(perk.tiers, start=1):
            with IfAnd(
                CLICKED_PERK_INDEX == perk.index,
                perk.unlocked_tier_stat == tier - 1,
            ):
                PERK_BUY_PRICE.value = price
                PERK_NEW_TIER.value = tier

    with IfAnd(
        PERK_BUY_PRICE < 0,
    ):
        chat(IMPORTANT_MESSAGE_PREFIX + '&cThis perk cannot be upgraded any further!')
        play_unable_sound()
        exit_function()
    with IfAnd(
        PLAYER_FUNDS < PERK_BUY_PRICE,
        PERK_NEW_TIER == 1,
    ):
        chat(IMPORTANT_MESSAGE_PREFIX + '&cYou do not have enough Funds to purchase this perk!')
        play_unable_sound()
        exit_function()
    with IfAnd(
        PLAYER_FUNDS < PERK_BUY_PRICE,
    ):
        chat(IMPORTANT_MESSAGE_PREFIX + '&cYou do not have enough Funds to upgrade this perk!')
        play_unable_sound()
        exit_function()

    trigger_function(force_upgrade_perk)


@create_function('Force Upgrade Perk')
def force_upgrade_perk() -> None:
    for perk in ALL_PERKS:
        with IfAnd(
            CLICKED_PERK_INDEX == perk.index,
        ):
            perk.unlocked_tier_stat.value = PERK_NEW_TIER
            chat(IMPORTANT_MESSAGE_PREFIX + f'&b&lNICE!&e Upgraded&a {perk.name}&e to&c Tier {perk.unlocked_tier_stat}&e!')
    PLAYER_FUNDS.value -= PERK_BUY_PRICE
    TOTAL_FUNDS_SPENT.value += PERK_BUY_PRICE
    RemoveFundsTitleActionBar.apply(PERK_BUY_PRICE)
    play_big_success_sound()
    PERK_BUY_PRICE.value = 0
    PERK_NEW_TIER.value = 0


@create_function('Force Select Perk')
def force_select_perk() -> None:
    for perk in ALL_PERKS:
        for letter_stat, letter, letter_name in (
            (SELECTED_PERK_A, LETTER_A, 'A'),
            (SELECTED_PERK_B, LETTER_B, 'B'),
        ):
            with IfAnd(
                CHANGING_PERK_LETTER == letter,
                CLICKED_PERK_INDEX == perk.index,
            ):
                letter_stat.value = CLICKED_PERK_INDEX
                chat(IMPORTANT_MESSAGE_PREFIX + f'&eSelected&a {perk.name}&e as your&a Perk {letter_name}&e.&7 (Click again to upgrade)')

    play_small_success_sound()

    with IfAnd(
        CHANGING_PERK_LETTER == LETTER_A,
        SELECTED_PERK_A == SELECTED_PERK_B
    ):
        SELECTED_PERK_B.value = 0
        chat(IMPORTANT_MESSAGE_PREFIX + '&cYou now have no Perk B selected.')
    with IfAnd(
        CHANGING_PERK_LETTER == LETTER_B,
        SELECTED_PERK_B == SELECTED_PERK_A
    ):
        SELECTED_PERK_A.value = 0
        chat(IMPORTANT_MESSAGE_PREFIX + '&cYou now have no Perk A selected.')


# NOTE: In selecting perk menu, set CHANGING_PERK_LETTER to A or B and CLICKED_PERK_INDEX to the perk index then trigger this, then reopen menu
@create_function('Select Or Upgrade Perk')
def select_or_upgrade_perk() -> None:
    with IfAnd(
        SELECTED_PERK_A == CLICKED_PERK_INDEX,
        CHANGING_PERK_LETTER == LETTER_A,
    ):
        trigger_function(try_to_upgrade_perk)
        exit_function()
    with IfAnd(
        SELECTED_PERK_B == CLICKED_PERK_INDEX,
        CHANGING_PERK_LETTER == LETTER_B,
    ):
        trigger_function(try_to_upgrade_perk)
        exit_function()

    for perk in ALL_PERKS:
        with IfAnd(
            CLICKED_PERK_INDEX == perk.index,
            perk.unlocked_tier_stat <= 0,
        ):
            trigger_function(try_to_upgrade_perk)
        with IfAnd(
            CLICKED_PERK_INDEX == perk.index,
            perk.unlocked_tier_stat <= 0,
        ):
            exit_function()

    trigger_function(force_select_perk)


# NOTE: In selecting perk menu, set CHANGING_PERK_LETTER to A or B then trigger this
@create_function('Deselect Perk')
def deselect_perk() -> None:
    for letter_stat, letter, letter_name in (
        (SELECTED_PERK_A, LETTER_A, 'A'),
        (SELECTED_PERK_B, LETTER_B, 'B'),
    ):
        with IfAnd(
            CHANGING_PERK_LETTER == letter,
            letter_stat > 0,
        ):
            letter_stat.value = 0
            chat(IMPORTANT_MESSAGE_PREFIX + f'&eDeselected&a Perk {letter_name}&e.')
        with IfAnd(
            CHANGING_PERK_LETTER == letter,
            letter_stat == 0,
        ):
            chat(IMPORTANT_MESSAGE_PREFIX + f'&eYou do not have a Perk {letter_name} selected.')

    play_small_success_sound()


@create_function('Set Perk Color Stats')
def set_perk_color_stats() -> None:
    for perk in ALL_PERKS:
        with IfOr(
            SELECTED_PERK_A == perk.index,
            SELECTED_PERK_B == perk.index,
        ):
            perk.color_stat.value = 2
        with Else:
            perk.color_stat.value = 8


@create_function('Reset Perk Color Stats')
def reset_perk_color_stats() -> None:
    for perk in ALL_PERKS:
        perk.color_stat.value = 0


# NOTE: In blacksmith menu, on perk item click, trigger this
@create_function('Open General Perk Menu')
def open_general_perk_menu() -> None:
    trigger_function(set_perk_color_stats)
    display_menu('Blacksmith: Perks')
    pause_execution(20)
    trigger_function(reset_perk_color_stats)


# NOTE: in general perk menu, on perk A/B item click, set CHANGING_PERK_LETTER to A/B then trigger this
@create_function('Open Selecting Perk Menu')
def open_selecting_perk_menu() -> None:
    trigger_function(set_perk_color_stats)
    with IfAnd(
        CHANGING_PERK_LETTER == LETTER_A,
    ):
        display_menu('Select Perk A')
    with IfAnd(
        CHANGING_PERK_LETTER == LETTER_B,
    ):
        display_menu('Select Perk B')
    pause_execution(20)
    trigger_function(reset_perk_color_stats)


# JOIN / LEAVE ========================================================


display_player_join_leave_message_player_id = GLOBAL_TEMP_ARG_1
display_player_join_leave_message_mode = GLOBAL_TEMP_ARG_2
display_player_join_leave_message_mode_join = 0
display_player_join_leave_message_mode_join_new = 1
display_player_join_leave_message_mode_leave = 2
display_player_join_leave_message_mode_leave_with_combat = 3
@create_function('Display Player Join/Leave Message')
def display_player_join_leave_message() -> None:
    with IfAnd(
        display_player_join_leave_message_mode == display_player_join_leave_message_mode_join,
    ):
        chat(f'&eWelcome back&a P#{display_player_join_leave_message_player_id}&e!')
    with IfAnd(
        display_player_join_leave_message_mode == display_player_join_leave_message_mode_join_new,
    ):
        chat(f'&b&lWELCOME!&e They will be known as&a P#{display_player_join_leave_message_player_id}&e!')

    with IfAnd(
        display_player_join_leave_message_mode == display_player_join_leave_message_mode_leave,
    ):
        chat(f'&eGoodbye&a P#{display_player_join_leave_message_player_id}&e!')
    with IfAnd(
        display_player_join_leave_message_mode == display_player_join_leave_message_mode_leave_with_combat,
    ):
        chat(f'&eGoodbye&a P#{display_player_join_leave_message_player_id}&e..&7 (&4&lCOMBAT LOG&7)')


# NOTE have this get called by the actual event
@create_function('On Player Join')
def on_player_join() -> None:
    display_player_join_leave_message_mode.value = display_player_join_leave_message_mode_join
    with IfAnd(
        GroupPriority < 20,
        PLAYER_ID == 0,
    ):
        display_player_join_leave_message_mode.value = display_player_join_leave_message_mode_join_new
        trigger_function(on_player_join_first_time)
    display_player_join_leave_message_player_id.value = PLAYER_ID
    trigger_function(display_player_join_leave_message, trigger_for_all_players=True)

    with IfAnd(
        COMBAT_TIMER > 0,
    ):
        COMBAT_TIMER.value += on_player_death_combat_logged_timer_addon
        trigger_function(on_player_death)


@create_function('On Player Join First Time')
def on_player_join_first_time() -> None:
    TOTAL_PLAYERS_JOINED.value += 1
    PLAYER_ID.value = TOTAL_PLAYERS_JOINED
    set_player_team(SpawnTeam.TEAM)

    PLAYER_CRED.value = 10
    PLAYER_FUNDS.value = 100

    NamedPerks.regen_on_kill.unlocked_tier_stat.value = 1
    SELECTED_PERK_A.value = NamedPerks.regen_on_kill.index
    NamedPerks.extra_xp_on_kill.unlocked_tier_stat.value = 1
    SELECTED_PERK_B.value = NamedPerks.extra_xp_on_kill.index

    reset_inventory()
    give_item(Items.tier_1_weapon.item)
    give_item(Items.tier_1_boots.item)


# NOTE have this get called by the actual event
@create_function('On Player Leave')
def on_player_leave() -> None:
    display_player_join_leave_message_player_id.value = PLAYER_ID
    display_player_join_leave_message_mode.value = display_player_join_leave_message_mode_leave
    with IfAnd(
        COMBAT_TIMER > 0,
    ):
        display_player_join_leave_message_mode.value = display_player_join_leave_message_mode_leave_with_combat
    trigger_function(display_player_join_leave_message, trigger_for_all_players=True)


# DEATH / KILLS ======================================================================


@create_function('Send Gang Leader Fallen Chat')
def send_gang_leader_fallen_chat() -> None:
    GangLeaderFallenTitleActionBar.apply()


display_death_message_streak = GLOBAL_TEMP_ARG_1
@create_function('Display Death Message')
def display_death_message() -> None:
    chat(f'&7They had a&6&l {display_death_message_streak}&6-Streak&7!')


on_player_death_combat_logged_timer_addon = 1_000_000
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

    removing_cred = PlayerStat('tempc')
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

    with IfAnd(
        COMBAT_TIMER >= on_player_death_combat_logged_timer_addon,
    ):
        removing_cred.value *= 2
        chat(IMPORTANT_MESSAGE_PREFIX + '&cYou logged out during combat! This counts as a death with double&2 Cred&c loss.')

    PLAYER_CRED.value -= removing_cred
    trigger_function(clamp_cred)

    pause_execution(1)

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

    trigger_function(check_gang_leaders_and_armor)
    OnDeathTitleActionBar.apply(
        removing_cred,
        PLAYER_KILL_STREAK,
    )
    removing_cred.value = 0

    with IfAnd(
        PLAYER_KILL_STREAK > 3,
    ):
        display_death_message_streak.value = PLAYER_KILL_STREAK
        trigger_function(display_death_message, trigger_for_all_players=True)

    PLAYER_KILL_STREAK.value = 0

    trigger_function(move_to_spawn)


@create_function('Apply On Kill Perk Buffs')
def apply_on_kill_perk_buffs() -> None:
    has_regen_on_kill = PlayerStat('temp')
    with IfOr(
        SELECTED_PERK_A == NamedPerks.regen_on_kill.index,
        SELECTED_PERK_B == NamedPerks.regen_on_kill.index,
    ):
        has_regen_on_kill.value = 1
    with Else:
        has_regen_on_kill.value = 0
    with IfAnd(
        has_regen_on_kill == 1,
        NamedPerks.regen_on_kill.unlocked_tier_stat < 3,
    ):
        REGEN_ON_KILL_TIMER.value = NamedPerks.regen_on_kill.unlocked_tier_stat + 3
    with IfAnd(
        has_regen_on_kill == 1,
        NamedPerks.regen_on_kill.unlocked_tier_stat >= 3,
    ):
        REGEN_ON_KILL_TIMER.value = NamedPerks.regen_on_kill.unlocked_tier_stat + 1

    with IfOr(
        SELECTED_PERK_A == NamedPerks.extra_xp_on_kill.index,
        SELECTED_PERK_B == NamedPerks.extra_xp_on_kill.index,
    ):
        ADD_EXPERIENCE.value += NamedPerks.extra_xp_on_kill.unlocked_tier_stat

    with IfOr(
        SELECTED_PERK_A == NamedPerks.extra_funds_on_kill.index,
        SELECTED_PERK_B == NamedPerks.extra_funds_on_kill.index,
    ):
        ADD_FUNDS.value += NamedPerks.extra_funds_on_kill.unlocked_tier_stat * 20

    with IfOr(
        SELECTED_PERK_A == NamedPerks.strength_on_kill.index,
        SELECTED_PERK_B == NamedPerks.strength_on_kill.index,
    ):
        STRENGTH_ON_KILL_TIMER.value = NamedPerks.strength_on_kill.unlocked_tier_stat

    with IfOr(
        SELECTED_PERK_A == NamedPerks.max_power_on_kill.index,
        SELECTED_PERK_B == NamedPerks.max_power_on_kill.index,
    ):
        PLAYER_POWER.value = PLAYER_MAX_POWER
    with IfAnd(
        PLAYER_POWER > PLAYER_POWER_UPPER_BOUND,
    ):
        PLAYER_POWER_UPPER_BOUND.value = PLAYER_POWER


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

    ADD_EXPERIENCE.value = 3 + (PLAYER_KILL_STREAK // 5)
    with IfAnd(
        ADD_EXPERIENCE > 10,
    ):
        ADD_EXPERIENCE.value = 10
    ADD_EXPERIENCE.value += PLAYER_PRESTIGE

    ADD_FUNDS.value = 10 + PLAYER_PRESTIGE
    ADD_CRED.value = 3

    trigger_function(apply_on_kill_perk_buffs)

    with IfAnd(
        LATEST_DEATH_WAS_LEADER == 1,
    ):
        ADD_EXPERIENCE.value *= 2
        ADD_FUNDS.value *= 2
        ADD_CRED.value += 2

    with IfAnd(
        PLAYER_CRED < 0,
    ):
        ADD_FUNDS.value /= 2
        ADD_EXPERIENCE.value /= 2

    trigger_function(add_experience)
    PLAYER_FUNDS.value += ADD_FUNDS
    PLAYER_CRED.value += ADD_CRED
    OnKillTitleActionBar.apply(
        ADD_FUNDS,
        ADD_CRED,
        ADD_EXPERIENCE,
    )


@create_function('On Bad Player Kill')
def on_bad_player_kill() -> None:
    removed_cred = DISPLAY_ARG_1
    with IfAnd(
        LATEST_DEATH_WAS_LEADER == 1,
    ):
        removed_cred.value = 3
    with Else:
        removed_cred.value = 5

    with IfAnd(
        TEAM_LEADER_ID == PLAYER_ID,
    ):
        removed_cred.value = 0

    PLAYER_CRED.value -= removed_cred
    trigger_function(clamp_cred)

    has_penalty = DISPLAY_ARG_2
    with IfAnd(
        removed_cred > 0,
    ):
        has_penalty.value = 1
    with Else:
        has_penalty.value = 0

    OnBadKillTitleActionBar.apply(removed_cred, has_penalty)
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


FREE_SWITCHES_PER_DAY = 3
SWITCH_COST = 2
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
    '&eGiving a&6 /cookie&e is greatly appreciated and can earn everyone rewards!',
    '&eYour&c Power&e is used for abilities and will regenerate over time.',
    '&eKilling your own gang leader is discouraged, but it will promote you to leader.',
    '&eGained&3 XP&e on kill =&a min&7(&b3&a +&6 killstreak&a /&b 5&7,&b 10&7)',  # min(3 + killstreak/5, 10) + prestige
    '&eHaving all 5 machine effects at the same time will give you&c +1 Strength&e effect.',
    '&eYour turf will slowly heal back to&c full health&e over time.',
    '&eKilling an enemy gang leader gives double&3 XP&e and&6 Funds&e, and more&2 Cred&e!',
    '&eIf you have negative&2 Cred&e, you will earn less&6 Funds&e and&3 XP&e.',
    f'&eYou cannot have less than&2 {MIN_CRED} Cred&e.',
    '&eIf you have negative&2 Cred&e, you cannot switch gangs.',
    '&eThe more stars your turf has, the more&6 Funds&e it will generate.',
    '&eTurfs will not generate&6 Funds&e if all its members are at spawn.',
    '&eYour turf will gain double&6 Funds&e/s if you don\'t distribute it for more than 5 minutes.',
    '&eLogging out during combat will count as a death with double&2 Cred&e loss.',  # TODO
    f'&eYou can only switch gangs for free {FREE_SWITCHES_PER_DAY} times every in-game day.&7 (= 20 minutes)',
    '&eYour global level is calculated by combining all your individual levels.',
    '&eMembers of very small gangs compared to others will gain&c +1 Strength&e.',
    '&eKilling a friendly gang member will cause you to lose&2 Cred&e.',
    '&eA new gang leader will be randomly chosen if the crown is not worn for a long period of time.',
    '&eYou will lose&2 Cred&e if you kill a friendly gang member.',
    '&eA gang leader does not lose&2 Cred&e if they kill a friendly gang member.',
    '&eYou can buy and upgrade your gear at spawn or with&7 /shop&e.',
    '&eThe max HP of a turf is determined by the gang level of all its members.',
]


def check_tips() -> None:
    TIP_COUNTER.value += 1
    with IfAnd(
        TIP_COUNTER >= 300,
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


# NOTE on button click, set MACHINE_EFFECT_INDEX to the index of the machine effect then trigger this
@create_function('Maybe Apply Machine Effect')
def maybe_apply_machine_effect() -> None:
    for index, (timer_stat, cost, name) in enumerate((
        (SPEED_EFFECT_TIMER, 25, '&f+1 Speed'),
        (RESISTANCE_EFFECT_TIMER, 500, '&9+1 Resistance'),
        (REGENERATION_EFFECT_TIMER, 250, '&d+1 Regen'),
        (JUMPBOOST_EFFECT_TIMER, 125, '&a+1 Jump Boost'),
        (INVISIBILITY_EFFECT_TIMER, 125, '&7Invisibility'),
    )):
        with IfAnd(
            MACHINE_EFFECT_INDEX == index,
            timer_stat > 10,
        ):
            chat(IMPORTANT_MESSAGE_PREFIX + f'&cYou still have&b {timer_stat}s&c of {name}&c left!')
            play_unable_sound()
            exit_function()
        with IfAnd(
            MACHINE_EFFECT_INDEX == index,
            PLAYER_FUNDS < cost,
        ):
            chat(IMPORTANT_MESSAGE_PREFIX + f'&cYou do not have enough Funds to purchase {name}&c! ({PLAYER_FUNDS}/{cost:,})')
            play_unable_sound()
            exit_function()
        with IfAnd(
            MACHINE_EFFECT_INDEX == index,
        ):
            PLAYER_FUNDS.value -= cost
            TOTAL_FUNDS_SPENT.value += cost
            RemoveFundsTitleActionBar.apply(cost)
            seconds = 60
            timer_stat.value = seconds
            chat(IMPORTANT_MESSAGE_PREFIX + f'&b&lNICE!&e Purchased&b {seconds}s&e of {name}&e for {cost:,}⛁ Funds&e!')
            play_big_success_sound()


@create_function('Misc 0.2s')
def misc_every_4_ticks() -> None:
    with IfAnd(
        COMBAT_TIMER == 1,
    ):
        chat(IMPORTANT_MESSAGE_PREFIX + '&aYou are no longer in combat.')
    with IfAnd(
        COMBAT_TIMER > 0,
    ):
        COMBAT_TIMER.value -= 1
    with IfAnd(
        PLAYER_ID == NO_GANG_LEADER_ID,
    ):
        PLAYER_ID.value = RandomInt(1_000_000, 10_000_000)
    with IfAnd(
        SELECTED_PERK_A > 0,
        SELECTED_PERK_A == SELECTED_PERK_B,
    ):
        SELECTED_PERK_B.value = 0


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
    with IfAnd(
        WEAPON_ABILITY_SPEED_TIMER > 0,
    ):
        count.value += 1
    with IfOr(
        SELECTED_PERK_A == NamedPerks.perm_speed.index,
        SELECTED_PERK_B == NamedPerks.perm_speed.index,
    ):
        count.value += NamedPerks.perm_speed.unlocked_tier_stat
    apply_effects_to_max('speed', 4, count)

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
    with IfAnd(
        WEAPON_ABILITY_REGEN_TIMER > 0,
    ):
        count.value += 1
    with IfAnd(
        REGEN_ON_KILL_TIMER > 0,
        NamedPerks.regen_on_kill.unlocked_tier_stat < 3,
    ):
        count.value += 2
    with IfAnd(
        REGEN_ON_KILL_TIMER > 0,
        NamedPerks.regen_on_kill.unlocked_tier_stat >= 3,
    ):
        count.value += 3
    apply_effects_to_max('regeneration', 5, count)

    count.value = 0
    with IfAnd(
        JUMPBOOST_EFFECT_TIMER > 0,
    ):
        count.value += 1
    with Items.long_leg_leggings.if_has_condition():
        count.value += 2
    apply_effects_to_max('jump_boost', 3, count)

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
    one_eightth = PlayerStat('one8th')
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
    one_eightth.value = 0
    with IfAnd(
        STRENGTH_ON_KILL_TIMER > 0,
    ):
        count.value += 1
    apply_effects_to_max('strength', 3, count)

    apply_potion_effect(
        'night_vision',
        duration=4141,
        level=1,
        override_existing_effects=True,
    )


@create_function('Set Player Group')
def set_player_group_function() -> None:
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
        demotion_protection=False,
    )


@create_function('Set Player Team')
def set_player_team_function() -> None:
    for gang in ALL_GANG_TEAMS:
        with IfAnd(
            PLAYER_GANG == gang.ID,
        ):
            set_player_team(gang.TEAM)
            exit_function()
    set_player_team(SpawnTeam.TEAM)
    PLAYER_GANG.value = SpawnTeam.ID


TEMPORARY_SPAWN = (-2.5, 106.0, -40.5)


SPAWNS: list[tuple[float, float, float, float, float]] = [
    (17.5, 111, -45, 65, 10),
    (17.5, 111, -36, 110, 10),
    (24, 104, -32.5, -130, 0),
    (37.5, 104, -47, -50, 10),
    (41, 104, -60.5, 0, 0),
    (52, 104, -60.5, 10, 0),
    (57.5, 104, -38, 140, 0),
    (46, 104, -28.5, 135, 0),
    (37.5, 111, -47, -30, 0),
    (56, 111, -60.5, 40, 0),
    (53.5, 111, -41, 120, 0),
    (25.5, 111, -43, -45, 0),
    (29, 111, -31.5, -150, 0),
    (24, 104, -25.5, -30, 0),
    (47, 111, -33.5, -50, 0),
    (57.5, 111, -20, 55, 0),
    (30, 111, -17.5, -160, 0),
    (45, 111, -21.5, 30, 0),
    (13.5, 104, 0, 90, 0),
    (44, 104, -7.5, 130, 0),
    (53, 104, -22.5, 15, 0),
    (57, 104, -20, 65, 0),
    (59.5, 104, 0, 60, 0),
    (50, 104, 34.5, 150, 0),
    (34, 104, 34.5, 145, 0),
    (-19.5, 104, 25, -90, 0),
    (13.5, 104, 19, 125, 0),
    (3, 104, 42.5, 25, 0),
    (-3.5, 104, 59, 110, 0),
    (-37.5, 104, 45, -100, 0),
    (-22, 104, 46.5, -170, 0),
    (-21.5, 104, 41, 75, 0),
    (-33.5, 111, 41, -70, 0),
    (-33.5, 111, 50, -130, 0),
    (10.5, 111, 41, 80, 0),
    (10.5, 111, 50, 120, 0),
    (-21, 104, 15.5, -130, 0),
    (-35.5, 104, 7, -110, 0),
    (-58.5, 104, 6, -30, 0),
    (-43, 106, -20.5, -20, 0),
    (-39, 106, -2.5, -160, 0),
    (-58.5, 106, 0, -150, 0),
    (-58.5, 104, -15, -90, 0),
    (-54.5, 104, -45, -105, 0),
    (-54.5, 104, -32, -105, 0),
    (-20, 104, -46.5, -30, 0),
    (-20, 104, -34.5, -115, 0),
    (-41, 95, -35.5, -55, 0),
    (-20.5, 95, -44, -70, 0),
    (-18, 97, -60.5, -10, 0),
    (-9, 97, -60.5, 10, 0),
    (-9, 95, -31.5, 160, 0),
    (5, 95, -60.5, -40, 0),
    (17, 93, -37.5, 120, 0),
    (23.5, 95, -71, 0, -10),
    (35, 97, -60.5, 0, 0),
    (41.5, 97, -52, 30, 0),
    (38, 97, -28.5, 160, 0),
]


teleport_into_map_portion = 10
teleport_into_map_iterate_all_in = 5 * 60

teleport_into_map_divider = round(teleport_into_map_iterate_all_in / len(SPAWNS))


@create_function('Teleport Into Map')
def teleport_into_map() -> None:
    SPAWN_TELEPORT_INDEX.value = (DateUnix // teleport_into_map_divider) + RandomInt(0, teleport_into_map_portion)
    SPAWN_TELEPORT_INDEX.value -= SPAWN_TELEPORT_INDEX // len(SPAWNS) * len(SPAWNS)

    for i, spawn in enumerate(SPAWNS):
        with IfAnd(
            SPAWN_TELEPORT_INDEX == i,
        ):
            teleport_player(spawn)

    play_sound('Enderman Teleport')


@create_function('Force Join Team')
def force_join_team() -> None:
    SEND_TO_SPAWN_COUNTER.value = 0
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
    with IfAnd(
        TeamPlayers(None) <= 1,
    ):
        transfer_gang_leadership(None)  # quiet transfer
    trigger_function(check_player_gang)
    trigger_function(teleport_into_map)


def joined_gang_no_switch_message(gang: type[GangSimTeam]) -> None:
    chat(IMPORTANT_MESSAGE_PREFIX + f'&eYou are now part of the&{gang.ID}&l {gang.name().upper()}&e!')


def joined_gang_with_switch_message(gang: type[GangSimTeam]) -> None:
    chat(IMPORTANT_MESSAGE_PREFIX + f'&b&lSWITCH!&e You are now part of the&{gang.ID}&l {gang.name().upper()}&e!&7 ({DAILY_FREE_SWITCHES}/{FREE_SWITCHES_PER_DAY:,} daily free switches left)')


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
    PLAYER_POWER.value = PLAYER_MAX_POWER

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
        trigger_function(move_to_spawn)
        chat(IMPORTANT_MESSAGE_PREFIX + '&cYou cannot switch gangs with negative&2 Cred&c!')
        trigger_function(display_last_gang_membership)
        play_unable_sound()
        exit_function()

    with IfAnd(
        DAILY_FREE_SWITCHES <= 0,
    ):
        NEW_DESIRED_GANG_ID.value = team.ID
        display_menu('ARE YOU SURE?')
        # NOTE set all green clay actions to:
        # trigger_function(pay_for_gang_switch)
        chat(IMPORTANT_MESSAGE_PREFIX + '&cYou have ran out of free daily gang switches.')
        trigger_function(display_last_gang_membership)
        trigger_function(move_to_spawn)
        play_unable_sound()
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


@create_function('AFK Area Iteration')
def afk_area_iteration() -> None:
    n = 1
    PLAYER_FUNDS.value += n
    teleport_player(('~', '~13', '~'))
    display_title(
        '&r',
        f'&e+{n:,}⛁&7 (&e{PLAYER_FUNDS}⛁&7)',
        fadein=0,
        stay=2,
        fadeout=0,
    )


# NOTE have this get called by the actual event
# but first have 4 ticks delay, feels nicer
@create_function('On Player Enter Portal')
def on_player_enter_portal() -> None:
    trigger_function(check_locations)
    for location, function in (
        (LocationInstances.spawn_bloods_area, on_bloods_join),
        (LocationInstances.spawn_crips_area, on_crips_join),
        (LocationInstances.spawn_kings_area, on_kings_join),
        (LocationInstances.spawn_grapes_area, on_grapes_join),
        (LocationInstances.spawn_afk_area, afk_area_iteration),
    ):
        with IfAnd(
            LOCATION_ID == location.id
        ):
            trigger_function(function)


BLOODS_SPAWN = (-8.5, 46, -47.5, 130, 0)
CRIPS_SPAWN = (7.5, 46, -47.5, -130, 0)
KINGS_SPAWN = (9.5, 46, -36.5, -60.0, 0)
GRAPES_SPAWN = (-10.5, 46, -36.5, 60.0, 0)


@create_function('Move To Spawn')
def move_to_spawn() -> None:
    SEND_TO_SPAWN_COUNTER.value = 0
    set_player_team(SpawnTeam.TEAM)
    PLAYER_GANG.value = SpawnTeam.ID
    COMBAT_TIMER.value = 0
    full_heal()
    PLAYER_POWER.value = PLAYER_MAX_POWER
    for gang_id, spawn in (
        (Bloods.ID, BLOODS_SPAWN),
        (Crips.ID, CRIPS_SPAWN),
        (Kings.ID, KINGS_SPAWN),
        (Grapes.ID, GRAPES_SPAWN),
    ):
        with IfAnd(
            PLAYER_LAST_GANG == gang_id,
        ):
            teleport_player(spawn)
            exit_function()
    Teleports.SPAWN.teleport()


@create_function('Check Out Of Spawn')
def check_out_of_spawn() -> None:
    with IfAnd(
        GroupPriority >= 18
    ):
        SEND_TO_SPAWN_COUNTER.value = 0
        exit_function()

    with IfOr(
        BIGGEST_LOCATION_ID == LocationInstances.spawn.biggest_id,
    ):
        SEND_TO_SPAWN_COUNTER.value = 0
        IS_AT_SPAWN_COUNTER.value += 1
    with Else:
        IS_AT_SPAWN_COUNTER.value = 0

    with IfAnd(
        IS_AT_SPAWN_COUNTER >= 10,
    ):
        PLAYER_GANG.value = SpawnTeam.ID

    with IfAnd(
        PLAYER_GANG == SpawnTeam.ID,
    ):
        IS_AT_SPAWN_COUNTER.value = 0
    with Else:
        SEND_TO_SPAWN_COUNTER.value = 0
        exit_function()

    with IfOr(
        BIGGEST_LOCATION_ID != LocationInstances.spawn.biggest_id,
        PLAYER_GANG == SpawnTeam.ID,
    ):
        SEND_TO_SPAWN_COUNTER.value = 0
    with Else:
        SEND_TO_SPAWN_COUNTER.value += 1

    with IfAnd(
        SEND_TO_SPAWN_COUNTER >= 10,
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
            chat(f'&b&lLEVEL UP!&e Your&{team.ID}&l {team.name().upper()} LEVEL&e is now&{team.ID} Lv{team.LEVEL}&e!')
            play_big_success_sound()

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
        if item.buffs is None:
            continue
        if not item.buffs:
            continue
        if not any(buff.type.stat is not None for buff in item.buffs):
            continue
        with item.if_has_condition():
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
    with IfOr(
        SELECTED_PERK_A == NamedPerks.additional_power.index,
        SELECTED_PERK_B == NamedPerks.additional_power.index,
    ):
        PLAYER_MAX_POWER.value += NamedPerks.additional_power.unlocked_tier_stat * 20
    with IfOr(
        SELECTED_PERK_A == NamedPerks.more_turf_damage.index,
        SELECTED_PERK_B == NamedPerks.more_turf_damage.index,
    ):
        PLAYER_DAMAGE.value += NamedPerks.more_turf_damage.unlocked_tier_stat
    trigger_function(clamp_cred)
    trigger_function(update_power)


@create_function('Increment Power')
def increment_power() -> None:
    PLAYER_POWER.value += (PLAYER_MAX_POWER // 30)
    trigger_function(update_power)


@create_function('Update Power')
def update_power() -> None:
    with IfAnd(
        PLAYER_POWER > PLAYER_POWER_UPPER_BOUND,
    ):
        PLAYER_POWER_UPPER_BOUND.value = PLAYER_POWER
    with IfAnd(
        PLAYER_POWER < PLAYER_POWER_UPPER_BOUND,
    ):
        PLAYER_POWER.value = PLAYER_POWER_UPPER_BOUND
    with IfAnd(
        PLAYER_POWER > PLAYER_MAX_POWER,
    ):
        PLAYER_POWER.value = PLAYER_MAX_POWER


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


def quiet_reset_turf(
    turf: type[BaseTurf],
    set_hp: bool,
) -> None:
    turf.GANG.value = EMPTY_TURF_GANG
    turf.FUNDS.value = 0
    turf.FUNDS_PER_SECOND.value = 0
    if set_hp:
        turf.HP.value = turf.MAX_HP
    turf.HELD_FOR.value = 0


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
        quiet_reset_turf(turf, set_hp=False)
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
    for amount in (300,):
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
        PLAYER_GANG == SpawnTeam.ID,
    ):
        exit_function()
    max_hp_addition = PlayerStat('temp')
    max_hp_addition.value = PLAYER_PRESTIGE * TURF_HP_PER_PRESTIGE
    for turf in (Turf1, Turf2, Turf3):
        with IfAnd(
            turf.GANG == PLAYER_GANG
        ):
            turf.MAX_HP += max_hp_addition
            turf.MAX_HP += PLAYER_CURRENT_LEVEL


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

    for turf in (Turf1, Turf2, Turf3):
        with IfAnd(
            turf.HP > turf.HP_UPPER_BOUND,
        ):
            turf.HP_UPPER_BOUND.value = turf.HP
        with IfAnd(
            turf.HP < turf.HP_UPPER_BOUND,
        ):
            turf.HP.value = turf.HP_UPPER_BOUND
        with IfAnd(
            turf.HP > turf.MAX_HP,
        ):
            turf.HP.value = turf.MAX_HP

    # check duplicates
    # if (turfa.GANG == turfb.GANG) and (turfb.GANG != EMPTY_TURF_GANG):
    # is the same as not ((turfa.GANG != turfb.GANG) or (turfb.GANG == EMPTY_TURF_GANG))
    with IfOr(
        Turf2.GANG != Turf3.GANG,
        Turf3.GANG == EMPTY_TURF_GANG,
    ):
        pass
    with Else:
        quiet_reset_turf(Turf3, set_hp=True)
    with IfOr(
        Turf1.GANG != Turf3.GANG,
        Turf3.GANG == EMPTY_TURF_GANG,
    ):
        pass
    with Else:
        quiet_reset_turf(Turf3, set_hp=True)
    with IfOr(
        Turf1.GANG != Turf2.GANG,
        Turf2.GANG == EMPTY_TURF_GANG,
    ):
        pass
    with Else:
        quiet_reset_turf(Turf2, set_hp=True)


# LOOPS ==========================================================


@create_function('Daily Reset')
def daily_reset() -> None:
    """Reset daily things, called every day at midnight UTC"""
    with IfAnd(
        DAILY_FREE_SWITCHES < FREE_SWITCHES_PER_DAY,
    ):
        DAILY_FREE_SWITCHES.value = FREE_SWITCHES_PER_DAY
        chat(IMPORTANT_MESSAGE_PREFIX + f'&eYour daily free gang switches have been reset to&b {FREE_SWITCHES_PER_DAY}&e.')


@create_function('Decrement Buff Timers')
def decrement_buff_timers() -> None:
    for timer, dec_in_spawn in (
        (SPEED_EFFECT_TIMER, False),
        (RESISTANCE_EFFECT_TIMER, False),
        (REGENERATION_EFFECT_TIMER, False),
        (JUMPBOOST_EFFECT_TIMER, False),
        (INVISIBILITY_EFFECT_TIMER, False),
        (WEAPON_ABILITY_SPEED_TIMER, True),
        (WEAPON_ABILITY_REGEN_TIMER, True),
        (REGEN_ON_KILL_TIMER, True),
        (STRENGTH_ON_KILL_TIMER, True),
    ):
        if dec_in_spawn:
            with IfAnd(
                timer > 0,
            ):
                timer.value -= 1
        else:
            with IfOr(
                timer <= 0,
                BIGGEST_LOCATION_ID == LocationInstances.spawn.biggest_id,
            ):
                pass
            with Else:
                timer.value -= 1


@create_function('Personal 1s')
def personal_every_second() -> None:
    trigger_function(increment_power)
    PLAYTIME_SECONDS.value += 1
    with IfAnd(
        DAILY_RESET_LAST_DAY < TIME_DAY,
    ):
        DAILY_RESET_LAST_DAY.value = TIME_DAY
        trigger_function(daily_reset)
    trigger_function(set_player_team_function)
    trigger_function(set_player_group_function)
    trigger_function(update_teleports)
    trigger_function(decrement_buff_timers)


# NOTE have this run every 4 ticks
@create_function('Personal 0.2s')
def personal_every_4ticks() -> None:
    trigger_function(check_player_gang)
    trigger_function(check_locations)
    trigger_function(check_out_of_spawn)
    trigger_function(misc_every_4_ticks)
    trigger_function(check_levels)
    trigger_function(set_most_stats)
    trigger_function(update_display_stats)
    trigger_function(display_action_bar_and_title)
    trigger_function(apply_all_potion_effects)
    PERSONAL_EVERY_SECOND_INDEX.value += 1
    with IfAnd(
        PERSONAL_EVERY_SECOND_INDEX >= 5,
    ):
        PERSONAL_EVERY_SECOND_INDEX.value = 0
        trigger_function(personal_every_second)


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
            give_item(
                crown.item,
                allow_multiple=True,
                inventory_slot='helmet',
                replace_existing_item=True,
            )


def transfer_gang_leadership(
    reason: Literal['RANDOM', 'BETRAYAL', 'TRANSFER'] | None,
) -> None:
    TEAM_LEADER_ID.value = PLAYER_ID
    TEAM_LEADER_NOT_WORN_TIMER.value = 0
    trigger_function(put_crown_on_head)
    if reason is not None:
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
            gang.TEAM.players() > 1,
        ):
            transfer_gang_leadership('RANDOM')
            exit_function()
        with IfAnd(
            PLAYER_GANG == gang.ID,
            gang.LEADER_IS_WEARING_CROWN == 0,
            gang.LEADER_NOT_WORN_TIMER >= SECONDS_TO_TRANSFER_LEADERSHIP,
        ):
            transfer_gang_leadership(None)


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
    for gang, illegals, crown, chestplate in (
        (Bloods, (*crips_armor, *kings_armor, *grapes_armor), Items.bloods_leader_crown, Items.bloods_chestplate),
        (Crips, (*bloods_armor, *kings_armor, *grapes_armor), Items.crips_leader_crown, Items.crips_chestplate),
        (Kings, (*bloods_armor, *crips_armor, *grapes_armor), Items.kings_leader_crown, Items.kings_chestplate),
        (Grapes, (*bloods_armor, *crips_armor, *kings_armor), Items.grapes_leader_crown, Items.grapes_chestplate),
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

        with IfAnd(
            HasItem(crown.item, where_to_check='armor'),
            HasItem(crown.item, where_to_check='inventory'),
        ):
            remove_item(crown.item)

        with IfOr(
            PLAYER_GANG != gang.ID,
            HasItem(chestplate.item, where_to_check='armor'),
        ):
            pass
        with Else:
            give_item(chestplate.item, inventory_slot='chestplate', replace_existing_item=True)

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
        play_unable_sound()
    TELEPORTING_ID.value = 0
    TELEPORTING_TIMER.value = 0
    DISPLAY_ID.value = 0


def check_in_combat_and_exit() -> None:
    with IfAnd(
        COMBAT_TIMER > 0,
    ):
        chat(IMPORTANT_MESSAGE_PREFIX + '&cYou cannot teleport while in combat.')
        exit_function()


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
    with IfOr(
        BIGGEST_LOCATION_ID == LocationInstances.spawn.biggest_id,
        IsFlying,
    ):
        Teleports.SPAWN.execute()
        cancel_teleport(send_message=False)
        exit_function()

    check_in_combat_and_exit()

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
        trigger_function(reset_cookie_goal)
        exit_function()

    with IfAnd(
        LATEST_COOKIES == HouseCookies,
        HouseCookies < COOKIE_GOAL,
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


@create_function('Destroy Cookie Goal')  # lol why did I name it this
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
    chat('&aYou received&e +1,000⛁ Funds&7 (will change soon)')
    add_funds(1000)


# NOTE: have this get called by the command
@create_function('Give Cookie Command')
def give_cookie_command() -> None:
    give_item(Items.slash_cookie.item, allow_multiple=True)
    play_sound('Item Pickup')


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
    chat(IMPORTANT_MESSAGE_PREFIX + f'&eDay {TIME_DAY} has started!')


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
    with IfAnd(
        TELEPORTING_ID > 0,
    ):
        WaitingOnTeleportTitleActionBar.display()
        exit_function()

    seconds_in_between = 8
    seconds_per = 3
    messages = [
        f'&6&l{PLAYER_KILL_STREAK}&6-Streak&7 (&a{PLAYER_KILLS}K&7/&c{PLAYER_DEATHS}D&7)&3 {PLAYER_CURRENT_XP}/{PLAYER_CURRENT_REQUIRED_XP}xp',
        f'&7(&{Turf1.GANG}&l✯✯✯&e {Turf1.FUNDS}⛁&7) (&{Turf2.GANG}&l✯✯&e {Turf2.FUNDS}⛁&7) (&{Turf3.GANG}&l✯&e {Turf3.FUNDS}⛁&7)',
    ]

    modulo_by = (seconds_in_between + seconds_per) * len(messages)
    did_modulo_on = PlayerStat('temp')
    did_modulo_on.value = DateUnix
    did_modulo_on.value -= did_modulo_on // modulo_by * modulo_by
    for i, message in enumerate(messages):
        with IfAnd(
            did_modulo_on >= i * (seconds_in_between),
            did_modulo_on < i * (seconds_in_between) + seconds_per,
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
        exit_function()

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

    with IfOr(
        SELECTED_PERK_A == NamedPerks.extra_distribution_funds.index,
        SELECTED_PERK_B == NamedPerks.extra_distribution_funds.index,
    ):
        payout.value *= (100 + NamedPerks.extra_distribution_funds.unlocked_tier_stat * 40)
        payout.value //= 100

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
    DISPLAY_ARG_1.value = turf.FUNDS
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
        PLAYER_GANG,
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
        turf.HP_UPPER_BOUND.value = turf.HP
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
