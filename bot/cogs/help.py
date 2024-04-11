from ..classes    import Bot, Cog, Context
from ..utils.help import *
from ..views.help import HelpView

from discord.ext import commands

class Help(Cog):
    """
    Use the dropdown at the bottom to navigate through different categories of commands.
    
    For more info on a command, run `{clean_prefix}help [command]`.
    """

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.emoji = "❓"
        self.short_description = "Getting help on the bot"
    
    @commands.command(aliases=["h", "commands"])
    async def help(self, ctx: Context, command: str = None):
        """Shows this help page"""
        bot = self.bot
        
        if command == None:
            embed = await craft_help_embed(ctx, self)
            if embed is None:
                return await ctx.send("That's strange, the help command could not be found. Please contact the developer.")
            
            view = HelpView(ctx, self)
            await view.update_pages()
            await view.update_buttons()
            await view.update_categories()
        
        else:
            cmd = bot.get_command(command)
            if not cmd:
                return await ctx.send(f"Command `{command}` not found.")
            
            embed = await craft_help_embed(ctx, cmd)
            if not embed:
                return await ctx.send(f"Command `{command}` not found.")
            
            view = None
        
        await ctx.send(embed=embed, view=view)

async def setup(bot: Bot) -> None:
    await bot.add_cog(Help(bot))