import checks
import utils.help
import views.help
import utils.slash_help
import views.slash_help
from classes import Bot, Cog, Context

import discord
from discord import app_commands
from discord.ext import commands

class Help(Cog):
    """
    Welcome to **{guild.name}**, {user.mention}!
    
    Use the dropdown at the bottom to navigate through different categories of commands.
    For more info on a command, run `{clean_prefix}help [command]`.
    """

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.emoji = "❓"
        self.short_description = "Getting help on the bot"
        
    @commands.command(aliases=["h", "cmds", "commands"])
    async def help(self, ctx: Context, *, command: str = None) -> None:
        """Shows this help page"""
        bot = self.bot
        
        if command == None:
            embed = await utils.help.craft_help_embed(ctx, self)
            if embed is None:
                return await ctx.send("That's strange, the help command category could not be found. Please contact the developer.")
            
            view = views.help.HelpView(ctx, self)
            await view.update_pages()
            await view.update_buttons()
            await view.update_categories()
        
        else:
            cmd = bot.get_command(command)
            if not cmd:
                return await ctx.send(f"Command `{command}` not found.")
            
            embed = await utils.help.craft_help_embed(ctx, cmd)
            if not embed:
                return await ctx.send(f"Command `{command}` not found.")
            
            view = views.help.CommandHelpView(ctx, cmd.cog)
            await view.update_button()
            
            if cmd.cog and cmd.cog.hidden and not checks._is_admin(ctx):
                view = None
        
        await ctx.send(embed=embed, view=view)
    
    @app_commands.command(name="help", extras={"aliases": ["cmds", "commands"]})
    @app_commands.describe(command="The command to get help on")
    async def slash_help(self, interaction: discord.Interaction, command: str = None) -> None:
        """Shows slash commands help page"""
        bot = self.bot
        
        if command == None:
            embed = await utils.slash_help.craft_slash_help_embed(bot, interaction, self)
            if embed is None:
                return await interaction.response.send_message("That's strange, the help command category could not be found. Please contact the developer.")
            
            view = views.slash_help.SlashHelpView(bot, interaction, self)
            await view.update_pages()
            await view.update_buttons()
            await view.update_categories()
        
        else:
            cmd = bot.tree.get_command(command)
            if not cmd:
                cmd = bot.get_command(command)
                if not isinstance(command, commands.HybridCommand):
                    return await interaction.response.send_message(f"Command `{command}` not found.")
            
            embed = await utils.slash_help.craft_slash_help_embed(bot, interaction, cmd)
            if not embed:
                return await interaction.response.send_message(f"Command `{command}` not found.")
            
            cog = self.bot.tree.get_cog(cmd)
            
            view = views.slash_help.SlashCommandHelpView(bot, interaction, cog)
            await view.update_button()
            
            if cog and cog.hidden and not checks._is_admin(interaction):
                view = None
        
        await interaction.response.send_message(embed=embed, view=view)
    
    @slash_help.autocomplete("command")
    async def slash_help_command_search_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        bot = self.bot
        cmds: dict[str, list[str]] = {}
        
        for command in bot.tree.get_commands():
            if command.qualified_name not in cmds: cmds[command.qualified_name]   =   [command.qualified_name]
            else:                                  cmds[command.qualified_name].append(command.qualified_name)
            
            if isinstance(command, commands.hybrid.HybridAppCommand):
                for cmd in bot.walk_commands():
                    if isinstance(cmd, commands.HybridCommand) and command.qualified_name == cmd.qualified_name:
                        command = cmd
                        break
                
                else:
                    raise commands.CommandNotFound(f"commands.HybridCommand with the name `{command.qualified_name}` not found in bot.walk_commands()")
                
                aliases = command.aliases
            
            else:
                aliases = command.extras.get("aliases", [])
            
            for alias in aliases:
                if alias not in cmds: cmds[alias]   =   [command.qualified_name]
                else:                 cmds[alias].append(command.qualified_name)
                
        if current:
            search_results = [
                alias for alias in cmds
                if current.lower() in alias.lower()
                or alias.lower() in current.lower()
            ]
        
        else:
            search_results = []
            for cmds_list in cmds.values():
                for command in cmds_list:
                    if command not in search_results:
                        search_results.append(command)
        
        final_search_results = []
        for alias in search_results:
            for command in cmds[alias]:
                if command not in final_search_results:
                    final_search_results.append(command)
        
        return [app_commands.Choice(name=command, value=command) for command in final_search_results][:25]

async def setup(bot: Bot) -> None:
    await bot.add_cog(Help(bot))