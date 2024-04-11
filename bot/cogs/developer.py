import copy
from typing import Literal, Optional

from ..        import cogs
from ..        import utils
from ..        import config
from ..logger  import logging
from ..classes import Bot, Cog, Context

import discord
from discord.ext import commands

class Developer(Cog):
    """All developer utilities."""
    
    def __init__(self, bot: Bot):
        self.bot = bot
        self.emoji = "🔨"
        self.short_description = "All developer utilities"
    
    async def cog_check(self, ctx: Context) -> bool:
        if ctx.author.id == 1027998777333788693 or ctx.author.id in config.ADMINS:
            return True
        else:
            raise commands.MissingPermissions([])

    @commands.command(aliases=["load_extension"])
    async def load(self, ctx: Context, cog: str):
        """Load a cog."""
        ext = cogs.__package__+"."+cog
        logging.warning(f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to load `{ext}`")
        await self.bot.load_extension(ext)
        await ctx.send(f"✅ Loaded the extension: `{ext}`")
        logging.info(f"successfully loaded `{ext}`")

    @commands.command(aliases=["unload_extension"])
    async def unload(self, ctx: Context, cog: str):
        """Unload a cog."""
        ext = cogs.__package__+"."+cog
        logging.warning(f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to unload `{ext}`")
        await self.bot.unload_extension(ext)
        await ctx.send(f"✅ Unloaded the extension: `{ext}`")
        logging.info(f"successfully unloaded `{ext}`")

    @commands.command(aliases=["r", "re", "reload_all", "reload_extension", "reload_all_extensions"])
    async def reload(self, ctx: Context, *cogs: str):
        """Reload an or all cogs."""
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
    async def extensions(self, ctx: Context):
        """List all loaded cogs."""
        
        paginated_list = utils.paginate([f"`{k}`" for k in self.bot.extensions.keys()])
        extensions = [", ".join(group) for group in paginated_list]
        extensions = ",\n".join(extensions)
        
        await ctx.send("All loaded extensions:\n"+
                       extensions)

    @load.error
    @unload.error
    @reload.error
    async def on_extension_error(self, ctx: Context, error: commands.CommandError):
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
    async def sudo(
        self,
        ctx: Context,
        channel: Optional[discord.TextChannel],
        who: discord.Member | discord.User,
        *,
        command: str
    ):
        """Run a command as another user optionally in another channel."""
        msg = copy.copy(ctx.message)
        new_channel = channel or ctx.channel
        msg.channel = new_channel
        msg.author = who
        msg.content = ctx.prefix + command
        new_ctx = await self.bot.get_context(msg, cls=type(ctx))
        await self.bot.invoke(new_ctx)

    @commands.command()
    async def do(self, ctx: Context, times: int, *, command: str):
        """Repeats a command a specified number of times."""
        msg = copy.copy(ctx.message)
        msg.content = ctx.prefix + command

        new_ctx = await self.bot.get_context(msg, cls=type(ctx))

        for i in range(times):
            await new_ctx.reinvoke()

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