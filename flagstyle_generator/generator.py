from parse import (
    Parser,
    Token,
    Variable,
    Negation,
    Conjunction,
    Disjunction,
    Implication,
    BiImplication,
)
from checker import Checker, PropositionType

from enum import Enum

from typing import Optional, Self


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
    maybe_symbol: Optional[str]
    def __init__(
        self,
        *,
        reason: LineReason,
        token: Token,
        maybe_symbol: Optional[str] = None,
    ) -> None:
        self.reason = reason
        self.token = token
        self.maybe_symbol = maybe_symbol


class Flag:
    top: list['Line | Flag']
    bottom: list['Line | Flag']
    parent: Optional['Flag']
    combined: Optional[list['Line | Flag']]
    def __init__(
        self,
        *,
        parent: Optional['Flag'],
        top: Optional[list['Line | Flag']] = None,
        bottom: Optional[list['Line | Flag']] = None,
    ) -> None:
        self.top = top or []
        self.bottom = bottom or []
        self.parent = parent
        self.combined = None

    def combine_top_and_bottom(self) -> None:
        self.combined = self.top + list(reversed(self.bottom))

    @property
    def complete(self) -> bool:
        return self.combined is not None


class Generator:
    parser: Parser
    checker: Checker
    flag: Optional[Flag]
    def __init__(
        self,
        parser: Parser,
    ) -> None:
        self.parser = parser
        self.checker = Checker.from_parser(parser)
        self.flag = None

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

        top_assumptions: list[Token] = []
        token: Token = self.parser.proposition
        flag: Flag = Flag(parent=None, bottom=[Line(reason=LineReason.unknown, token=token)])
        while True:
            if isinstance(token, Implication):
                left, right = token.content
                new_flag: Flag = Flag(
                    parent=flag,
                    top=[Line(
                        reason=LineReason.assumption,
                        token=left,
                    )],
                )
                flag.top.append(new_flag)
                bottom_line = flag.bottom[-1]
                assert isinstance(bottom_line, Line)
                bottom_line.reason = LineReason.intro
                bottom_line.maybe_symbol = Implication.get_main_symbol()
                continue
