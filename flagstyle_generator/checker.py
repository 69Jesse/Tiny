from parse import (
    Parser, 
    Variable,
)

from enum import Enum

from typing import Self


class PropositionType(Enum):
    not_sure = 0
    tautology = 1
    contradiction = 2
    contingency = 3


class Checker:
    parser: Parser
    proposition_type: PropositionType
    does_hold_for: list[dict[Variable, bool]]
    does_not_hold_for: list[dict[Variable, bool]]
    def __init__(
        self,
        parser: Parser,
    ) -> None:
        self.parser = parser
        self.proposition_type = PropositionType.not_sure
        self.does_hold_for = []
        self.does_not_hold_for = []

    @classmethod
    def from_parser(cls, parser: Parser) -> Self:
        return cls(parser)

    def brute_force(self) -> None:
        self.does_hold_for = []
        self.does_not_hold_for = []
        for n in range(2 ** len(self.parser.variables)):
            for i, variable in enumerate(self.parser.variables.values()):
                variable.value = bool(n & (1 << i))
            holds: bool = self.parser.proposition.get_value()
            if holds:
                self.does_hold_for.append({variable: variable.value for variable in self.parser.variables.values()})
            else:
                self.does_not_hold_for.append({variable: variable.value for variable in self.parser.variables.values()})
        if len(self.does_not_hold_for) == 0:
            self.proposition_type = PropositionType.tautology
        elif len(self.does_hold_for) == 0:
            self.proposition_type = PropositionType.contradiction
        else:
            self.proposition_type = PropositionType.contingency

    def get_result_string(self) -> str:
        if self.proposition_type is PropositionType.tautology:
            return 'Proposition is a tautology.'
        if self.proposition_type is PropositionType.contradiction:
            return 'Proposition is a contradiction.'
        return 'Proposition is a contingency. It does not hold for:\n' + '\n'.join(
            f'    {', '.join(f'{variable.name}={int(value)}' for variable, value in variables.items())}'
            for variables in self.does_not_hold_for
        )
