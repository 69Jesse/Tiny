import math
import re

from typing import Optional


class ShowToUserError(Exception):
    pass
def human_format(num: int) -> str:
    return str(num)


SYMBOL_TO_MULTIPLIER: dict[str, int] = {
    'k': 10**3, 'K': 10**3,
    'm': 10**6, 'M': 10**6,
    'kk': 10**6, 'kK': 10**6,
    'Kk': 10**6, 'KK': 10**6,
    'b': 10**9, 'B': 10**9,
    't': 10**12, 'T': 10**12,
    'q': 10**15, 'Q': 10**18,
}
SYMBOL_REGEX = re.compile(r'^((?:\d|.|,){1,12})(?:' + '|'.join(SYMBOL_TO_MULTIPLIER.keys()) + r')$')
PERCENT_REGEX = re.compile(r'^(\d{1,3})(?:%|p)$')
FRACTION_REGEX = re.compile(r'^(\d{1,3})/(\d{1,3})$')


def _parse(
    value: int | str,
    *,
    maximum: Optional[int] = None,
) -> int:
    if isinstance(value, int):
        return value
    try:
        return int(value)
    except ValueError:
        pass
    lowered = value.lower()
    if maximum is not None:
        if lowered in ('a', 'all'):
            return maximum
        if lowered in ('h', 'half'):
            return math.ceil(maximum / 2)
        if lowered in ('q', 'quarter'):
            return math.ceil(maximum / 4)
    match = SYMBOL_REGEX.match(lowered)
    if match is not None:
        return math.ceil(float(match.group(1).replace(',', '')) * SYMBOL_TO_MULTIPLIER[lowered[-1]])
    if maximum is not None:
        match = PERCENT_REGEX.match(lowered)
        if match is not None:
            return math.ceil(maximum * int(match.group(1)) / 100)
        match = FRACTION_REGEX.match(lowered)
        if match is not None:
            return math.ceil(maximum * int(match.group(1)) / int(match.group(2)))
    raise ValueError(f'Unable to parse {value!r} as an integer.')


def parse_integer(
    value: int | str,
    *,
    maximum: Optional[int] = None,
    minimum: int = 1,
) -> int:
    try:
        value = _parse(value, maximum=maximum)
    except ValueError:
        raise ShowToUserError(f'I was unable to turn `{value}` into a number..')

    if value < minimum:
        raise ShowToUserError(f'You must bet at least **{human_format(minimum)}**')
    if maximum is not None and value > maximum:
        raise ShowToUserError(f'You do not have enough currency to bet **{human_format(value)}**.')

    return value


"""
>>> from parse_integer import parse_integer
>>> parse_integer(1, maximum=1_000)
1
>>> parse_integer('1', maximum=1_000)
1
>>> parse_integer('1k', maximum=1_000)
1000
>>> parse_integer('1K', maximum=1_000)
1000
>>> parse_integer('1m', maximum=1_000_000)
1000000
>>> parse_integer('1.234k', maximum=1_000_000)
1234
>>> parse_integer('all', maximum=1_000_000)
1000000
>>> parse_integer('h', maximum=1_000_000)
500000
>>> parse_integer('q', maximum=1_000_000)
250000
>>> parse_integer('1/2', maximum=1_000_000)
500000
>>> parse_integer('1/4', maximum=1_000_000)
250000
>>> parse_integer('2/3', maximum=1_000_000)
666667
>>> parse_integer('50%', maximum=1_000_000)
500000
>>> parse_integer('25%', maximum=1_000_000)
250000
"""
