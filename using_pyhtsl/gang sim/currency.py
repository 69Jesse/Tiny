from pyhtsl import PlayerStat

from constants import PLAYER_FUNDS, PLAYER_CRED

from title_action_bar import (
    AddFundsTitleActionBar,
    RemoveFundsTitleActionBar,
    AddCredAndFundsTitleActionBar,
)


def add_funds(
    amount: int | PlayerStat,
) -> None:
    PLAYER_FUNDS.value += amount
    AddFundsTitleActionBar.apply(amount)


def remove_funds(
    amount: int | PlayerStat,
) -> None:
    PLAYER_FUNDS.value -= amount
    RemoveFundsTitleActionBar.apply(amount)


def add_funds_and_cred(
    cred: int | PlayerStat,
    funds: int | PlayerStat,
) -> None:
    PLAYER_CRED.value += cred
    PLAYER_FUNDS.value += funds
    AddCredAndFundsTitleActionBar.apply(cred, funds)
