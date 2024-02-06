from abc import ABC, abstractmethod

from typing import Generator, TypeAlias, Optional


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


class Negation(TokenWithContent[Token]):
    @staticmethod
    def get_symbols() -> list[str]:
        return ['~']

    @staticmethod
    def get_order_value() -> int:
        return 0

    def get_main_symbol(self) -> str:
        return '~'

    def get_value(self) -> bool:
        return not self.content.get_value()


class Conjuction(TokenWithContent[tuple[Token, Token]]):
    @staticmethod
    def get_symbols() -> list[str]:
        return ['&']

    @staticmethod
    def get_order_value() -> int:
        return 1

    def get_main_symbol(self) -> str:
        return '&'

    def get_value(self) -> bool:
        return self.content[0].get_value() and self.content[1].get_value()


class Disjunction(TokenWithContent[tuple[Token, Token]]):
    @staticmethod
    def get_symbols() -> list[str]:
        return ['|']

    @staticmethod
    def get_order_value() -> int:
        return 1

    def get_main_symbol(self) -> str:
        return '|'

    def get_value(self) -> bool:
        return self.content[0].get_value() or self.content[1].get_value()


class Implication(TokenWithContent[tuple[Token, Token]]):
    @staticmethod
    def get_symbols() -> list[str]:
        return ['=>']

    @staticmethod
    def get_order_value() -> int:
        return 2

    def get_main_symbol(self) -> str:
        return '=>'

    def get_value(self) -> bool:
        return not self.content[0].get_value() or self.content[1].get_value()


class BiImplication(TokenWithContent[tuple[Token, Token]]):
    @staticmethod
    def get_symbols() -> list[str]:
        return ['<=>']

    @staticmethod
    def get_order_value() -> int:
        return 3

    def get_main_symbol(self) -> str:
        return '<=>'

    def get_value(self) -> bool:
        return self.content[0].get_value() is self.content[1].get_value()


ORDERED_NON_VAR_TOKEN_TYPES: list[type[Token]] = sorted((
    Negation,
    Conjuction,
    Disjunction,
    Implication,
    BiImplication,
), key=lambda cls: cls.get_order_value())

TOKEN_TYPE_TO_SYMBOL: dict[type[Token], list[str]] = {
    cls: sorted(cls.get_symbols(), key=len, reverse=True)
    for cls in ORDERED_NON_VAR_TOKEN_TYPES
}

SYMBOL_TO_TOKEN_TYPE: dict[str, type[Token]] = {
    symbol: cls
    for cls, symbols in TOKEN_TYPE_TO_SYMBOL.items()
    for symbol in symbols
}

ALL_TOKEN_SYMBOLS: list[str] = sorted((
    symbol
    for symbols in TOKEN_TYPE_TO_SYMBOL.values()
    for symbol in symbols
), key=len, reverse=True)


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
        /,
        *,
        variables: Optional[dict[str, Variable]] = None,
    ) -> Token:
        print(proposition)
        parts: list[str | type[Token] | Token] = []
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
                        Parser.generate_token(
                            proposition[index + 1:i],
                            variables=variables,
                        )
                    )
                    index = i + 1
                    break
                else:
                    raise ValueError('Missing closing parenthesis')
                continue

            rest = proposition[index:]
            
            # ga alle symbolen af als niet in zit is variabele, check totdat er symbool is (of '(') en dan variabele toevoegen en symbool toevoegen

            # for symbol in ALL_TOKEN_SYMBOLS:
            #     if rest.startswith(symbol):
            #         parts.append(SYMBOL_TO_TOKEN_TYPE[symbol])
            #         index += len(symbol)
            #         break
            # else:

        print(parts)


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


parser = Parser.from_proposition('((aap => waarheid) => hoiii) => hoiii')
