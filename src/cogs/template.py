from ..classes import Bot, Cog, Context

from discord.ext import commands

class Example(Cog):
    """Example cog."""
    
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.emoji = "🥺"
        self.short_description = "Example cog"
    
    @commands.command()
    async def example(self, ctx: Context) -> None:
        """Example command"""
        await ctx.send("Hello world!")

async def setup(bot: Bot) -> None:
    await bot.add_cog(Example(bot))