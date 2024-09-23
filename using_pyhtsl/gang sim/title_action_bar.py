from pyhtsl import (
    display_action_bar,
    PlayerStat,
    Function,
    display_title,
    IfAnd,
    GlobalStat,
    trigger_function,
    Else,
    play_sound,
    TeamColor,
    TeamName,
    chat,
    TeamStat,
)
from pyhtsl.types import Condition

from constants import (
    PLAYER_POWER,
    PLAYER_MAX_POWER,
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
    Turf1,
    Turf2,
    Turf3,
    PLAYER_KILL_STREAK,
    PLAYER_CURRENT_LEVEL,
    PLAYER_CURRENT_XP,
    PLAYER_CURRENT_REQUIRED_XP,
    IMPORTANT_MESSAGE_PREFIX,
    TELEPORTING_TIMER,
    seconds_to_every_4_ticks,
    GangSimGang,
    Bloods,
    Crips,
    Kings,
    Grapes,
)

from abc import ABC, abstractmethod
from typing import final, Literal


class TitleActionBar(ABC):
    @staticmethod
    @abstractmethod
    def get_id() -> int:
        pass

    @classmethod
    def set_id(cls) -> None:
        DISPLAY_ID.value = cls.get_id()

    @classmethod
    @abstractmethod
    def apply(cls) -> None:
        pass

    @staticmethod
    def apply_globals() -> None:
        pass

    @staticmethod
    @abstractmethod
    def display() -> None:
        pass

    @staticmethod
    def is_regular() -> bool:
        return True

    @classmethod
    def display_irregular(cls) -> None:
        pass

    @classmethod
    def get_condition(cls) -> Condition:
        return DISPLAY_ID == cls.get_id()

    REGULAR_ACTION_BAR_DISPLAY_FUNCTION: Function = Function('Regular Action Bar Display')


@final
class RemovePowerTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 1

    @classmethod
    def apply(
        cls,
        power: int | PlayerStat,
    ) -> None:
        cls.set_id()
        DISPLAY_ARG_1.value = power
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(1)

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&4{PLAYER_POWER}/{PLAYER_MAX_POWER}⸎&c -&4{DISPLAY_ARG_1}⸎ Power',
        )


@final
class AddCredTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 2

    @classmethod
    def apply(
        cls,
        cred: int | PlayerStat,
    ) -> None:
        cls.set_id()
        DISPLAY_ARG_1.value = cred
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(2)
        play_sound('Successful Hit')

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&4{PLAYER_POWER}/{PLAYER_MAX_POWER}⸎&a +&2{DISPLAY_ARG_1}© Cred',
        )


@final
class AddFundsTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 3

    @classmethod
    def apply(
        cls,
        funds: int | PlayerStat,
    ) -> None:
        cls.set_id()
        DISPLAY_ARG_1.value = funds
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(2)
        play_sound('Item Pickup')

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&4{PLAYER_POWER}/{PLAYER_MAX_POWER}⸎&a +&e{DISPLAY_ARG_1}⛁ Funds',
        )


@final
class RemoveCredTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 4

    @classmethod
    def apply(
        cls,
        removed_cred: int | PlayerStat,
    ) -> None:
        cls.set_id()
        DISPLAY_ARG_1.value = removed_cred
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(2)

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&4{PLAYER_POWER}/{PLAYER_MAX_POWER}⸎&c -&2{DISPLAY_ARG_1}© Cred',
        )


@final
class RemoveFundsTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 5

    @classmethod
    def apply(
        cls,
        removed_funds: int | PlayerStat,
    ) -> None:
        cls.set_id()
        DISPLAY_ARG_1.value = removed_funds
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(2)

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&4{PLAYER_POWER}/{PLAYER_MAX_POWER}⸎&c -&e{DISPLAY_ARG_1}⛁ Funds',
        )


@final
class AddCredAndFundsTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 6

    @classmethod
    def apply(
        cls,
        cred: int | PlayerStat,
        funds: int | PlayerStat,
    ) -> None:
        cls.set_id()
        DISPLAY_ARG_1.value = cred
        DISPLAY_ARG_2.value = funds
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(2)
        play_sound('Successful Hit')

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&4{PLAYER_POWER}/{PLAYER_MAX_POWER}⸎&a +&2{DISPLAY_ARG_1}©&a +&e{DISPLAY_ARG_2}⛁',
        )


@final
class TurfDestroyedTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 7

    @classmethod
    def apply(
        cls,
        added_funds: int | GlobalStat,
    ) -> None:
        cls.set_id()
        DISPLAY_ARG_1.value = added_funds
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(4)
        for number, name in (
            (Turf1.ID, 'Alpha'),
            (Turf2.ID, 'Beta'),
            (Turf3.ID, 'Gamma'),
        ):
            with IfAnd(
                GLOBAL_DISPLAY_ARG_1 == number,
            ):
                chat(IMPORTANT_MESSAGE_PREFIX + f'&eTurf&b {name[0]}&a{name[1:]}&{GLOBAL_DISPLAY_ARG_2}&l DESTROYED&e by&{GLOBAL_DISPLAY_ARG_4} P#{GLOBAL_DISPLAY_ARG_3}')
        play_sound('Wither Death')

    @staticmethod
    def apply_globals(
        destroyed_turf: int,
        destroyed_gang: int | GlobalStat,
        destroyer_id: int | PlayerStat,
        destroyer_gang: int | PlayerStat,
        funds_stolen: int | GlobalStat,
        seconds_held: int | GlobalStat,
    ) -> None:
        GLOBAL_DISPLAY_ARG_1.value = destroyed_turf
        GLOBAL_DISPLAY_ARG_2.value = destroyed_gang
        GLOBAL_DISPLAY_ARG_3.value = destroyer_id
        GLOBAL_DISPLAY_ARG_4.value = destroyer_gang
        GLOBAL_DISPLAY_ARG_5.value = funds_stolen
        GLOBAL_DISPLAY_ARG_6.value = seconds_held

    @staticmethod
    def is_regular() -> bool:
        return False

    @staticmethod
    def display() -> None:
        raise

    @classmethod
    def display_irregular(cls) -> None:
        # display_action_bar(
        #     f'&4{PLAYER_POWER}/{PLAYER_MAX_POWER}⸎&a +&2{DISPLAY_ARG_1}©&a +&2{DISPLAY_ARG_2}⛁',
        # )
        for number, name, stars in (
            (Turf1.ID, 'Alpha', '✯✯✯'),
            (Turf2.ID, 'Beta', '✯✯'),
            (Turf3.ID, 'Gamma', '✯'),
        ):
            with IfAnd(
                cls.get_condition(),
                GLOBAL_DISPLAY_ARG_1.value == number,
            ):
                display_title(
                    title=f'&eTurf&b {name[0]}&a{name[1:]}&{GLOBAL_DISPLAY_ARG_2}&l DESTROYED',
                    subtitle=f'&aBy&{GLOBAL_DISPLAY_ARG_4} P#{GLOBAL_DISPLAY_ARG_3}&a, it held&e {GLOBAL_DISPLAY_ARG_5}⛁&7 (&{GLOBAL_DISPLAY_ARG_2}&l{stars}&{GLOBAL_DISPLAY_ARG_2} {GLOBAL_DISPLAY_ARG_6}s&7)',
                    fadein=0,
                    stay=1,
                    fadeout=0,
                )
        with IfAnd(
            cls.get_condition(),
            DISPLAY_ARG_1 == 0,
        ):
            trigger_function(
                TitleActionBar.REGULAR_ACTION_BAR_DISPLAY_FUNCTION
            )
        with IfAnd(
            cls.get_condition(),
            DISPLAY_ARG_1 > 0,
        ):
            AddFundsTitleActionBar.display()


@final
class TurfCapturedTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 8

    @classmethod
    def apply(
        cls,
    ) -> None:
        cls.set_id()
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(4)
        for number, name in (
            (Turf1.ID, 'Alpha'),
            (Turf2.ID, 'Beta'),
            (Turf3.ID, 'Gamma'),
        ):
            with IfAnd(
                GLOBAL_DISPLAY_ARG_1 == number,
                GLOBAL_DISPLAY_ARG_5 == 0,
            ):
                chat(IMPORTANT_MESSAGE_PREFIX + f'&eTurf&b {name[0]}&a{name[1:]}&{GLOBAL_DISPLAY_ARG_2}&l CAPTURED&e by&{GLOBAL_DISPLAY_ARG_3}')
            with IfAnd(
                GLOBAL_DISPLAY_ARG_1 == number,
                GLOBAL_DISPLAY_ARG_5 == 1,
            ):
                chat(IMPORTANT_MESSAGE_PREFIX + f'&eTurf&b {name[0]}&a{name[1:]}&{GLOBAL_DISPLAY_ARG_2}&l CAPTURED&e by&{GLOBAL_DISPLAY_ARG_3}&7 (&aPROMOTION&7)')
        play_sound('Wither Death')

    @staticmethod
    def apply_globals(
        captured_turf: int,
        captured_gang: int | GlobalStat,
        capturer_id: int | PlayerStat,
        turf_earnings: int | GlobalStat,
        is_promotion: PlayerStat,
    ) -> None:
        GLOBAL_DISPLAY_ARG_1.value = captured_turf
        GLOBAL_DISPLAY_ARG_2.value = captured_gang
        GLOBAL_DISPLAY_ARG_3.value = capturer_id
        GLOBAL_DISPLAY_ARG_4.value = turf_earnings
        GLOBAL_DISPLAY_ARG_5.value = is_promotion

    @staticmethod
    def is_regular() -> bool:
        return False

    @staticmethod
    def display() -> None:
        raise

    @classmethod
    def display_irregular(cls) -> None:
        # display_action_bar(
        #     f'&4{PLAYER_POWER}/{PLAYER_MAX_POWER}⸎&a +&2{DISPLAY_ARG_1}©&a +&2{DISPLAY_ARG_2}⛁',
        # )
        for number, name, stars in (
            (Turf1.ID, 'Alpha', '✯✯✯'),
            (Turf2.ID, 'Beta', '✯✯'),
            (Turf3.ID, 'Gamma', '✯'),
        ):
            with IfAnd(
                cls.get_condition(),
                GLOBAL_DISPLAY_ARG_1.value == number,
                GLOBAL_DISPLAY_ARG_5 == 0,
            ):
                display_title(
                    title=f'&eTurf&b {name[0]}&a{name[1:]}&{GLOBAL_DISPLAY_ARG_2}&l CAPTURED',
                    subtitle=f'&aBy&{GLOBAL_DISPLAY_ARG_2} P#{GLOBAL_DISPLAY_ARG_3}&a, it earns&e +{GLOBAL_DISPLAY_ARG_4}/s&7 (&{GLOBAL_DISPLAY_ARG_2}&l{stars}&{GLOBAL_DISPLAY_ARG_2}&7)',
                    fadein=0,
                    stay=1,
                    fadeout=0,
                )
            with IfAnd(
                cls.get_condition(),
                GLOBAL_DISPLAY_ARG_1.value == number,
                GLOBAL_DISPLAY_ARG_5 == 1,
            ):
                display_title(
                    title=f'&eTurf&b {name[0]}&a{name[1:]}&{GLOBAL_DISPLAY_ARG_2}&l CAPTURED',
                    subtitle=f'&aPROMOTION by&{GLOBAL_DISPLAY_ARG_2} P#{GLOBAL_DISPLAY_ARG_3}&a, it earns&e +{GLOBAL_DISPLAY_ARG_4}/s&7 (&{GLOBAL_DISPLAY_ARG_2}&l{stars}&{GLOBAL_DISPLAY_ARG_2}&7)',
                    fadein=0,
                    stay=1,
                    fadeout=0,
                )
        with IfAnd(
            cls.get_condition(),
        ):
            trigger_function(
                TitleActionBar.REGULAR_ACTION_BAR_DISPLAY_FUNCTION
            )


class OnKillTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 9

    @classmethod
    def apply(
        cls,
        added_funds: int | PlayerStat,
        added_cred: int | PlayerStat,
        added_experience: int | PlayerStat,
    ) -> None:
        cls.set_id()
        DISPLAY_ARG_1.value = added_funds
        DISPLAY_ARG_2.value = added_cred
        DISPLAY_ARG_3.value = added_experience
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(2)
        play_sound('Successful Hit')

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&4&lNICE KILL&6&l {PLAYER_KILL_STREAK}&6-Streak&a +&e{DISPLAY_ARG_1}⛁&a +&2{DISPLAY_ARG_2}©&a +&3{DISPLAY_ARG_3}xp',
        )


class OnBadKillTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 10

    @classmethod
    def apply(
        cls,
        removed_cred: int | PlayerStat,
    ) -> None:
        cls.set_id()
        DISPLAY_ARG_1.value = removed_cred
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(2)
        chat(IMPORTANT_MESSAGE_PREFIX + f'&4&lBAD KILL&7 why??&c -&2{DISPLAY_ARG_1}©')
        play_sound('Anvil Land')

    @staticmethod
    def display() -> None:
        display_title(
            title=f'&4&lBAD KILL&7 why??&c -&2{DISPLAY_ARG_1}©',
            subtitle='&8Do not kill members of your own gang!',
            fadein=0,
            stay=1,
            fadeout=0,
        )
        display_action_bar(
            f'&4&lBAD KILL&7 why??&c -&2{DISPLAY_ARG_1}©',
        )


class OnDeathTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 11

    @classmethod
    def apply(
        cls,
        removed_cred: int | PlayerStat,
        previous_streak: int | PlayerStat,
    ) -> None:
        cls.set_id()
        DISPLAY_ARG_1.value = removed_cred
        DISPLAY_ARG_2.value = previous_streak
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(2)
        play_sound('Fall Big')

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&4&lYOU DIED&7 with&6&l {DISPLAY_ARG_2}&6-Streak&c -&2{DISPLAY_ARG_1}©',
        )


class LevelUpTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 12

    @classmethod
    def apply(
        cls,
        old_level: int | PlayerStat,
    ) -> None:
        cls.set_id()
        DISPLAY_ARG_1.value = old_level
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(4)
        play_sound('Level Up')

    @staticmethod
    def display() -> None:
        display_title(
            title=f'{TeamColor}&l{TeamName} LEVEL UP',
            subtitle=f'&3Level{TeamColor} {DISPLAY_ARG_1}&3 ->{DISPLAY_ARG_1}&l {PLAYER_CURRENT_LEVEL}&7 (&3{PLAYER_CURRENT_XP}/{PLAYER_CURRENT_REQUIRED_XP}&7)',
            fadein=0,
            stay=1,
            fadeout=0,
        )
        trigger_function(
            TitleActionBar.REGULAR_ACTION_BAR_DISPLAY_FUNCTION
        )


class WaitingOnTeleportTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 13

    @classmethod
    def apply(cls) -> None:
        cls.set_id()
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(30)

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&eTeleporting in&c {TELEPORTING_TIMER}s',
        )


REASON_TO_NUMBER = {
    'RANDOM': 0,
    'BETRAYAL': 1,
    'TRANSFER': 2,
    # 'BOUGHT': 3,  # TODO I want people to be able to buy leadership if current leader is dead for like 100*members funds
}
NUMBER_TO_REASON = {
    0: 'RANDOM',
    1: 'BETRAYAL',
    2: 'TRANSFER',
    # 3: 'BOUGHT',
}


class NewGangLeaderTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 14

    @classmethod
    def apply(
        cls,
    ) -> None:
        cls.set_id()
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(2)
        for gang in (
            Bloods, Crips, Kings, Grapes,
        ):
            for reason_number, reason in NUMBER_TO_REASON.items():
                with IfAnd(
                    GLOBAL_DISPLAY_ARG_2 == gang.ID,
                    GLOBAL_DISPLAY_ARG_3 == reason_number,
                ):
                    chat(IMPORTANT_MESSAGE_PREFIX + f'&{gang.ID}&lNEW {gang.name().upper()} LEADER&e P#{GLOBAL_DISPLAY_ARG_1}&7 (&a{reason}&7)')
        play_sound('Ambience Thunder')

    @classmethod
    def apply_globals(
        cls,
        new_leader_id: PlayerStat,
        new_leader_gang_id: int | PlayerStat | TeamStat,
        reason: Literal['RANDOM', 'BETRAYAL', 'TRANSFER'], # 'BOUGHT'],
    ) -> None:
        GLOBAL_DISPLAY_ARG_1.value = new_leader_id
        GLOBAL_DISPLAY_ARG_2.value = new_leader_gang_id
        GLOBAL_DISPLAY_ARG_3.value = REASON_TO_NUMBER[reason]

    @staticmethod
    def is_regular() -> bool:
        return False

    @staticmethod
    def display_irregular() -> None:
        for gang in (
            Bloods, Crips, Kings, Grapes,
        ):
            for reason_number, reason in NUMBER_TO_REASON.items():
                with IfAnd(
                    NewGangLeaderTitleActionBar.get_condition(),
                    GLOBAL_DISPLAY_ARG_2 == gang.ID,
                    GLOBAL_DISPLAY_ARG_3 == reason_number,
                ):
                    display_title(
                        title=f'&{gang.ID}&lNEW {gang.name().upper()} LEADER',
                        subtitle=f'&eThey are&{gang.ID} P#{GLOBAL_DISPLAY_ARG_1}&7 (&a{reason}&7)',
                        fadein=0,
                        stay=1,
                        fadeout=0,
                    )
        with IfAnd(
            NewGangLeaderTitleActionBar.get_condition(),
        ):
            trigger_function(
                TitleActionBar.REGULAR_ACTION_BAR_DISPLAY_FUNCTION
            )


class GangLeaderFallenTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 100000000  # not actually applying

    @classmethod
    def apply(
        cls,
    ) -> None:
        for gang in (
            Bloods, Crips, Kings, Grapes,
        ):
            with IfAnd(
                GLOBAL_DISPLAY_ARG_1 == gang.ID,
            ):
                chat(IMPORTANT_MESSAGE_PREFIX + f'&{gang.ID}&l{gang.name().upper()} LEADER FALLEN')
        play_sound('Ambience Thunder')

    @classmethod
    def apply_globals(
        cls,
        gang: type[GangSimGang],
    ) -> None:
        GLOBAL_DISPLAY_ARG_1.value = gang.ID

    @staticmethod
    def is_regular() -> bool:
        return False

    @staticmethod
    def display_irregular() -> None:
        pass


# TODO add more action bars? prestige with title instead of action bar and shit


def get_title_action_bars() -> list[type[TitleActionBar]]:
    return TitleActionBar.__subclasses__()
