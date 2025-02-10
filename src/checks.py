"""
Check functions that run to check stuff.

Examples:
    @commands.check(checks.is_admin)
    @app_commands.check(checks.is_admin)
"""

from .        import config
from .classes import Context

import discord
from discord.ext import commands

__all__ = (
    "guild_only",
    "is_guild_owner",
    "is_in_vc",
    "is_admin",
)

CtxOrUser = Context | discord.Member | discord.User | int

def _get_user(ctx_or_user: CtxOrUser) -> discord.User | discord.Member | discord.Object:
    if isinstance(ctx_or_user, Context):
        return ctx_or_user.author
    elif isinstance(ctx_or_user, int):
        return discord.Object(id=ctx_or_user)
    else:
        return ctx_or_user

def guild_only(ctx: Context | discord.Interaction) -> bool:
    """Check if the command is invoked in a guild"""
    return bool(ctx.guild)

async def is_guild_owner(ctx: Context) -> bool:
    """Check if the command invoker is the guild owner"""
    if not ctx.guild:
        raise commands.NoPrivateMessage()
    return ctx.guild.owner == ctx.author

async def is_in_vc(ctx: Context) -> bool:
    """Check if the command invoker is in a voice channel"""
    return bool(ctx.author.voice if isinstance(ctx.author, discord.Member) else None)

def is_admin(ctx_or_user: CtxOrUser) -> bool:
    """Helper function to check if a user is an admin"""
    return _get_user(ctx_or_user).id in config.ADMINS