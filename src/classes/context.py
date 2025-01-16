from typing import Any, TYPE_CHECKING
import utils

if TYPE_CHECKING:
    from bot import Bot

import discord
from discord.ext import commands

class Context(commands.Context):
    """Utility class for commands that is used to easily interact with commands."""
    bot: "Bot"
    voice: discord.VoiceState | None
    cleaned_up_code: str
    out: bool = True
    
    def __init__(
        self,
        *args: Any, 
        **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.voice = self.author.voice if isinstance(self.author, discord.Member) else None
        self.cleaned_up_code = utils.cleanup_code(self.message.content)
    
    async def react(self, emoji: str | discord.Emoji) -> None:
        """Add reaction to a message"""
        await self.message.add_reaction(emoji)
    
    async def yes(self)          -> None: await self.react("✅")
    async def done(self)         -> None: await self.react("✅")
    async def tick(self)         -> None: await self.react("✅")
    async def check(self)        -> None: await self.react("✅")
    async def green(self)        -> None: await self.react("✅")
    async def success(self)      -> None: await self.react("✅")
    async def successful(self)   -> None: await self.react("✅")
    
    async def x(self)            -> None: await self.react("❌")
    async def no(self)           -> None: await self.react("❌")
    async def red(self)          -> None: await self.react("❌")
    async def fail(self)         -> None: await self.react("❌")
    async def cross(self)        -> None: await self.react("❌")
    async def failure(self)      -> None: await self.react("❌")
    async def unsuccessful(self) -> None: await self.react("❌")