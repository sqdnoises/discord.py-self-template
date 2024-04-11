from ..        import config
from ..logger  import logging
from ..classes import Bot, Cog, Context

from discord.ext import commands

class Events(Cog):
    """All bot events"""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.emoji = None
        self.hidden = True
    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info("ready to handle commands")
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, exception: commands.CommandError) -> None:
        if isinstance(exception, commands.MissingRequiredArgument):
            if config.MISSING_ARGUMENT_MESSAGE:
                await ctx.send(config.MISSING_ARGUMENT_MESSAGE.format(
                    argument=exception.param.name,
                    type=exception.param.converter.__name__,
                    prefix=ctx.prefix,
                    clean_prefix=ctx.clean_prefix,
                    command=ctx.command,
                    user=ctx.author
                ))
        
        elif isinstance(exception, commands.MissingPermissions):
            if config.NO_PERMISSIONS_MESSAGE:
                await ctx.send(config.NO_PERMISSIONS_MESSAGE.format(
                    prefix=ctx.prefix,
                    clean_prefix=ctx.clean_prefix,
                    command=ctx.command,
                    user=ctx.author,
                    perms=exception.missing_permissions,
                    permissions=exception.missing_permissions,
                    joined_permissions=", ".join(exception.missing_permissions),
                    joined_permissions_code=", ".join(f"`{permission}`" for permission in exception.missing_permissions)
                ))
        
        elif isinstance(exception, commands.BotMissingPermissions):
            if config.BOT_NO_PERMISSIONS_MESSAGE:
                await ctx.send(config.BOT_NO_PERMISSIONS_MESSAGE.format(
                    prefix=ctx.prefix,
                    clean_prefix=ctx.clean_prefix,
                    command=ctx.command,
                    user=ctx.author,
                    perms=exception.missing_permissions,
                    permissions=exception.missing_permissions,
                    joined_permissions=", ".join(exception.missing_permissions),
                    joined_permissions_code=", ".join(f"`{permission}`" for permission in exception.missing_permissions)
                ))
        
        else:
            raise exception
    
    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context) -> None:
        """Increase the commands_used counter"""
        prisma = self.bot.prisma
        
        guild_stats = await prisma.statistics.find_unique(
            where = {"guild_id": ctx.guild.id}
        )

        if guild_stats:
            await prisma.statistics.update(
                where = {"guild_id": ctx.guild.id},
                data = {"commands_used": guild_stats.commands_used + 1}
            )
        
        else:
            await prisma.statistics.create(
                data = {"guild_id": ctx.guild.id, "commands_used": 1}
            )

async def setup(bot: Bot) -> None:
    await bot.add_cog(Events(bot))