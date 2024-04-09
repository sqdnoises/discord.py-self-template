import time
import asyncio

import objects
from classes import Bot, Context

import discord
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

    async def get_all_statistics(self):
        prisma = self.bot.prisma
        
        statistics = await prisma.statistics.find_many()
        stats = {
            "commands_used": sum([stat.commands_used for stat in statistics])
        }
        
        return objects.Statistics(**stats)
    
    async def measure_ping(self, ctx: Context, message: str = "Ping?"):
        """Measure the ping"""
        start = time.monotonic()
        msg = await ctx.send(message)
        end = time.monotonic()

        return msg, end - start
    
    @commands.command(aliases=["latency"])
    async def ping(self, ctx: Context):
        """Check the latency of the bot"""
        bot = self.bot
        msg, msg_latency = await self.measure_ping(ctx)
        await msg.edit(content=f"Pong! 🏓 (took `{round(msg_latency * 1000)}ms`, ws: `{round(bot.latency * 1000)}ms`)")
    
    @commands.command(aliases=["stats"])
    async def statistics(self, ctx: Context):
        """Statistics of the bot"""
        bot = self.bot
        
        stats = await self.get_statistics(ctx.guild.id)
        all_stats = await self.get_all_statistics()
        
        embed = discord.Embed(
            title = f"🌟 {ctx.me.display_name} Statistics",
            timestamp = discord.utils.utcnow(),
            color=discord.Color.blurple()
        )
        
        embed.add_field(
            name = "Servers",
            value = f"`{len(bot.guilds)}`"
        )
        
        embed.add_field(
            name = "Users",
            value = f"`{len(bot.users)}`"
        )
        
        embed.add_field(
            name = "Commands used",
            value = f"`{stats.commands_used}` (server)\n"
                    f"`{all_stats.commands_used}` (total)"
        )
        
        embed.add_field(
            name = "Uptime",
            value = f"up since <t:{int(bot.uptime.timestamp())}:R>"
        )
        
        msg, msg_latency = await self.measure_ping(ctx)
        
        embed.add_field(
            name = "Latency",
            value = f"`{round(msg_latency * 1000)}ms` (message)\n"
                    f"`{round(bot.latency * 1000)}ms` (websocket)"
        )
        
        embed.set_footer(
            text = f"Requested by {ctx.author.display_name}",
            icon_url = ctx.author.display_avatar
        )
        
        embed.set_thumbnail(
            url = bot.user.display_avatar
        )
        
        await msg.edit(content="Pong! 🏓", embed=embed)
        await asyncio.sleep(3)
        await msg.edit(content="")

async def setup(bot: Bot) -> None:
    await bot.add_cog(Statistics(bot))