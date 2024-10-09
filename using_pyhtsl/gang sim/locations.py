from pyhtsl import (
    IfAnd,
    PlayerLocationX,
    PlayerLocationY,
    PlayerLocationZ,
)
from pyhtsl.types import IfStatement
import colorsys
import random

from constants import LOCATION_ID

from typing import Callable, Generator


class Location:
    low: tuple[int, int, int]
    high: tuple[int, int, int]
    name: str
    id: int
    big_id: int
    biggest_id: int
    contains: list['Location']

    def __init__(
        self,
        point1: tuple[int, int, int],
        point2: tuple[int, int, int],
        name: str,
        id: int,
    ) -> None:
        self.low = (
            min(point1[0], point2[0]),
            min(point1[1], point2[1]),
            min(point1[2], point2[2]),
        )
        self.high = (
            max(point1[0], point2[0]),
            max(point1[1], point2[1]),
            max(point1[2], point2[2]),
        )
        self.name = name
        self.id = id
        self.big_id = id // 100
        self.biggest_id = self.big_id // 100
        self.contains = []

    @staticmethod
    def sort_key() -> Callable[['Location'], tuple[int, int, int, int, int, int]]:
        return lambda loc: (
            loc.low[0], loc.low[1], loc.low[2],
            -loc.high[0], -loc.high[1], -loc.high[2],
        )

    def walk(self) -> Generator['Location', None, None]:
        for location in sorted(self.contains, key=Location.sort_key()):
            yield from location.walk()
        yield self

    def full_contains(self, location: 'Location') -> bool:
        return all(
            self.low[i] <= location.low[i] <= self.high[i]
            for i in range(3)
        ) and all(
            self.low[i] <= location.high[i] <= self.high[i]
            for i in range(3)
        )

    def half_contains(self, location: 'Location') -> bool:
        return all(
            self.low[i] <= location.low[i] <= self.high[i]
            for i in range(3)
        ) or all(
            self.low[i] <= location.high[i] <= self.high[i]
            for i in range(3)
        )

    def if_inside_condition(self) -> 'IfStatement':
        return IfAnd(
            LOCATION_ID == 0,
            PlayerLocationX >= self.low[0],
            PlayerLocationX <= self.high[0],
            PlayerLocationY >= self.low[1],
            PlayerLocationY <= self.high[1],
            PlayerLocationZ >= self.low[2],
            PlayerLocationZ <= self.high[2],
        )

    def __repr__(self) -> str:
        return f'Location({self.low}, {self.high}, {self.name}, {len(self.contains)})'


class LocationInstances:
    __slots__ = ()
    spawn = Location(
        (-51, 1, -91),
        (49, 80, 9),
        'Spawn',
        10000,
    )
    spawn_bloods_area = Location(
        (-10, 42, -48),
        (-20, 50, -58),
        'Bloods Spawn Area',
        10100,
    )
    spawn_crips_area = Location(
        (8, 42, -48),
        (18, 50, -58),
        'Crips Spawn Area',
        10200,
    )
    spawn_kings_area = Location(
        (11, 42, -38),
        (21, 50, -28),
        'Kings Spawn Area',
        10300,
    )
    spawn_grapes_area = Location(
        (-13, 42, -38),
        (-23, 50, -28),
        'Grapes Spawn Area',
        10400,
    )
    spawn_afk_area = Location(
        (3, 56, -9),
        (-5, 40, -13),
        'AFK Drop Area',
        10500,
    )

    # cell_block = Location(
    #     (-22, 115, -28),
    #     (18, 102, -54),
    #     'Cell Block',
    #     20000,
    # )
    # cell_block_cell_1 = Location(
    #     (15, 103, -34),
    #     (11, 107, -29),
    #     'Cell 1',
    #     20001,
    # )
    # cell_block_cell_2 = Location(
    #     (8, 103, -34),
    #     (4, 107, -29),
    #     'Cell 2',
    #     20002,
    # )
    # cell_block_cell_3 = Location(
    #     (1, 103, -34),
    #     (-3, 107, -29),
    #     'Cell 3',
    #     20003,
    # )
    # cell_block_cell_4 = Location(
    #     (-6, 103, -34),
    #     (-10, 107, -29),
    #     'Cell 4',
    #     20004,
    # )
    # cell_block_cell_5 = Location(
    #     (-13, 103, -34),
    #     (-17, 107, -29),
    #     'Cell 5',
    #     20005,
    # )
    # cell_block_cell_6 = Location(
    #     (-17, 103, -48),
    #     (-13, 107, -53),
    #     'Cell 6',
    #     20006,
    # )
    # cell_block_cell_7 = Location(
    #     (-10, 103, -48),
    #     (-6, 107, -53),
    #     'Cell 7',
    #     20007,
    # )
    # cell_block_cell_8 = Location(
    #     (-3, 103, -48),
    #     (1, 107, -53),
    #     'Cell 8',
    #     20008,
    # )
    # cell_block_cell_9 = Location(
    #     (4, 103, -48),
    #     (8, 107, -53),
    #     'Cell 9',
    #     20009,
    # )
    # cell_block_cell_10 = Location(
    #     (11, 103, -48),
    #     (15, 107, -53),
    #     'Cell 10',
    #     20010,
    # )
    # cell_block_cell_11 = Location(
    #     (15, 110, -34),
    #     (11, 114, -29),
    #     'Cell 11',
    #     20011,
    # )
    # cell_block_cell_12 = Location(
    #     (8, 110, -34),
    #     (4, 114, -29),
    #     'Cell 12',
    #     20012,
    # )
    # cell_block_cell_13 = Location(
    #     (1, 110, -34),
    #     (-3, 114, -29),
    #     'Cell 13',
    #     20013,
    # )
    # cell_block_cell_14 = Location(
    #     (-6, 110, -34),
    #     (-10, 114, -29),
    #     'Cell 14',
    #     20014,
    # )
    # cell_block_cell_15 = Location(
    #     (-13, 110, -34),
    #     (-17, 114, -29),
    #     'Cell 15',
    #     20015,
    # )
    # cell_block_cell_16 = Location(
    #     (-17, 110, -48),
    #     (-13, 114, -53),
    #     'Cell 16',
    #     20016,
    # )
    # cell_block_cell_17 = Location(
    #     (-10, 110, -48),
    #     (-6, 114, -53),
    #     'Cell 17',
    #     20017,
    # )
    # cell_block_cell_18 = Location(
    #     (-3, 110, -48),
    #     (1, 114, -53),
    #     'Cell 18',
    #     20018,
    # )
    # cell_block_cell_19 = Location(
    #     (4, 110, -48),
    #     (8, 114, -53),
    #     'Cell 19',
    #     20019,
    # )
    # cell_block_cell_20 = Location(
    #     (11, 110, -48),
    #     (15, 114, -53),
    #     'Cell 20',
    #     20020,
    # )
    # cell_block_roof = Location(
    #     (-24, 116, -26),
    #     (21, 128, -56),
    #     'Cell Block Roof',
    #     20100,
    # )

    # # https://www.youtube.com/watch?v=yj18bIGL_CQ walks through a lot of rooms
    # corridors = Location(
    #     (19, 114, -28),
    #     (57, 102, -61),
    #     'Corridors',
    #     30000,
    # )

    # basement_corridor = Location(
    #     (45, 101, -24),
    #     (21, 92, -79),
    #     'Basement Corridor',
    #     -1,
    # )
    # the_deep = Location(
    #     (19, 91, -65),
    #     (-22, 100, -27),
    #     'The Deep',
    #     -2,
    # )

    @classmethod
    def get_all_locations(cls) -> Generator[Location, None, None]:
        for location in cls.__dict__.values():
            if isinstance(location, Location):
                yield location


class Locations:
    locations: list[Location]
    def __init__(self) -> None:
        locations = sorted(LocationInstances.get_all_locations(), key=Location.sort_key())
        self.locations = []
        for location in locations:
            for seen in self.locations:
                for loc in seen.walk():
                    if loc.full_contains(location):
                        loc.contains.append(location)
                        break
                else:
                    continue
                break
            else:
                self.locations.append(location)

        all_locations = list(self.walk())

        # checking if you didnt fuck up
        for location in all_locations:
            for loc in all_locations:
                if location is loc:
                    continue
                if location.low == loc.low and location.high == loc.high:
                    raise ValueError(f'{location} and {loc} are the same')
                if location.half_contains(loc) and not (location.full_contains(loc) or loc.full_contains(location)):
                    raise ValueError(f'{location} half contains {loc}')

        # checking if I didnt fuck up
        for location in all_locations:
            for loc in all_locations:
                if location is loc:
                    continue
                if location.full_contains(loc):
                    assert any(walk is loc for walk in location.walk())

        self.locations.sort(key=Location.sort_key())

    def walk(self) -> Generator[Location, None, None]:
        for location in self.locations:
            yield from location.walk()


LOCATIONS = Locations()


def random_neon_color_prefix() -> str:
    r, g, b = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(random.random(), 0.7, 1.0))
    return f'\033[38;2;{r};{g};{b}m'


def display_locations_blocking() -> None:
    low: tuple[int, int, int] = (
        min(LOCATIONS.walk(), key=lambda p: p.low[0]).low[0],
        min(LOCATIONS.walk(), key=lambda p: p.low[1]).low[1],
        min(LOCATIONS.walk(), key=lambda p: p.low[2]).low[2],
    )
    high: tuple[int, int, int] = (
        max(LOCATIONS.walk(), key=lambda p: p.high[0]).high[0],
        max(LOCATIONS.walk(), key=lambda p: p.high[1]).high[1],
        max(LOCATIONS.walk(), key=lambda p: p.high[2]).high[2],
    )
    y_level_has_location: set[int] = set()
    mapping: dict[tuple[int, int, int], str] = {}
    for location in LOCATIONS.walk():
        value = random_neon_color_prefix() + f'{location.id:05d}' + '\033[0m'
        for x in range(location.low[0], location.high[0] + 1):
            for y in range(location.low[1], location.high[1] + 1):
                for z in range(location.low[2], location.high[2] + 1):
                    key = (x, y, z)
                    if key in mapping:
                        continue
                    mapping[key] = value
                    y_level_has_location.add(y)

    y = low[1]
    action = ''

    while True:
        layer: list[list[str]] = [
            [
                mapping.get((x, y, z), '.' * 5)
                for z in range(low[2], high[2] + 1)
            ]
            for x in range(low[0], high[0] + 1)
        ]
        corners: list[str] = [
            f'({x}, {y}, {z})'
            for x, z in (
                (low[0], low[2]),
                (high[0], low[2]),
                (low[0], high[2]),
                (high[0], high[2]),
            )
        ]
        lines: list[str] = []
        for x in range(low[0], high[0] + 1):
            if x == low[0]:
                prefix, suffix = corners[0], corners[1]
            elif x == high[0]:
                prefix, suffix = corners[2], corners[3]
            else:
                prefix, suffix = '', ''
            prefix, suffix = ' ' * (max(len(corners[0]), len(corners[1])) - len(prefix)) + prefix, suffix + ' ' * (max(len(corners[2]), len(corners[3])) - len(suffix))
            lines.append(f'{prefix} {' '.join(layer[x - low[0]])} {suffix}')

        print('\n' + '\n'.join(lines))

        try:
            action = input('\n(u)p, (d)own: ')[0]
        except IndexError:
            pass
        if action == 'u':
            y = min(high[1], y + 1)
            while y not in y_level_has_location:
                y = min(high[1], y + 1)
        elif action == 'd':
            y = max(low[1], y - 1)
            while y not in y_level_has_location:
                y = max(low[1], y - 1)


if __name__ == '__main__':
    display_locations_blocking()
