from abc import ABC, abstractmethod

from enum import Enum

from typing import Generator, TypeAlias


class Token(ABC):
    def __init__(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def get_symbols() -> list[str]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_order_value() -> int:
        raise NotImplementedError

    @abstractmethod
    def get_main_symbol(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_value(self) -> bool:
        raise NotImplementedError


class Variable(Token):
    name: str
    value: bool
    def __init__(
        self,
        name: str,
        value: bool = False,
    ) -> None:
        super().__init__()
        self.name = name
        self.value = value

    @staticmethod
    def get_symbols() -> list[str]:
        raise NotImplementedError

    @staticmethod
    def get_order_value() -> int:
        raise NotImplementedError

    def get_main_symbol(self) -> str:
        return self.name

    def get_value(self) -> bool:
        return self.value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}<{self.name}={self.value}>'

    def __str__(self) -> str:
        return self.name


class TokenWithContent[Content: Token | tuple[Token, Token]](Token):
    content: Content
    def __init__(
        self,
        content: Content,
    ) -> None:
        super().__init__()
        self.content = content

    def get_tokens_with_value(self) -> Generator[Token, None, None]:
        if isinstance(self.content, Token):
            yield self.content
            return
        yield from self.content

    def __repr__(self) -> str:
        if isinstance(self.content, Token):
            return f'{self.__class__.__name__}<{self.get_main_symbol()}{repr(self.content)}>'
        return f'{self.__class__.__name__}<{repr(self.content[0])} {self.get_main_symbol()} {repr(self.content[1])}'

    def maybe_wrap(self, token: Token) -> str:
        if isinstance(token, TokenWithContent) and not isinstance(token, Negation):
            return f'({token})'
        return str(token)

    def __str__(self) -> str:
        if isinstance(self.content, Token):
            return f'{self.get_main_symbol()}{self.maybe_wrap(self.content)}'  # type: ignore
        return f'{self.maybe_wrap(self.content[0])} {self.get_main_symbol()} {self.maybe_wrap(self.content[1])}'


class Negation(TokenWithContent[Token]):
    @staticmethod
    def get_symbols() -> list[str]:
        return ['~', '¬']

    @staticmethod
    def get_order_value() -> int:
        return 0

    def get_main_symbol(self) -> str:
        return '¬'

    def get_value(self) -> bool:
        return not self.content.get_value()


class Conjuction(TokenWithContent[tuple[Token, Token]]):
    @staticmethod
    def get_symbols() -> list[str]:
        return ['&', '∧']

    @staticmethod
    def get_order_value() -> int:
        return 1

    def get_main_symbol(self) -> str:
        return '∧'

    def get_value(self) -> bool:
        return self.content[0].get_value() and self.content[1].get_value()


class Disjunction(TokenWithContent[tuple[Token, Token]]):
    @staticmethod
    def get_symbols() -> list[str]:
        return ['|', '∨']

    @staticmethod
    def get_order_value() -> int:
        return 1

    def get_main_symbol(self) -> str:
        return '∨'

    def get_value(self) -> bool:
        return self.content[0].get_value() or self.content[1].get_value()


class Implication(TokenWithContent[tuple[Token, Token]]):
    @staticmethod
    def get_symbols() -> list[str]:
        return ['=>', '->', '⇒']

    @staticmethod
    def get_order_value() -> int:
        return 2

    def get_main_symbol(self) -> str:
        return '⇒'

    def get_value(self) -> bool:
        return not self.content[0].get_value() or self.content[1].get_value()


class BiImplication(TokenWithContent[tuple[Token, Token]]):
    @staticmethod
    def get_symbols() -> list[str]:
        return ['<=>', '<->', '⇔']

    @staticmethod
    def get_order_value() -> int:
        return 3

    def get_main_symbol(self) -> str:
        return '⇔'

    def get_value(self) -> bool:
        return self.content[0].get_value() is self.content[1].get_value()


ORDERED_NON_VAR_TOKEN_CLASSES: list[type[Token]] = sorted((
    Negation,
    Conjuction,
    Disjunction,
    Implication,
    BiImplication,
), key=lambda cls: cls.get_order_value())

NON_VAR_TOKEN_TYPES_CONTENT_OFFSETS: dict[type[Token], tuple[int] | tuple[int, int]] = {
    Negation: (1,),
    Conjuction: (-1, 1),
    Disjunction: (-1, 1),
    Implication: (-1, 1),
    BiImplication: (-1, 1),
}

TOKEN_CLASS_TO_SYMBOLS: dict[type[Token], list[str]] = {
    cls: sorted(cls.get_symbols(), key=len, reverse=True)
    for cls in ORDERED_NON_VAR_TOKEN_CLASSES
}

SYMBOL_TO_TOKEN_CLASS: dict[str, type[Token]] = {
    symbol: cls
    for cls, symbols in TOKEN_CLASS_TO_SYMBOLS.items()
    for symbol in symbols
}

ALL_TOKEN_SYMBOLS: list[str] = sorted((
    symbol
    for symbols in TOKEN_CLASS_TO_SYMBOLS.values()
    for symbol in symbols
), key=len, reverse=True)

ALLOWED_VARIABLE_NAME_CHARACTERS: set[str] = set(
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
)


TokenWithContentPairType: TypeAlias = type[Conjuction] | type[Disjunction] | type[Implication] | type[BiImplication]


class PropositionType(Enum):
    not_sure = 0
    tautology = 1
    contradiction = 2
    contingency = 3


class Parser:
    proposition: Token
    variables: dict[str, Variable]
    proposition_type: PropositionType
    does_hold_for: list[dict[Variable, bool]]
    does_not_hold_for: list[dict[Variable, bool]]
    def __init__(
        self,
        *,
        proposition: Token,
        variables: dict[str, Variable],
    ) -> None:
        self.proposition = proposition
        self.variables = variables
        self.proposition_type = PropositionType.not_sure
        self.does_hold_for = []
        self.does_not_hold_for = []

    @staticmethod
    def maybe_add_variable(
        *,
        variables: dict[str, Variable],
        parts: list[type[Token] | Token],
        name: str,
    ) -> None:
        if len(name) == 0:
            return
        variable: Variable = variables.get(name, None) or Variable(name)
        variables[name] = variable
        parts.append(variable)

    @staticmethod
    def _generate_token(
        proposition: str,
        /,
        *,
        variables: dict[str, Variable],
    ) -> Token:
        parts: list[type[Token] | Token] = []
        index = 0
        while index < len(proposition):
            if proposition[index] == '(':
                depth: int = 1
                for i in range(index + 1, len(proposition)):
                    c = proposition[i]
                    if c == '(':
                        depth += 1
                        continue
                    elif c != ')':
                        continue
                    depth -= 1
                    if depth != 0:
                        continue
                    parts.append(
                        Parser._generate_token(
                            proposition[index + 1:i],
                            variables=variables,
                        )
                    )
                    index = i + 1
                    break
                else:
                    raise ValueError('Missing closing parenthesis')
                continue

            rest: str = proposition[index:]
            variable_name: str = ''
            for i in range(len(rest)):
                for symbol in ALL_TOKEN_SYMBOLS:
                    if rest[i:len(symbol) + i] == symbol:
                        Parser.maybe_add_variable(
                            variables=variables,
                            parts=parts,
                            name=variable_name,
                        )
                        parts.append(SYMBOL_TO_TOKEN_CLASS[symbol])
                        index += len(symbol) + len(variable_name)
                        break
                else:
                    c = rest[i]
                    if c not in ALLOWED_VARIABLE_NAME_CHARACTERS:
                        raise ValueError(f'Invalid character {c}')
                    variable_name += c
                    continue
                break
            else:
                Parser.maybe_add_variable(
                    variables=variables,
                    parts=parts,
                    name=variable_name,
                )
                index += len(variable_name)

        for token_cls in ORDERED_NON_VAR_TOKEN_CLASSES:
            index: int = 0
            while index < len(parts):
                part = parts[index]
                if isinstance(part, Token):
                    index += 1
                    continue
                if part is not token_cls:
                    index += 1
                    continue
                offsets: tuple[int] | tuple[int, int] = NON_VAR_TOKEN_TYPES_CONTENT_OFFSETS[token_cls]
                if len(offsets) == 1:
                    content = parts.pop(index + offsets[0])
                    if not isinstance(content, Token):
                        raise ValueError('Invalid proposition')
                else:
                    content = (parts.pop(index + offsets[0]), parts.pop(index + offsets[1] - 1))
                    if not all(isinstance(part, Token) for part in content):
                        raise ValueError('Invalid proposition')
                    index -= 1
                parts[index] = token_cls(content)  # type: ignore
        if len(parts) != 1:
            raise ValueError('Invalid proposition')

        return parts[0]  # type: ignore

    @classmethod
    def from_raw_proposition(
        cls,
        raw_proposition: str,
    ) -> 'Parser':
        raw_proposition = raw_proposition.replace(' ', '').replace('\n', '')
        variables: dict[str, Variable] = {}
        proposition = cls._generate_token(raw_proposition, variables=variables)
        return cls(proposition=proposition, variables=variables)

    def brute_force(self) -> None:
        self.does_hold_for = []
        self.does_not_hold_for = []
        for n in range(2 ** len(self.variables)):
            for i, variable in enumerate(self.variables.values()):
                variable.value = bool(n & (1 << i))
            holds: bool = self.proposition.get_value()
            if holds:
                self.does_hold_for.append({variable: variable.value for variable in self.variables.values()})
            else:
                self.does_not_hold_for.append({variable: variable.value for variable in self.variables.values()})
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


for raw_proposition in (
    # '(P ⇒ (Q ∧ R)) ⇒ ((P ⇒ Q) ∧ (Q ⇒ (P ⇒ R)))',
    # 'a|b|c|d|e|f|g',
    # 'a=>b=>c',
    # 'a=>b=>c=>d',
    '''

(a|b|(c&d)) &  ((a&b)|c|d)

''',
    '''


    (a | (
        (b | (
            (c | (
                d & ~d
            )) & (~c | d)
        )) & (~b | c | d)
    )) & (~a | b | c | d)


''',
    '''


    (a | (
        (b | (
            c & (~c | d)
        )) & (~b | c | d)
    )) & (~a | b | c | d)


''',
'''


    (a | (
        (b | (
            c & d
        )) & (~b | c | d)
    )) & (~a | b | c | d)


''',
):
    parser = Parser.from_raw_proposition(raw_proposition)
    parser.brute_force()
    print(parser.proposition)
    print(parser.get_result_string())
