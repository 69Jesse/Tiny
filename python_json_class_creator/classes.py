from typing import (
    Any,
)


class Interests:
    def __init__(
        self,
        *,
        name: str,
        extra: str,
    ) -> None:
        self.name: str = name
        self.extra: str = extra


class Belongings:
    def __init__(
        self,
        *,
        name: str,
        value: float,
    ) -> None:
        self.name: str = name
        self.value: float = value


class Person:
    def __init__(
        self,
        *,
        name: str,
        age: int,
        height: float,
        weight: float,
        belongings: list[dict[str, Any]],
        isAdult: bool,
        interests: list[dict[str, Any]] | None = None,
        friends: list[str] | None = None,
    ) -> None:
        self.name: str = name
        self.age: int = age
        self.height: float = height
        self.weight: float = weight
        self.belongings: list[Belongings] = [Belongings(**item) for item in belongings]
        self.is_adult: bool = isAdult
        self.interests: list[Interests] | None = [Interests(**item) for item in interests] if interests is not None else None
        self.friends: list[str] | None = friends
