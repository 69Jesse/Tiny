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
)

from abc import ABC, abstractmethod
from typing import final


def seconds_to_every_4_ticks(seconds: int) -> int:
    return seconds * 5


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
    PROMOTION_PLAYER_ID = -999999999

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
    def set_promotion_player_id() -> None:
        GLOBAL_DISPLAY_ARG_3.value = TurfDestroyedTitleActionBar.PROMOTION_PLAYER_ID

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
                GLOBAL_DISPLAY_ARG_3 > cls.PROMOTION_PLAYER_ID,
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
                GLOBAL_DISPLAY_ARG_1.value == number,
                GLOBAL_DISPLAY_ARG_3 == cls.PROMOTION_PLAYER_ID,
            ):
                display_title(
                    title=f'&eTurf&b {name[0]}&a{name[1:]}&{GLOBAL_DISPLAY_ARG_2}&l DESTROYED',
                    subtitle=f'&aPROMOTION, it held&e {GLOBAL_DISPLAY_ARG_5}⛁&7 (&{GLOBAL_DISPLAY_ARG_2}&l{stars}&{GLOBAL_DISPLAY_ARG_2} {GLOBAL_DISPLAY_ARG_6}s&7)',
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
        play_sound('Wither Death')

    @staticmethod
    def apply_globals(
        captured_turf: int,
        captured_gang: int | GlobalStat,
        capturer_id: int | PlayerStat,
        turf_earnings: int | GlobalStat,
    ) -> None:
        GLOBAL_DISPLAY_ARG_1.value = captured_turf
        GLOBAL_DISPLAY_ARG_2.value = captured_gang
        GLOBAL_DISPLAY_ARG_3.value = capturer_id
        GLOBAL_DISPLAY_ARG_4.value = turf_earnings

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
        for number, name in (
            (Turf1.ID, 'Alpha'),
            (Turf2.ID, 'Beta'),
            (Turf3.ID, 'Gamma'),
        ):
            with IfAnd(
                cls.get_condition(),
                GLOBAL_DISPLAY_ARG_1.value == number,
            ):
                display_title(
                    title=f'&eTurf&b {name[0]}&a{name[1:]}&{GLOBAL_DISPLAY_ARG_2}&l CAPTURED',
                    subtitle=f'&aBy&{GLOBAL_DISPLAY_ARG_2} P#{GLOBAL_DISPLAY_ARG_3}&a, it earns&e +{GLOBAL_DISPLAY_ARG_4}/s&7 (&{GLOBAL_DISPLAY_ARG_2}&l✯✯✯&{GLOBAL_DISPLAY_ARG_2}&7)',
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
        added_funds: int | GlobalStat,
        added_cred: int | GlobalStat,
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
        removed_cred: int | GlobalStat,
    ) -> None:
        cls.set_id()
        DISPLAY_ARG_1.value = removed_cred
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(2)
        play_sound('Anvil Land')

    @staticmethod
    def display() -> None:
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
        removed_cred: int | GlobalStat,
        previous_streak: int | GlobalStat,
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


# TODO add more action bars? prestige with title instead of action bar and shit


def get_title_action_bars() -> list[type[TitleActionBar]]:
    return TitleActionBar.__subclasses__()
