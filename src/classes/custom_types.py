from typing import (
    Iterable,
    Callable, Awaitable,
    TypeVar, ParamSpec
)

from .bot     import Bot
from .cog     import Cog
from .context import Context

from discord import Message

__all__ = (
    "BotT",
    "CogT",
    "ContextT",
    "ContextT_co",
    "BasicPrefix",
    "SyncPrefixFunc",
    "AsyncPrefixFunc",
    "PrefixType"
)

T = TypeVar("T")
P = ParamSpec("P")

MaybeAwaitable     = T | Awaitable[T]
MaybeAwaitableFunc = Callable[P, MaybeAwaitable[T]]

BotT         = TypeVar("BotT",        bound=Bot,     covariant=True)
CogT         = TypeVar("CogT",        bound=Cog                    )
ContextT     = TypeVar("ContextT",    bound=Context                )
ContextT_co  = TypeVar("ContextT_co", bound=Context, covariant=True)

BasicPrefix     = str | Iterable[str]
SyncPrefixFunc  = Callable[[Bot, Message], BasicPrefix]
AsyncPrefixFunc = Callable[[Bot, Message], Awaitable[BasicPrefix]]
PrefixType      = BasicPrefix | SyncPrefixFunc | AsyncPrefixFunc