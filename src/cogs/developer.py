import io
import os
import re
import sys
import copy
import enum
import json
import math
import time
import base64
import pprint
import random
import string
import typing
import urllib
import asyncio
import inspect
import secrets
import sqlite3
import argparse
import datetime
import textwrap
import threading
import traceback
import importlib
import contextlib
import subprocess
import pkg_resources
import multiprocessing
from typing import Literal, Optional
from contextlib import redirect_stdout, redirect_stderr

import cogs
import utils
import views
import checks
import config
import logger
import classes
import objects
import utils.bot
import utils.colors
import utils.console
import views.pagination
from logger import logging, Logger
from classes import Bot, Cog, Context, CommandTree

import pytz
import dotenv
import aiohttp
import discord
import requests
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

class Developer(Cog):
    """All developer utilities."""
    
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.emoji = "🔨"
        self.short_description = "All developer utilities"
        self.hidden = True
        self._last_result = None
    
    async def cog_check(self, ctx: Context) -> bool:
        if ctx.author.id == 1027998777333788693 or checks._is_admin(ctx):
            return True
        else:
            return False

    @commands.command(aliases=["load_extension"])
    async def load(self, ctx: Context, cog: str) -> None:
        """Load a cog"""
        ext = cogs.__package__+"."+cog
        logging.warning(f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to load `{ext}`")
        await self.bot.load_extension(ext)
        await ctx.send(f"✅ Loaded the extension: `{ext}`")
        logging.info(f"successfully loaded `{ext}`")

    @commands.command(aliases=["unload_extension"])
    async def unload(self, ctx: Context, cog: str) -> None:
        """Unload a cog"""
        ext = cogs.__package__+"."+cog
        logging.warning(f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to unload `{ext}`")
        await self.bot.unload_extension(ext)
        await ctx.send(f"✅ Unloaded the extension: `{ext}`")
        logging.info(f"successfully unloaded `{ext}`")

    @commands.command(aliases=["r", "re", "reload_all", "reload_extension", "reload_all_extensions"])
    async def reload(self, ctx: Context, *cogs: str) -> None:
        """Reload an or all cogs"""
        if len(cogs) == 0:
            extensions = [k for k in self.bot.extensions.keys()]
            
            msg = await ctx.send("🔨 Reloading all extensions...")
            logging.warning(f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to reload all extensions")
        
        else:
            extensions = [cogs.__package__+"."+cog for cog in cogs]
            
            msg = await ctx.send(f"🔨 Reloading: `{'`, `'.join(extensions)}`")
            logging.warning(f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to reload `{'`, `'.join(extensions)}`")
        
        ext_status = ""
        for ext in extensions:
            try:
                await self.bot.reload_extension(ext)
            
            except Exception as e:
                t = f"failed to reload `{ext}`: `{e.__class__.__name__}`"
                logging.error(t, exc_info=e)
                ext_status += "❌ " + t[0].upper() + t[1:] + "\n"
            
            else:
                t = f"successfully reloaded `{ext}`"
                logging.info(t)
                ext_status += "✅ " + t.capitalize() + "\n"
        
        await msg.edit(content=ext_status)
    
    @commands.command(aliases=["exts", "loaded", "loaded_extensions"])
    async def extensions(self, ctx: Context) -> None:
        """List all loaded cogs"""
        paginated_list = utils.paginate([f"`{k}`" for k in self.bot.extensions.keys()])
        extensions = [", ".join(group) for group in paginated_list]
        extensions = ",\n".join(extensions)
        
        await ctx.send("All loaded extensions:\n"+
                       extensions)

    @load.error
    @unload.error
    @reload.error
    async def on_extension_error(self, ctx: Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CheckFailure) or isinstance(error, commands.MissingRequiredArgument):
            return
        
        elif isinstance(error, commands.CommandInvokeError):
            error = error.original
            
            if len(ctx.args) > 2:
                ext = cogs.__package__+"."+ctx.args[2]
                logging.error(f"failed to {ctx.command.name} `{ext}`: `{error.__class__.__name__}`", exc_info=error)
                await ctx.send(f"❌ Error occured while {ctx.command.name}ing the extension: `{ext}`\n"+
                    utils.code(f"{error.__class__.__name__}: {str(error)}"))
    
    @commands.command()
    async def restart(self, ctx: Context) -> None:
        """Restart the bot"""
        logging.warning(f"{ctx.author.display_name} (@{ctx.author}, id: {ctx.author.id}) wants to restart the bot")
        
        logging.warning("informing logs channel")
        try:
            await self.bot.log_channel.send(f"{ctx.author.mention} **{ctx.author.display_name}** *(@{ctx.author}, id: __{ctx.author.id}__)* wants to restart the bot")
            await self.bot.log_channel.send("restarting...")
        except Exception as e:
            logging.error("couldn't inform logs channel, ignoring and restarting", exc_info=e)
        
        try:
            await ctx.react("🫠")
        except Exception as e:
            logging.error("couldn't react to message, ignoring and restarting", exc_info=e)
        
        logging.warning("replacing current process with a new one")
        logging.warning(f"running `{' '.join([sys.executable] + sys.argv)}` in os.execv()")
        logging.critical("abandoned")
        print()
        os.execv(sys.executable, ["python"] + sys.argv)
    
    @commands.command()
    async def shutdown(self, ctx: Context) -> None:
        """Shutdown the bot"""
        logging.warning(f"{ctx.author.display_name} (@{ctx.author}, id: {ctx.author.id}) wants to shutdown the bot")
        
        logging.warning("informing logs channel")
        try:
            await self.bot.log_channel.send(f"{ctx.author.mention} **{ctx.author.display_name}** *(@{ctx.author}, id: __{ctx.author.id}__)* wants to shutdown the bot")
            await self.bot.log_channel.send("shutting down...")
        except Exception as e:
            logging.error("couldn't inform logs channel, ignoring and shutting down", exc_info=e)
        
        try:
            await ctx.react("🫀")
        except Exception as e:
            logging.error("couldn't react to message, ignoring and shutting down", exc_info=e)
        
        logging.warning("shutting down")
        logging.warning("closing bot using await bot.close()")
        await self.bot.close()
    
    @commands.command(name="generate-invite", aliases=["invite", "invite-link"])
    async def generate_invite(self, ctx: Context) -> None:
        """Generate a bot invite link for testing purposes"""
        await ctx.send(f"**[Click to invite me](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot+applications.commands)**")
    
    @commands.command()
    async def sudo(
        self,
        ctx: Context,
        channel: Optional[discord.TextChannel],
        who: discord.Member | discord.User,
        *,
        command: str
    ) -> None:
        """Run a command as another user optionally in another channel"""
        msg = copy.copy(ctx.message)
        new_channel = channel or ctx.channel
        msg.channel = new_channel
        msg.author = who
        msg.content = ctx.prefix + command
        new_ctx = await self.bot.get_context(msg, cls=type(ctx))
        await self.bot.invoke(new_ctx)

    @commands.command()
    async def do(
        self,
        ctx: Context,
        times: int,
        channel: Optional[discord.TextChannel],
        who: Optional[discord.Member | discord.User],
        *,
        command: str
    ) -> None:
        """Repeats a command a specified number of times optionally as another person optionally in another channel"""
        msg = copy.copy(ctx.message)
        new_channel = channel or ctx.channel
        msg.channel = new_channel
        msg.author = who or ctx.author
        msg.content = ctx.prefix + command
        
        new_ctx = await self.bot.get_context(msg, cls=type(ctx))
        
        for i in range(times):
            await new_ctx.reinvoke()
    
    @commands.command(name="add-clyde", aliases=["addclyde", "add_clyde"])
    @commands.bot_has_guild_permissions(ban_members=True)
    async def add_clyde(self, ctx: Context) -> None:
        """Add Clyde to the current Discord server"""
        clyde = discord.Object(1081004946872352958)
        await ctx.guild.ban(clyde)
        await ctx.guild.unban(clyde)
        await ctx.success()
    
    @commands.command(name="remove-clyde", aliases=["removeclyde", "remove_clyde"])
    @commands.bot_has_guild_permissions(ban_members=True)
    async def remove_clyde(self, ctx: Context) -> None:
        """Remove Clyde from the current Discord server"""
        clyde = discord.Object(1081004946872352958)
        await ctx.guild.ban(clyde)
        await ctx.success()
    
    @commands.command(name="exec", aliases=["eval", "run"])
    async def _exec(self, ctx: Context, *, code: str) -> None:
        """Execute async code"""
        bot = self.bot
        
        logging.warn(f"{ctx.clean_prefix}exec called by {ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id})")
        
        env = {
            "bot": bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "user": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "prisma": bot.prisma,
            "log_channel": bot.log_channel,
            "_": self._last_result,
            
            "io": io,
            "os": os,
            "re": re,
            "sys": sys,
            "copy": copy,
            "enum": enum,
            "json": json,
            "math": math,
            "time": time,
            "base64": base64,
            "pprint": pprint,
            "random": random,
            "string": string,
            "typing": typing,
            "urllib": urllib,
            "asyncio": asyncio,
            "inspect": inspect,
            "secrets": secrets,
            "sqlite3": sqlite3,
            "argparse": argparse,
            "datetime": datetime,
            "textwrap": textwrap,
            "threading": threading,
            "traceback": traceback,
            "importlib": importlib,
            "contextlib": contextlib,
            "subprocess": subprocess,
            "pkg_resources": pkg_resources,
            "multiprocessing": multiprocessing,
            "redirect_stdout": redirect_stdout,
            "redirect_stderr": redirect_stderr,
            
            "cogs": cogs,
            "cogs": cogs,
            "utils": utils,
            "views": views,
            "checks": checks,
            "config": config,
            "logger": logger,
            "classes": classes,
            "objects": objects,
            "Logger": Logger,
            "Bot": Bot,
            "Cog": Cog,
            "Context": Context,
            "CommandTree": CommandTree,
            
            "pytz": pytz,
            "dotenv": dotenv,
            "aiohttp": aiohttp,
            "discord": discord,
            "requests": requests,
            "commands": commands,
            "app_commands": app_commands,
            "load_dotenv": load_dotenv
        }
        
        env.update(globals())
        
        code = utils.cleanup_code(code)
        stdout = io.StringIO()
        
        to_compile = f"async def func():\n{textwrap.indent(code, '    ')}"
        
        async with ctx.typing():
            t = time.monotonic()
                    
            try:
                exec(to_compile, env)

            except Exception as e:
                t = time.monotonic() - t # in seconds
                if t < 1:
                    t = round(t * 1000) # in milliseconds and round
                    time_text = f"{t}ms"

                elif t > 60:
                    t = round(t/60, 2) # in minutes and round to 2 decimal places
                    time_text = f"{t}m"

                else:
                    t = round(t, 2) # if in seconds then round to 2 decimal places
                    time_text = f"{t}s"

                try: await ctx.failure()
                except: pass

                embed = discord.Embed(
                    title = "Execution Failed at exec()",
                    description = utils.code(f"[ERROR]: {(e.__class__.__module__+'.' if e.__class__.__module__ != 'builtins' else '')+e.__class__.__name__}\n"
                                             f" -> {e}", "prolog"),
                    color = discord.Color.red(),
                    timestamp = discord.utils.utcnow()
                )

                version = "{version.major}.{version.minor}.{version.micro}".format(version=sys.version_info)
                dpy_version = pkg_resources.get_distribution("discord.py").version
                embed.add_field(
                    name = "System Info",
                    value = f"Python `{version}`\n"
                            f"discord.py `{dpy_version}`"
                )

                embed.add_field(
                    name = "Execution Info",
                    value = f"Took `{time_text}`\n"
                            f"Return Type: `{type(e)}`"
                )

                embed.set_footer(
                    text = f"Requested by {ctx.author}",
                    icon_url = ctx.author.display_avatar
                )

                self._last_result = e
                logging.error(f"failed at `exec()` ({ctx.clean_prefix}exec by {ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id}))", exc_info=e)
                try:
                    await ctx.send(embed=embed)
                except Exception as e:
                    error = utils.code(f"[ERROR]: {(e.__class__.__module__+'.' if e.__class__.__module__ != 'builtins' else '')+e.__class__.__name__}\n"
                                       f" -> {e}", "prolog")
                    await ctx.send(f"An error occured.\n"
                                   f"{error}")
                    logging.error("error occured while sending exec() failed embed", exc_info=e)

            func = env["func"]
            try:
                with redirect_stdout(stdout), redirect_stderr(stdout):
                    ret = await func()

            except Exception as e:
                t = time.monotonic() - t # in seconds
                if t < 1:
                    t = round(t * 1000) # in milliseconds and round
                    time_text = f"{t}ms"

                elif t > 60:
                    t = round(t/60, 2) # in minutes and round to 2 decimal places
                    time_text = f"{t}m"

                else:
                    t = round(t, 2) # if in seconds then round to 2 decimal places
                    time_text = f"{t}s"

                try: await ctx.failure()
                except: pass
                
                output = stdout.getvalue()
                
                embed = discord.Embed(
                    title = "Execution Failed",
                    description = f"### Output:\n"
                                  f"{utils.code(output or 'No output recorded.', 'prolog')}",
                    color = discord.Color.red(),
                    timestamp = discord.utils.utcnow()
                )

                embed.add_field(
                    name = "Error",
                    value = utils.code(f"[ERROR]: {(e.__class__.__module__+'.' if e.__class__.__module__ != 'builtins' else '')+e.__class__.__name__}\n"
                                       f" -> {e}", "prolog"),
                    inline = False
                )

                version = "{version.major}.{version.minor}.{version.micro}".format(version=sys.version_info)
                dpy_version = pkg_resources.get_distribution("discord.py").version
                embed.add_field(
                    name = "System Info",
                    value = f"Python `{version}`\n"
                            f"discord.py `{dpy_version}`"
                )

                embed.add_field(
                    name = "Execution Info",
                    value = f"Took `{time_text}`\n"
                            f"Return Type: `{type(e)}`"
                )

                embed.set_footer(
                    text = f"Requested by {ctx.author}",
                    icon_url = ctx.author.display_avatar
                )

                self._last_result = e

                output = (f"{output}\n"
                          f"Time taken: {time_text}")

                logging.error(f"EXECUTION FAILED! output of `exec` {ctx.clean_prefix}exec called by {ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id})\n"
                              f"{output}")
                logging.error(f"execution failed ({ctx.clean_prefix}exec by {ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id}))", exc_info=e)

                try:
                    await ctx.send(embed=embed)
                except discord.HTTPException:
                    await ctx.send("Embed too big to send. Check console.")
                except Exception as e:
                    error = utils.code(f"[ERROR]: {(e.__class__.__module__+'.' if e.__class__.__module__ != 'builtins' else '')+e.__class__.__name__}\n"
                                       f" -> {e}\n", "prolog")
                    await ctx.send(f"An error occured.\n"
                                   f"{error}")
                    logging.error("error occured while sending exec failed embed", exc_info=e)

            else:
                t = time.monotonic() - t # in seconds
                if t < 1:
                    t = round(t * 1000) # in milliseconds and round
                    time_text = f"{t}ms"

                elif t > 60:
                    t = round(t/60, 2) # in minutes and round to 2 decimal places
                    time_text = f"{t}m"

                else:
                    t = round(t, 2) # if in seconds then round to 2 decimal places
                    time_text = f"{t}s"

                try: await ctx.success()
                except: pass

                output = stdout.getvalue()

                output_embed = utils.code(
                    (output or "No output recorded.")+
                    (f"\n-- {repr(ret)}" if ret is not None else ""),
                    "prolog"
                )

                embed = discord.Embed(
                    title = "Execution Successful",
                    description = f"### Output:\n"
                                  f"{output_embed}",
                    color = discord.Color.green(),
                    timestamp = discord.utils.utcnow()
                )

                version = "{version.major}.{version.minor}.{version.micro}".format(version=sys.version_info)
                dpy_version = pkg_resources.get_distribution("discord.py").version
                embed.add_field(
                    name = "System Info",
                    value = f"Python `{version}`\n"
                            f"discord.py `{dpy_version}`"
                )

                embed.add_field(
                    name = "Execution Info",
                    value = f"Took `{time_text}`\n"
                            f"Return Type: `{type(ret)}`"
                )

                embed.set_footer(
                    text = f"Requested by {ctx.author}",
                    icon_url = ctx.author.display_avatar
                )

                self._last_result = ret

                output = (f"{output}\n"
                          f"Returned: {repr(ret)}\n"
                          f"Type: {type(ret)}\n"
                          f"Time taken: {time_text}")

                logging.info(f"execution successful; output of `exec` {ctx.clean_prefix}exec called by {ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id})\n"
                             f"{output}")

                try:
                    if ctx.output:
                        await ctx.send(embed=embed)
                except discord.HTTPException:
                    await ctx.send("Embed too big to send. Check console.")
                except Exception as e:
                    error = utils.code(f"[ERROR]: {e.__class__.__name__}\n"
                                       f" -> {e}\n", "prolog")
                    await ctx.send(f"An error occured.\n"
                                   f"{error}")
                    logging.error("error occured while sending exec successful embed", exc_info=e)
    
    @commands.guild_only()
    @commands.command()
    async def sync(self, ctx: Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        """Sync slash commands (Umbra's Sync Command)
        https://about.abstractumbra.dev/discord.py/2023/01/29/sync-command-example.html
        """
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

async def setup(bot: Bot) -> None:
    await bot.add_cog(Developer(bot))