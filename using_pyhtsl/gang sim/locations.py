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
    medium = Location(
        (0, 0, 0),
        (20, 20, 20),
        'Medium',
        1,
    )
    big = Location(
        (0, 0, 0),
        (30, 30, 30),
        'Big',
        2,
    )
    small = Location(
        (0, 0, 0),
        (10, 10, 10),
        'Small',
        3,
    )
    bigger = Location(
        (-5, -5, -5),
        (35, 35, 35),
        'Bigger',
        4,
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


@create_function('Set Location ID')
def set_location_id() -> None:
    LOCATION_ID.value = 0
    for location in LOCATIONS.walk():
        with location.if_inside_condition():
            LOCATION_ID.value = location.id
            exit_function()
