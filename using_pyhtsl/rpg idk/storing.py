from pyhtsl import PlayerStat

from everything import fetch_digits


a = PlayerStat('a')
b = PlayerStat('b')
# fetch_digits(a, b, 'xxx...')  # example: a = 123456789, b = 456
fetch_digits(a, b, 'x.')  # example: a = 123456789, b = 8
