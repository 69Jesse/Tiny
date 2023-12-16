symbols: tuple[str, ...] = (
    'K',  # 1.0e3, thousand
    'M',  # 1.0e6, million
    'B',  # 1.0e9, billion
    'T',  # 1.0e12, trillion
    'q',  # 1.0e15, quadrillion
    'Q',  # 1.0e18, quintillion
)
def human_format(
    num: int,
    *,
    max_decimals: int = 5,
    maybe_plus: bool = False,
    decimal_point: str = '.',
) -> str:
    """
    Formats an integer to make it readable,
    always removes trailing 0s as decimals.

    Parameters
    ------------
    num: :class:`int`
        The number to format.
    max_decimals: :class:`int`
        The maximum number of decimals to show.
        If -1, it will show all decimals.
        Defaults to 5.
    maybe_plus: :class:`bool`
        Whether to show a plus sign if the number is positive.
        Defaults to False.
    decimal_point: :class:`str`
        The decimal point to use when relevant.
        Defaults to ``'.'``.
    """
    prefix = '+' if maybe_plus and num >= 0 else ('-' if num < 0 else '')
    num = abs(int(num))
    if num < 1000:
        return f'{prefix}{num}'
    stringified = str(num)

    magnitude = (len(stringified) - 1) // 3
    if max_decimals >= 0:
        try:
            before_length = len(stringified)
            i = (
                max_decimals
                + ((before_length - 1) % 3 + 1)
                + max(0, 3 * (before_length // 3 - len(symbols)))
            )
            if int(stringified[i]) >= 5:
                stringified = str(int(stringified[:i]) + 1) + stringified[i:]
                if len(stringified) > before_length and len(stringified) % 3 == 1:
                    magnitude += 1
        except (ValueError, IndexError):
            pass
    magnitude = min(magnitude, len(symbols))

    whole, decimals = stringified[:-3 * magnitude], stringified[-3 * magnitude:]
    decimals = decimals[:max_decimals] if max_decimals >= 0 else decimals
    rounded = (decimal_point + decimals).rstrip('0').removesuffix('.')
    symbol = symbols[magnitude - 1]
    return prefix + whole + rounded + symbol


"""
>>> from human_format import human_format
>>> human_format(1_000)
'1K'
>>> human_format(1_000_000)
'1M'
>>> human_format(123_123)
'123.123K'
>>> human_format(123_123, max_decimals=1)
'123.1K'
>>> human_format(123_123, max_decimals=100)
'123.123K'
>>> human_format(9_009, max_decimals=2)
'9.01K'
>>> human_format(500_000, maybe_plus=True)
'+500K'
>>> human_format(-500_000, maybe_plus=True)
'-500K'
>>> human_format(1_000_000_000_001, max_decimals=-1, decimal_point=',')
'1,000000000001T'
"""
