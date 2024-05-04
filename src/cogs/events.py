import config
from logger import logging
from classes import Bot, Cog, Context

from discord.ext import commands

class Events(Cog):
    """All bot events"""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.emoji = None
        self.hidden = True
    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.log_channel = self.bot.get_channel(self.bot.log_channel_id)
        
        if not self.bot.log_channel:
            logging.critical(f"log channel with id {self.bot.log_channel_id} not found. this may cause problems.")
        else:
            logging.info(f"log channel: #{self.bot.log_channel.name} (id: {self.bot.log_channel.id})")
        
        logging.info(f"serving {len(self.bot.guilds)} guilds and {len(self.bot.users)} users")
        logging.info("ready to handle commands")
        await self.bot.log_channel.send(f"**{self.bot.user.name}** is ready")
    
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
                    message=ctx.message,
                    user=ctx.author,
                    ctx=ctx,
                    bot=ctx.bot
                ))
        
        elif isinstance(exception, commands.MissingPermissions):
            if config.NO_PERMISSIONS_MESSAGE:
                await ctx.send(config.NO_PERMISSIONS_MESSAGE.format(
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
                ))
        
        elif isinstance(exception, commands.BotMissingPermissions):
            if config.BOT_NO_PERMISSIONS_MESSAGE:
                await ctx.send(config.BOT_NO_PERMISSIONS_MESSAGE.format(
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
                ))
        
        elif isinstance(exception, commands.CommandNotFound):
            if config.LOG_NOT_FOUND_COMMANDS_TO_CONSOLE:
                logging.error(f"{ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id}) used {ctx.message.content} but command `{ctx.message.content[len(ctx.prefix):].split()[0]}` doesn't exist!")
            
            if config.COMMAND_NOT_FOUND_MESSAGE:
                await ctx.send(config.COMMAND_NOT_FOUND_MESSAGE.format(
                    prefix=ctx.prefix,
                    clean_prefix=ctx.clean_prefix,
                    command=ctx.message.content[len(ctx.prefix):].split()[0],
                    message=ctx.message,
                    user=ctx.author,
                    ctx=ctx,
                    bot=ctx.bot,
                ))
        
        else:
            raise exception
    
    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context) -> None:
        """Log commands to console and increase the commands_used counter"""
        prisma = self.bot.prisma
        
        if config.LOG_COMMANDS_TO_CONSOLE:
            logging.info(f"{ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id}) used {ctx.message.content}")
        
        guild_stats = await prisma.statistics.find_unique(
            where = {"guild_id": ctx.guild.id}
        )

        if guild_stats:
            await prisma.statistics.update(
                where = {"guild_id": ctx.guild.id},
                data = {"commands_used": {"increment": 1}}
            )
        
        else:
            await prisma.statistics.create(
                data = {"guild_id": ctx.guild.id, "commands_used": 1}
            )

async def setup(bot: Bot) -> None:
    await bot.add_cog(Events(bot))