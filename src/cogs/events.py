import utils
import aiohttp
import requests
from logger  import logging

import config
from classes import Bot, Cog, Context

import discord
from discord.ext import commands, tasks

class Events(Cog):
    """All bot events"""
    
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info(f"serving {len(self.bot.guilds)} guilds and {len(self.bot.users)} users")
        logging.info("ready to handle commands")
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, exception: commands.CommandError) -> None:
        if isinstance(exception, commands.MissingRequiredArgument):
            if config.MISSING_ARGUMENT_MESSAGE:
                msg = config.MISSING_ARGUMENT_MESSAGE.format(
                    argument=exception.param.name,
                    type=exception.param.converter.__name__,
                    prefix=ctx.prefix,
                    clean_prefix=ctx.clean_prefix,
                    command=ctx.command,
                    message=ctx.message,
                    user=ctx.author,
                    ctx=ctx,
                    bot=ctx.bot
                )
                try:    await ctx.reply(msg)
                except: await ctx.send(f"{ctx.author.mention}, {msg}")
        
        elif isinstance(exception, commands.MissingPermissions):
            if config.NO_PERMISSIONS_MESSAGE:
                msg = config.NO_PERMISSIONS_MESSAGE.format(
                    prefix=ctx.prefix,
                    clean_prefix=ctx.clean_prefix,
                    command=ctx.command,
                    message=ctx.message,
                    user=ctx.author,
                    perms=exception.missing_permissions,
                    permissions=exception.missing_permissions,
                    joined_permissions=", ".join(exception.missing_permissions),
                    joined_permissions_code=", ".join(f"`{permission}`" for permission in exception.missing_permissions),
                    ctx=ctx,
                    bot=ctx.bot
                )
                try:    await ctx.reply(msg)
                except: await ctx.send(f"{ctx.author.mention}, {msg}")
        
        elif isinstance(exception, commands.BotMissingPermissions):
            if config.BOT_NO_PERMISSIONS_MESSAGE:
                msg = config.BOT_NO_PERMISSIONS_MESSAGE.format(
                    prefix=ctx.prefix,
                    clean_prefix=ctx.clean_prefix,
                    command=ctx.command,
                    message=ctx.message,
                    user=ctx.author,
                    perms=exception.missing_permissions,
                    permissions=exception.missing_permissions,
                    joined_permissions=", ".join(exception.missing_permissions),
                    joined_permissions_code=", ".join(f"`{permission}`" for permission in exception.missing_permissions),
                    ctx=ctx,
                    bot=ctx.bot
                )
                try:    await ctx.reply(msg)
                except: await ctx.send(f"{ctx.author.mention}, {msg}")
        
        elif isinstance(exception, commands.CommandNotFound):
            if config.LOG_NOT_FOUND_COMMANDS_TO_CONSOLE:
                logging.error(f"{ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id}) used {ctx.message.content} but command `{ctx.message.content[len(ctx.prefix or ""):].split()[0]}` doesn't exist!")
            
            if config.COMMAND_NOT_FOUND_MESSAGE:
                msg = config.COMMAND_NOT_FOUND_MESSAGE.format(
                    prefix=ctx.prefix,
                    clean_prefix=ctx.clean_prefix,
                    command=ctx.message.content[len(ctx.prefix or ""):].split()[0],
                    message=ctx.message,
                    user=ctx.author,
                    ctx=ctx,
                    bot=ctx.bot,
                )
                try:    await ctx.reply(msg)
                except: await ctx.send(f"{ctx.author.mention}, {msg}")
        
        else:
            raise exception

async def setup(bot: Bot) -> None:
    await bot.add_cog(Events(bot))