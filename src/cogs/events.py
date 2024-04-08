import logging
from classes import Bot
from discord.ext import commands
import prisma.errors as prisma_errors

class Events(commands.Cog):
    """All bot events"""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info("ready to handle commands")
    
    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context) -> None:
        """Increase the commands_used counter"""
        prisma = self.bot.prisma
        
        guild_stats = await prisma.statistics.find_unique(
            where={"guild_id": ctx.guild.id}
        )

        if guild_stats:
            await prisma.statistics.update(
                where={"guild_id": ctx.guild.id},
                data ={"commands_used": guild_stats.commands_used + 1}
            )
        
        else:
            await prisma.statistics.create(
                data={"guild_id": ctx.guild.id, "commands_used": 1}
            )

async def setup(bot: Bot) -> None:
    await bot.add_cog(Events(bot))