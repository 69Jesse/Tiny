from parse import Parser
from checker import Checker

from typing import Self



class Generator:
    parser: Parser
    checker: Checker
    def __init__(
        self,
        parser: Parser,
    ) -> None:
        self.parser = parser
        self.checker = Checker.from_parser(parser)

    @classmethod
    def from_parser(cls, parser: Parser) -> Self:
        return cls(parser)

    @classmethod
    def from_proposition(cls, proposition: str) -> Self:
        return cls.from_parser(Parser.from_raw_proposition(proposition))

    def check(
        self,
        *,
        display: bool,
    ) -> None:
        self.checker.brute_force()
        if not display:
            return
        print(self.checker.get_result_string())
