import math
import re


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


def parse_integer(
    value: int | str,
    *,
    maximum: int,
    minimum: int = 1,
) -> int:
    def parse(v: int | str) -> int:
        if isinstance(v, int):
            return v
        try:
            return int(v)
        except ValueError:
            pass
        lowered = v.lower()
        if lowered in ('a', 'all'):
            return maximum
        if lowered in ('h', 'half'):
            return math.ceil(maximum / 2)
        if lowered in ('q', 'quarter'):
            return math.ceil(maximum / 4)
        match = SYMBOL_REGEX.match(lowered)
        if match is not None:
            return math.ceil(float(match.group(1).replace(',', '')) * SYMBOL_TO_MULTIPLIER[lowered[-1]])
        match = PERCENT_REGEX.match(lowered)
        if match is not None:
            return math.ceil(maximum * int(match.group(1)) / 100)
        match = FRACTION_REGEX.match(lowered)
        if match is not None:
            return math.ceil(maximum * int(match.group(1)) / int(match.group(2)))
        raise ValueError

    try:
        value = parse(value)
    except ValueError:
        raise ShowToUserError(f'I was not able to turn `{value}` into a number..')

    if value < minimum:
        raise ShowToUserError(f'You must bet at least {human_format(minimum)} marbles.')
    if value > maximum:
        raise ShowToUserError(f'You do not have enough marbles to bet {human_format(value)}.')

    return value


assert parse_integer(1, maximum=1_000) == 1
assert parse_integer('1', maximum=1_000) == 1
assert parse_integer('1k', maximum=1_000) == 1_000
assert parse_integer('1K', maximum=1_000) == 1_000
assert parse_integer('1m', maximum=1_000_000) == 1_000_000
assert parse_integer('1.234k', maximum=1_000_000) == 1_234
assert parse_integer('all', maximum=1_000_000) == 1_000_000
assert parse_integer('h', maximum=1_000_000) == 500_000
assert parse_integer('q', maximum=1_000_000) == 250_000
assert parse_integer('1/2', maximum=1_000_000) == 500_000
assert parse_integer('1/4', maximum=1_000_000) == 250_000
assert parse_integer('2/3', maximum=1_000_000) == 666_667
assert parse_integer('50%', maximum=1_000_000) == 500_000
assert parse_integer('25%', maximum=1_000_000) == 250_000
