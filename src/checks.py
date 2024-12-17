"""
Check functions that run to check stuff.
"""

import config
from classes import Context

import discord
from discord.ext import commands

def guild_only(ctx: Context):
    """Check if the command is invoked in a guild."""
    return bool(ctx.guild)

def is_guild_owner(ctx: Context):
    """Check if the command invoker is the guild owner."""
    if not ctx.guild:
        raise commands.NoPrivateMessage()
    return ctx.guild.owner == ctx.author

def is_in_vc(ctx: Context):
    """Check if the command invoker is in a voice channel."""
    return bool(ctx.voice)

def is_admin(ctx_or_user: Context | discord.Interaction | discord.Member | discord.User | int):
    """Helper function to check if a user is an admin."""
    if isinstance(ctx_or_user, Context):
        user = ctx_or_user.author
    elif isinstance(ctx_or_user, discord.Interaction):
        user = ctx_or_user.user
    elif isinstance(ctx_or_user, int):
        user = discord.Object(id=ctx_or_user)
    else:
        user = ctx_or_user
    
    return user.id in config.ADMINS