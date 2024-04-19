from pyhtsl import (
    Team,
    GlobalStat,
    PlayerStat,
)

import re

from typing import Optional


class Teams:
    __slots__ = ()
    combat = Team('Combat')
    mining = Team('Mining')
    farming = Team('Farming')
    fishing = Team('Fishing')


class GlobalStats:
    __slots__ = ()
    latest_cookies = GlobalStat('latest_cookies')
    cookie_goal = GlobalStat('cookie_goal')
    cookies_needed = GlobalStat('cookies_needed')


LINE_REGEX = re.compile(r'^(x+)(\.*)$')
def fetch_digits(
    fetch_from: PlayerStat,
    assign_to: PlayerStat,
    line: Optional[str] = None,
    *,
    size: Optional[int] = None,
    right_offset: Optional[int] = None,
) -> None:
    if line is None:
        assert size is not None and right_offset is not None
    else:
        match = LINE_REGEX.match(line)
        assert match is not None
        size = len(match.group(1))
        right_offset = len(match.group(2))
    high, low = 10 ** (size + right_offset), 10 ** right_offset
    assign_to.value = (fetch_from - (fetch_from // high * high)) // low
