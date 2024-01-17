from discord import app_commands
from discord.ext import commands
from discord.utils import MISSING

from .cog import Cog
from .context import Context
from .interaction import Interaction

from __future__ import annotations



print('yoooooo')
"""some string waddup"""

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Concatenate,
    Coroutine,
    ParamSpec,
    TypeVar,
    Union,
)
if TYPE_CHECKING:
    from discord.app_commands import Group
    from discord.app_commands.models import (
        Choice,
        ChoiceT,
    )

    from typing import (
        TYPE_CHECKING,
        Any,
    )
    Binding = Union[Group, commands.Cog]
    GroupT = TypeVar('GroupT', bound=Binding)
    AutocompleteCallback = Union[
        Callable[[GroupT, Interaction, str], Coroutine[Any, Any, list[Choice[ChoiceT]]]],
        Callable[[Interaction, str], Coroutine[Any, Any, list[Choice[ChoiceT]]]],
    ]


T = TypeVar('T')
P = ParamSpec('P')
CogT = TypeVar('CogT', bound='Cog')
ContextT = TypeVar('ContextT', bound='Context')

CommandCallback = Union[
    Callable[Concatenate[CogT, ContextT, P], Coroutine[Any, Any, T]],
    Callable[Concatenate[ContextT, P], Coroutine[Any, Any, T]],
]


__all__ = (
    'hybrid_command',
)


class HybridCommand(commands.HybridCommand[CogT, P, T]):
    if TYPE_CHECKING:
        def autocomplete(
            self,
            name: str,
        ) -> Callable[[AutocompleteCallback[CogT, ChoiceT]], AutocompleteCallback[CogT, ChoiceT]]:
            ...


if TYPE_CHECKING:
    def hybrid_command(
        name: Union[str, app_commands.locale_str] = MISSING,
        *,
        with_app_command: bool = True,
        **attrs: Any,
    ) -> Callable[[CommandCallback[CogT, Context, P, T]], HybridCommand[CogT, P, T]]:
        ...
else:
    hybrid_command = commands.hybrid_command
