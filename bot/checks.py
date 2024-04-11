"""
Check functions that run to check stuff
"""

from .        import config
from .classes import Context

import discord
from discord.ext import commands

def guild_only(ctx: Context = None):
    async def predicate(ctx: Context = ctx):
        if not ctx.guild:
            return False
        else:
            return True
    return commands.check(predicate)

def is_guild_owner(ctx: Context = None):
    async def predicate(ctx: Context = ctx):
        if not ctx.guild:
            raise commands.MissingPermissions(missing_permissions=[discord.Permissions.all])
        else:
            return True if ctx.guild.owner == ctx.author else False
    return commands.check(predicate)

def is_in_vc(ctx: Context = None):
    async def predicate(ctx: Context = ctx):
        if not ctx.author.voice:
            return False
        else:
            return True
    return commands.check(predicate)

def is_admin(ctx: Context = None):
    async def predicate(ctx: Context = ctx):
        if ctx.author.id in config.ADMIN:
            return True
        else:
            raise commands.MissingPermissions([])
    return commands.check(predicate)