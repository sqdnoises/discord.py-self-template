from logger  import logging
from classes import Bot, Context, Cog

from discord.ext import commands

class Test(Cog):
    """Test cog."""
    
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.emoji = "🥺"
        self.short_description = "Test cog"
        self.hidden = True
    
    @commands.command(hidden=True)
    async def test(self, ctx: Context) -> None:
        """Test command"""
        logging.log_level = 5
        logging.info("INFO example")
        logging.warn("WARNING example")
        logging.error("ERROR example")
        logging.critical("CRITICAL example")
        logging.debug("DEBUG example")
        logging.log_level = 4
                
        await ctx.send("Hello world!")

async def setup(bot: Bot) -> None:
    await bot.add_cog(Test(bot))