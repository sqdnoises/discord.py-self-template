from ..classes import Bot, Cog, Context

import discord
from   discord     import app_commands
from   discord.ext import commands

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
    
    # just in case i ever need slash command autocomplete
    async def search_autocomplete_example(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        stuff: list[str] = []
        
        if current:
            search_results = [
                app_commands.Choice(name=thing, value=thing) for thing in stuff
                if current.lower() in thing.lower()
                or thing.lower() in current.lower()
            ]
        
        else:
            search_results = [app_commands.Choice(name=thing, value=thing) for thing in stuff]
        
        return search_results[:25]

async def setup(bot: Bot) -> None:
    await bot.add_cog(Example(bot))