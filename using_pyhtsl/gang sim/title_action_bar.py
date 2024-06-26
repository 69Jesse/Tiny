from pyhtsl import (
    create_function,
    trigger_function,
    IfAnd,
    exit_function,
    DateUnix,
    Function,
    display_action_bar,
    PlayerStat,
)

from stats.playerstats import (
    POWER,
    MAX_POWER,
    DISPLAY_ID,
    DISPLAY_TIMER,
    DISPLAY_ARG_1,
    DISPLAY_ARG_2,
    DISPLAY_ARG_3,
    FUNDS_PER_SECOND,
    LOCATION_ID,
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
    for location in LOCATIONS.walk():
        with IfAnd(
            LOCATION_ID == location.id,
        ):
            display_action_bar(
                f'&b⏣ {location.name}&3 &4{POWER}/{MAX_POWER} &e+{FUNDS_PER_SECOND}⛁/s',
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
            f'&4{POWER}/{MAX_POWER} -{DISPLAY_ARG_1}',
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
            f'&4{POWER}/{MAX_POWER}&2 +{DISPLAY_ARG_1}© Cred',
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
            f'&4{POWER}/{MAX_POWER}&e +{DISPLAY_ARG_1}⛁ Funds',
        )


@final
class AddCredAndFundsTitleActionBar(TitleActionBar):
    @staticmethod
    def get_id() -> int:
        return 4

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
            f'&4{POWER}/{MAX_POWER}&2 +{DISPLAY_ARG_1}©&e +{DISPLAY_ARG_2}⛁',
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
