from pyhtsl import (
    IfAnd,
    PlayerLocationX,
    PlayerLocationY,
    PlayerLocationZ,
    create_function,
    exit_function,
)
from pyhtsl.types import IfStatement

from stats.playerstats import LOCATION_ID

from typing import Callable, Generator


class Location:
    low: tuple[int, int, int]
    high: tuple[int, int, int]
    name: str
    id: int
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
            *(
                PlayerLocationX >= self.low[0],
                PlayerLocationX <= self.high[0],
                PlayerLocationY >= self.low[1],
                PlayerLocationY <= self.high[1],
                PlayerLocationZ >= self.low[2],
                PlayerLocationZ <= self.high[2],
            ),
        )

    def __repr__(self) -> str:
        return f'Location({self.low}, {self.high}, {self.name}, {len(self.contains)})'


class LocationInstances:
    __slots__ = ()
    cell_block = Location(
        (-22, 115, -28),
        (18, 102, -54),
        'Cell Block',
        1000,
    )
    cell_block_cell_1 = Location(
        (15, 103, -34),
        (11, 107, -29),
        'Cell 1',
        1001,
    )
    cell_block_cell_2 = Location(
        (8, 103, -34),
        (4, 107, -29),
        'Cell 2',
        1002,
    )
    cell_block_cell_3 = Location(
        (1, 103, -34),
        (-3, 107, -29),
        'Cell 3',
        1003,
    )
    cell_block_cell_4 = Location(
        (-6, 103, -34),
        (-10, 107, -29),
        'Cell 4',
        1004,
    )
    cell_block_cell_5 = Location(
        (-13, 103, -34),
        (-17, 107, -29),
        'Cell 5',
        1005,
    )
    cell_block_cell_6 = Location(
        (-17, 103, -48),
        (-13, 107, -53),
        'Cell 6',
        1006,
    )
    cell_block_cell_7 = Location(
        (-10, 103, -48),
        (-6, 107, -53),
        'Cell 7',
        1007,
    )
    cell_block_cell_8 = Location(
        (-3, 103, -48),
        (1, 107, -53),
        'Cell 8',
        1008,
    )
    cell_block_cell_9 = Location(
        (4, 103, -48),
        (8, 107, -53),
        'Cell 9',
        1009,
    )
    cell_block_cell_10 = Location(
        (11, 103, -48),
        (15, 107, -53),
        'Cell 10',
        1010,
    )
    cell_block_cell_11 = Location(
        (15, 110, -34),
        (11, 114, -29),
        'Cell 11',
        1011,
    )
    cell_block_cell_12 = Location(
        (8, 110, -34),
        (4, 114, -29),
        'Cell 12',
        1012,
    )
    cell_block_cell_13 = Location(
        (1, 110, -34),
        (-3, 114, -29),
        'Cell 13',
        1013,
    )
    cell_block_cell_14 = Location(
        (-6, 110, -34),
        (-10, 114, -29),
        'Cell 14',
        1014,
    )
    cell_block_cell_15 = Location(
        (-13, 110, -34),
        (-17, 114, -29),
        'Cell 15',
        1015,
    )
    cell_block_cell_16 = Location(
        (-17, 110, -48),
        (-13, 114, -53),
        'Cell 16',
        1016,
    )
    cell_block_cell_17 = Location(
        (-10, 110, -48),
        (-6, 114, -53),
        'Cell 17',
        1017,
    )
    cell_block_cell_18 = Location(
        (-3, 110, -48),
        (1, 114, -53),
        'Cell 18',
        1018,
    )
    cell_block_cell_19 = Location(
        (4, 110, -48),
        (8, 114, -53),
        'Cell 19',
        1019,
    )
    cell_block_cell_20 = Location(
        (11, 110, -48),
        (15, 114, -53),
        'Cell 20',
        1020,
    )
    cell_block_roof = Location(
        (-24, 116, -26),
        (21, 128, -56),
        'Cell Block Roof',
        1100,
    )

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

    def walk(self) -> Generator[Location, None, None]:
        for location in sorted(self.locations, key=Location.sort_key()):
            yield from location.walk()


LOCATIONS = Locations()
from pyhtsl import display_action_bar

@create_function('Set Location ID')
def set_location_id() -> None:
    LOCATION_ID.value = 0
    for location in LOCATIONS.walk():
        with location.if_inside_condition():
            LOCATION_ID.value = location.id
            display_action_bar(f'&b{location.name} ({location.id})')
            exit_function()
