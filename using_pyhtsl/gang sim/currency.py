from pyhtsl import PlayerStat

from stats import FUNDS, CRED

from title_action_bar import (
    AddFundsTitleActionBar,
    RemoveFundsTitleActionBar,
    AddCredAndFundsTitleActionBar,
)


def add_funds(
    amount: int | PlayerStat,
) -> None:
    FUNDS.value += amount
    AddFundsTitleActionBar.apply(amount)


def remove_funds(
    amount: int | PlayerStat,
) -> None:
    FUNDS.value -= amount
    RemoveFundsTitleActionBar.apply(amount)


def add_funds_and_cred(
    cred: int | PlayerStat,
    funds: int | PlayerStat,
) -> None:
    CRED.value += cred
    FUNDS.value += funds
    AddCredAndFundsTitleActionBar.apply(cred, funds)
