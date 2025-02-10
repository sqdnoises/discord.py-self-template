import io
import os
import sys
import copy
import json
import time
import random
import asyncio
import datetime
import textwrap
import pkg_resources
from typing     import (
    TYPE_CHECKING, Optional
)
from contextlib import (
    redirect_stdout, redirect_stderr
)

from ..        import utils
from ..        import checks
from ..        import config
from ..logger  import logging
from ..classes import Bot, Cog, Context

import discord
from discord.ext import commands

class Developer(Cog):
    """All developer utilities."""
    
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.emoji = "🔨"
        self.short_description = "All developer utilities"
        self._last_result = None
    
    async def cog_check(self, ctx: Context) -> bool:
        return checks.is_admin(ctx)
    
    @commands.command(aliases=["load-extension"])
    async def load(self, ctx: Context, cog: str) -> None:
        """Loads a specified cog.
        
        Parameters
        ----------
        cog : str
            The name of the cog to load (without the 'cogs.' prefix).
        """
        ext = "cogs."+cog
        logging.warning(f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to load `{ext}`")
        await self.bot.load_extension(ext)
        await ctx.send(f"✅ Loaded the extension: `{ext}`")
        logging.info(f"successfully loaded `{ext}`")
    
    @commands.command(aliases=["unload-extension"])
    async def unload(self, ctx: Context, cog: str) -> None:
        """Unloads a specified cog.
        
        Parameters
        ----------
        cog : str
            The name of the cog to unload (without the 'cogs.' prefix).
        """
        ext = "cogs."+cog
        logging.warning(f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to unload `{ext}`")
        await self.bot.unload_extension(ext)
        await ctx.send(f"✅ Unloaded the extension: `{ext}`")
        logging.info(f"successfully unloaded `{ext}`")
    
    @commands.command(aliases=["r", "re", "reload-all", "reload-extension", "reload-all-extensions"])
    async def reload(self, ctx: Context, *cogs: str) -> None:
        """Reloads specified cogs or all cogs if none are specified.
        
        Parameters
        ----------
        *cogs : str
            The name(s) of the cog(s) to reload (without the 'cogs.' prefix).
            If no cogs are specified, all cogs will be reloaded.
        """
        if len(cogs) == 0:
            extensions = [k for k in self.bot.extensions.keys()]
            
            msg = await ctx.send("🔨 Reloading all extensions...")
            logging.warning(f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to reload all extensions")
        
        else:
            extensions = ["cogs."+cog for cog in cogs]
            
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
    
    @commands.command(aliases=["exts", "loaded", "loaded-extensions"])
    async def extensions(self, ctx: Context) -> None:
        """Lists all currently loaded cogs."""
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
            e = error.original
            
            if ctx.command and len(ctx.args) > 2:
                ext = "cogs."+ctx.args[2]
                logging.error(f"failed to {ctx.command.name} `{ext}`: `{error.__class__.__name__}`", exc_info=error)
                await ctx.send(f"❌ Error occurred while {ctx.command.name}ing the extension: `{ext}`\n"+
                               utils.code(f"{e.__class__.__name__}: {str(e)}"))
            
            else:
                raise error
        
        else:
            raise error
    
    @commands.command()
    async def restart(self, ctx: Context) -> None:
        """Restarts the bot."""
        logging.warning(f"{ctx.author.display_name} (@{ctx.author}, id: {ctx.author.id}) is restarting the bot")
        
        try:
            await ctx.react("🫠")
        except Exception as e:
            logging.error("couldn't react to message, ignoring and restarting", exc_info=e)
        
        logging.warning("closing bot and replacing current process with a new one by running:\n"
                        f"`{' '.join([sys.executable] + sys.argv)}` in os.execv()")
        await self.bot.close()
        os.execv(sys.executable, ["python"] + sys.argv)
    
    @commands.command()
    async def shutdown(self, ctx: Context) -> None:
        """Shuts down the bot."""
        logging.warning(f"{ctx.author.display_name} (@{ctx.author}, id: {ctx.author.id}) is shutting down the bot")
        
        try:
            await ctx.react("🫀")
        except Exception as e:
            logging.error("couldn't react to message, ignoring and shutting down", exc_info=e)
        
        logging.warning("shutting down")
        logging.warning("closing bot using await bot.close()")
        await self.bot.close()
    
    @commands.command()
    async def sudo(
        self,
        ctx: Context,
        channel: Optional[discord.TextChannel],
        who: discord.Member | discord.User,
        *,
        command: str
    ) -> None:
        """Runs a command as another user, optionally in another channel.
        
        Parameters
        ----------
        channel : Optional[discord.TextChannel]
            The channel to run the command in. If not specified, it defaults to the current channel.
        who : discord.Member | discord.User
            The user to impersonate when running the command.
        command : str
            The command to run.
        """
        if TYPE_CHECKING and ctx.prefix is None:
            # to satisfy the typechecker
            return
        
        msg = copy.copy(ctx.message)
        new_channel = channel or ctx.channel
        msg.channel = new_channel
        msg.author = who
        msg.content = ctx.prefix + command
        new_ctx = await self.bot.get_context(msg, cls=type(ctx))
        await self.bot.invoke(new_ctx)
    
    @commands.command(name="exec", aliases=["eval", "run"])
    async def _exec(self, ctx: Context, *, code: str) -> None:
        """Executes async python code.
        
        Parameters
        ----------
        code : str
            The code to execute.
        """
        bot = self.bot
        
        logging.warn(f"{ctx.clean_prefix}exec called by {ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id})")
        
        version = "{version.major}.{version.minor}.{version.micro}".format(version=sys.version_info)
        dpy_version = pkg_resources.get_distribution("discord.py-self").version
        
        env = {
            "bot": bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "user": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result,
            
            "os": os,
            "sys": sys,
            "json": json,
            "time": time,
            "random": random,
            "asyncio": asyncio,
            "datetime": datetime,
            
            "config": config,
            
            "discord": discord,
            "commands": commands
        }
        
        env.update(globals())
        
        code = utils.cleanup_code(code)
        stdout = io.StringIO()
        
        to_compile = f"async def func():\n{textwrap.indent(code, '    ')}"
        
        response_text = ""  # Initialize an empty string to store the output
        
        async with ctx.typing():
            t = time.monotonic()
            
            try:
                exec(to_compile, env)
            
            except Exception as e:
                t = time.monotonic() - t
                if t < 1:
                    t = round(t * 1000)
                    time_text = f"{t}ms"
                
                elif t > 60:
                    t = round(t / 60, 2)
                    time_text = f"{t}m"
                
                else:
                    t = round(t, 2)
                    time_text = f"{t}s"
                
                try: await ctx.failure()
                except: pass
                
                error_text = utils.error(e, include_module=True)
                
                response_text = (
                     "## `❌` Execution Failed at exec()\n"
                    f"**Error:**\n{textwrap.indent(error_text, '> ', lambda _: True)}\n"
                     "**System Info:**\n"
                    f"> Python `{version}`\n"
                    f"> discord.py-self`{dpy_version}`\n\n"
                     "**Execution Info:**\n"
                    f"> Took `{time_text}`\n"
                    f"> Return Type: `{type(e)}`"
                )
                
                self._last_result = e
                logging.error(f"failed at `exec()` ({ctx.clean_prefix}exec by {ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id}))", exc_info=e)
            
            else:
                func = env["func"]
                try:
                    with redirect_stdout(stdout), redirect_stderr(stdout):
                        ret = await func()
                
                except Exception as e:
                    t = time.monotonic() - t
                    if t < 1:
                        t = round(t * 1000)
                        time_text = f"{t}ms"
                    
                    elif t > 60:
                        t = round(t / 60, 2)
                        time_text = f"{t}m"
                    
                    else:
                        t = round(t, 2)
                        time_text = f"{t}s"
                    
                    try: await ctx.failure()
                    except: pass
                    
                    output = stdout.getvalue()
                    error_text = utils.error(e, include_module=True)
                    
                    response_text = f"## `❌` Execution Failed\n"
                    
                    if output.strip():
                        response_text += f"**Output:**\n{textwrap.indent(utils.code(output, 'prolog'), '> ', lambda _: True)}\n"
                    else:
                        response_text += f"**Output:**\n> No output recorded.\n"
                    
                    response_text += (
                        f"\n**Error:**\n{textwrap.indent(error_text, '> ', lambda _: True)}\n\n"
                         "**System Info:**\n"
                        f"> Python `{version}`\n"
                        f"> discord.py-self `{dpy_version}`\n\n"
                         "**Execution Info:**\n"
                        f"> Took `{time_text}`\n"
                        f"> Return Type: `{type(e)}`"
                    )
                    
                    self._last_result = e
                    
                    output = (f"{output}\n"
                              f"Time taken: {time_text}")
                    
                    logging.error(f"EXECUTION FAILED! output of `exec` {ctx.clean_prefix}exec called by {ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id})\n"
                                f"{output}")
                    logging.error(f"execution failed ({ctx.clean_prefix}exec by {ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id}))", exc_info=e)
                
                else:
                    t = time.monotonic() - t
                    if t < 1:
                        t = round(t * 1000)
                        time_text = f"{t}ms"
                    
                    elif t > 60:
                        t = round(t / 60, 2)
                        time_text = f"{t}m"
                    
                    else:
                        t = round(t, 2)
                        time_text = f"{t}s"
                    
                    try: await ctx.success()
                    except: pass
                    
                    output = stdout.getvalue()
                    
                    response_text = "## `✅` Execution Successful\n"
                    
                    if output.strip():
                        response_text += f"**Output:**\n{textwrap.indent(utils.code(output, 'prolog'), '> ', lambda _: True)}\n"
                    else:
                        response_text += f"**Output:**\n> No output recorded.\n"
                    
                    response_text += (f"**Returned:** `{repr(ret)}`\n" if ret is not None else "") + (
                        f"**Type:** `{type(ret)}`\n" if ret is not None else ""
                    ) + (
                        f"\n**System Info:**\n"
                        f"> Python `{version}`\n"
                        f"> discord.py-self `{dpy_version}`\n\n"
                        f"**Execution Info:**\n"
                        f"> Took `{time_text}`"
                    )
                        
                    self._last_result = ret
                    
                    output = (f"{output}\n"
                            f"Returned: {repr(ret)}\n"
                            f"Type: {type(ret)}\n"
                            f"Time taken: {time_text}")
                    
                    logging.info(f"execution successful; output of `exec` {ctx.clean_prefix}exec called by {ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id})\n"
                                f"{output}")
        
        try:
            await ctx.reply(response_text)
        except:
            try:
                await ctx.send(response_text)
            except discord.HTTPException:
                await ctx.send("Output too big to send. Check console.")
            except Exception as e:
                error = utils.error(e)
                await ctx.send(f"An error occurred.\n"
                                f"{error}")
                logging.error("error occurred while sending execution failed output", exc_info=e)

async def setup(bot: Bot) -> None:
    await bot.add_cog(Developer(bot))