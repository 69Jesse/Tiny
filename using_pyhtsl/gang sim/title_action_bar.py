from pyhtsl import (
    create_function,
    trigger_function,
    IfAnd,
    IfOr,
    Else,
    exit_function,
    DateUnix,
    Function,
    display_action_bar,
    PlayerStat,
    RequiredTeam,
)

from stats import (
    POWER,
    MAX_POWER,
    DISPLAY_ID,
    DISPLAY_TIMER,
    DISPLAY_ARG_1,
    DISPLAY_ARG_2,
    DISPLAY_ARG_3,
    LOCATION_ID,
    TEAM_ID,
    TURF_1_GANG,
    TURF_2_GANG,
    TURF_3_GANG,
)
from locations import LOCATIONS

from abc import ABC, abstractmethod
from typing import final


# run every 4 ticks
def maybe_update_display_stats() -> None:
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


def seconds_to_ticks(seconds: int) -> int:
    return seconds * 20


class TitleActionBar(ABC):
    @staticmethod
    @abstractmethod
    def get_id() -> int:
        pass

    @classmethod
    def set_id(cls) -> None:
        DISPLAY_ID.value = cls.get_id()

    @staticmethod
    @abstractmethod
    def apply() -> None:
        pass

    @staticmethod
    @abstractmethod
    def display() -> None:
        pass


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

    visited_ids: set[int] = set()
    for location in LOCATIONS.walk():
        if location.id in visited_ids:
            continue
        visited_ids.add(location.id)
        with IfAnd(
            LOCATION_ID == location.id,
        ):
            display_action_bar(
                f'&b⏣ {location.name}&4 {POWER}/{MAX_POWER}⸎&{DISPLAY_ARG_1} &l✯&{DISPLAY_ARG_2}&l✯&{DISPLAY_ARG_3}&l✯',
            )


@final
class RegularTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 0

    @staticmethod
    def apply() -> None:
        raise ValueError('Regular Action Bar cannot be applied')

    @staticmethod
    def display() -> None:
        trigger_function(regular_action_bar_display)


@final
class RemovePowerTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 1

    @staticmethod
    def apply(
        power: int | PlayerStat,
    ) -> None:
        DISPLAY_ARG_1.value = power
        DISPLAY_TIMER.value = seconds_to_ticks(1)

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&4{POWER}/{MAX_POWER}⸎ -{DISPLAY_ARG_1}',
        )


@final
class AddCredTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 2

    @staticmethod
    def apply(
        cred: int | PlayerStat,
    ) -> None:
        DISPLAY_ARG_1.value = cred
        DISPLAY_TIMER.value = seconds_to_ticks(3)

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&4{POWER}/{MAX_POWER}⸎&2 +{DISPLAY_ARG_1}© Cred',
        )


@final
class AddFundsTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 3

    @staticmethod
    def apply(
        funds: int | PlayerStat,
    ) -> None:
        DISPLAY_ARG_1.value = funds
        DISPLAY_TIMER.value = seconds_to_ticks(3)

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&4{POWER}/{MAX_POWER}⸎&e +{DISPLAY_ARG_1}⛁ Funds',
        )


@final
class RemoveCredTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 4

    @staticmethod
    def apply(
        removed_cred: int | PlayerStat,
    ) -> None:
        DISPLAY_ARG_1.value = removed_cred
        DISPLAY_TIMER.value = seconds_to_ticks(3)

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&4{POWER}/{MAX_POWER}⸎&c -{DISPLAY_ARG_1}© Cred',
        )


@final
class RemoveFundsTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 5

    @staticmethod
    def apply(
        removed_funds: int | PlayerStat,
    ) -> None:
        DISPLAY_ARG_1.value = removed_funds
        DISPLAY_TIMER.value = seconds_to_ticks(3)

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&4{POWER}/{MAX_POWER}⸎&6 -{DISPLAY_ARG_1}⛁ Funds',
        )


@final
class AddCredAndFundsTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 6

    @staticmethod
    def apply(
        cred: int | PlayerStat,
        funds: int | PlayerStat,
    ) -> None:
        DISPLAY_ARG_1.value = cred
        DISPLAY_ARG_2.value = funds
        DISPLAY_TIMER.value = seconds_to_ticks(3)

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&4{POWER}/{MAX_POWER}⸎&2 +{DISPLAY_ARG_1}©&e +{DISPLAY_ARG_2}⛁',
        )


# TODO add more action bars? prestige with title instead of action bar and shit


def get_title_action_bars() -> list[type[TitleActionBar]]:
    return TitleActionBar.__subclasses__()


@create_function('Display Action Bar or Title')
def display_action_bar_or_title() -> None:
    for action_bar in get_title_action_bars():
        with IfAnd(
            DISPLAY_ID == action_bar.get_id(),
        ):
            action_bar.display()
