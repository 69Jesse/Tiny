from parse import Parser, Token
from checker import Checker, PropositionType

from enum import Enum

from typing import Self


def format_line_numbers(lines: list[int]) -> str:
    if len(lines) == 0:
        return '...'
    if len(lines) == 1:
        return f'({lines[0]})'
    return f'{', '.join(f'({line})' for line in lines[:-1])} and ({lines[-1]})'


class LineReason(Enum):
    unknown = '...'
    assumption = 'Assume'
    intro = '{symbol}-intro on {lines}'
    elim = '{symbol}-elim on {lines}'


class Line:
    reason: LineReason
    token: Token
    def __init__(
        self,
        *,
        reason: LineReason,
        token: Token,
    ) -> None:
        self.reason = reason
        self.token = token


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
        if self.checker.proposition_type is PropositionType.not_sure:
            self.checker.brute_force()
        if not display:
            return
        print(self.checker.get_result_string())

    def prove(self) -> None:
        self.check(display=False)
        if self.checker.proposition_type is not PropositionType.tautology:
            raise ValueError(self.checker.get_result_string())
        ...
