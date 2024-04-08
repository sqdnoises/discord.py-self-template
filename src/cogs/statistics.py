import asyncio
import discord
from classes import Bot, Context
from discord.ext import commands

class Statistics(commands.Cog):
    """Statistics"""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    async def get_statistics(self, guild_id: int):
        prisma = self.bot.prisma
        
        statistics = await prisma.statistics.find_unique_or_raise(
            where={"guild_id": guild_id}
        )

        return statistics
    
    @commands.command(aliases=["stats"])
    async def statistics(self, ctx: Context):
        """Statistics of the bot"""
        
        await asyncio.sleep(1)
        
        stats = await self.get_statistics(ctx.guild.id)
        
        embed = discord.Embed(
            title = "Statistics",
            description = f"**Commands used: ** {stats.commands_used}",
            timestamp = discord.utils.utcnow(),
            color=discord.Color.orange()
        )
        
        await ctx.send(embed=embed)

async def setup(bot: Bot) -> None:
    await bot.add_cog(Statistics(bot))