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

from constants import (
    PLAYER_POWER,
    PLAYER_MAX_POWER,
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
    @abstractmethod
    def display() -> None:
        pass


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
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(3)

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
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(3)

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
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(3)

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
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(3)

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
        DISPLAY_TIMER.value = seconds_to_every_4_ticks(3)

    @staticmethod
    def display() -> None:
        display_action_bar(
            f'&4{PLAYER_POWER}/{PLAYER_MAX_POWER}⸎&a +&2{DISPLAY_ARG_1}©&a +&2{DISPLAY_ARG_2}⛁',
        )


# TODO add more action bars? prestige with title instead of action bar and shit


def get_title_action_bars() -> list[type[TitleActionBar]]:
    return TitleActionBar.__subclasses__()
