from abc import ABC, abstractmethod

from typing import Generator, TypeAlias, Optional


# neg -> and / or -> imp -> bi imp


class Token(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_main_symbol(self) -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_symbols() -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def get_value(self) -> bool:
        raise NotImplementedError


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
            yield self.content  # type: ignore
            return
        yield from self.content


class Variable(Token):
    name: str
    value: bool
    def __init__(
        self,
        name: str,
        value: bool,
    ) -> None:
        super().__init__()
        self.name = name
        self.value = value

    def get_main_symbol(self) -> str:
        return self.name

    @staticmethod
    def get_symbols() -> list[str]:
        raise NotImplementedError

    def get_value(self) -> bool:
        return self.value


class Negation(TokenWithContent[Token]):
    def get_main_symbol(self) -> str:
        return '~'

    @staticmethod
    def get_symbols() -> list[str]:
        return ['~']

    def get_value(self) -> bool:
        return not self.content.get_value()


class Conjuction(TokenWithContent[tuple[Token, Token]]):
    def get_main_symbol(self) -> str:
        return '&'

    @staticmethod
    def get_symbols() -> list[str]:
        return ['&']

    def get_value(self) -> bool:
        return self.content[0].get_value() and self.content[1].get_value()


class Disjunction(TokenWithContent[tuple[Token, Token]]):
    def get_main_symbol(self) -> str:
        return '|'

    @staticmethod
    def get_symbols() -> list[str]:
        return ['|']

    def get_value(self) -> bool:
        return self.content[0].get_value() or self.content[1].get_value()


class Implication(TokenWithContent[tuple[Token, Token]]):
    def get_main_symbol(self) -> str:
        return '=>'

    @staticmethod
    def get_symbols() -> list[str]:
        return ['=>']

    def get_value(self) -> bool:
        return not self.content[0].get_value() or self.content[1].get_value()


class BiImplication(TokenWithContent[tuple[Token, Token]]):
    def get_main_symbol(self) -> str:
        return '<=>'

    @staticmethod
    def get_symbols() -> list[str]:
        return ['<=>']

    def get_value(self) -> bool:
        return self.content[0].get_value() is self.content[1].get_value()


TOKEN_TYPES_WITH_SYMBOLS: list[type[Token]] = [
    Negation,
    Conjuction,
    Disjunction,
    Implication,
    BiImplication,
]
SYMBOLS_TO_TOKEN_TYPE: dict[str, type[Token]] = {
    symbol: cls for symbol, cls in sorted(
        ((symbol, cls)
        for cls in TOKEN_TYPES_WITH_SYMBOLS
        for symbol in cls.get_symbols()),
        key=lambda x: len(x[0]),
        reverse=True,
    )
}


TokenWithContentPairType: TypeAlias = type[Conjuction] | type[Disjunction] | type[Implication] | type[BiImplication]


class Parser:
    token: Token
    def __init__(
        self,
        token: Token,
    ) -> None:
        self.token = token

    @staticmethod
    def generate_token(
        proposition: str,
    ) -> Token:
        print(proposition)
        before_token: Optional[Token] = None
        in_between_type: Optional[TokenWithContentPairType] = None
        for index in range(len(proposition)):
            if proposition[index] == '(':
                depth = 1
                for i in range(index + 1, len(proposition)):
                    if proposition[i] == '(':
                        depth += 1
                    if proposition[i] != ')':
                        continue
                    depth -= 1
                    if depth != 0:
                        continue
                    if i == len(proposition) - 1:
                        if index == 0:
                            return Parser.generate_token(proposition[1:-1])
                        assert before_token is not None
                        assert in_between_type is not None
                        return in_between_type((
                            before_token,
                            Parser.generate_token(proposition[index + 1:i]),
                        ))
                    before_token = Parser.generate_token(proposition[index + 1:i])
                    for symbol, cls in SYMBOLS_TO_TOKEN_TYPE.items():
                        if not proposition[i + 1:].startswith(symbol):
                            continue
                        in_between_type = cls  # type: ignore
                        break
                    break
                else:
                    raise ValueError('Expected closing parenthesis')
        print(before_token, 'b')
        return proposition


    @classmethod
    def from_token(
        cls,
        token: Token,
    ) -> 'Parser':
        return cls(token)

    @classmethod
    def from_proposition(
        cls,
        proposition: str,
    ) -> 'Parser':
        proposition = proposition.replace(' ', '').replace('\n', '')
        token = cls.generate_token(proposition)
        return cls.from_token(token)


parser = Parser.from_proposition('((aap => waarheid) => hoiii)')
