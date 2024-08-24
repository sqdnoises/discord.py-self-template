"""
Class that contains views for the help slash command.
"""

import utils
import config
import utils.slash_help
from classes import Bot, Cog

import discord
from discord import app_commands
from discord.ext import commands

__all__ = (
    "SlashCommandHelpView",
    "SlashHelpView"
)

class SlashCommandHelpView(discord.ui.View):
    """View for the help of a single slash command"""

    def __init__(self, bot: Bot, interaction: discord.Interaction, category: Cog, items: int = config.HELP_PAGE_ITEMS, timeout: float | None = None) -> None:
        super().__init__(timeout=timeout)
        self.interaction = interaction
        self.bot = bot
        
        self.category = category
        self.items = items
        
        if category is None:
            self.category = self.bot.get_cog("Help")
    
    async def update_button(self) -> None:
        button: discord.ui.Button = self.children[0]
        button.label = button.label.format(category=self.category.qualified_name)
        button.emoji = self.category.emoji
    
    @discord.ui.button(emoji="❔", label="View help for {category}", style=discord.ButtonStyle.grey, custom_id="view_help")
    async def view_help(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        embed = await utils.slash_help.craft_slash_help_embed(self.bot, self.interaction, self.category, items=self.items)
        view = SlashHelpView(self.bot, self.interaction, self.category, self.items, self.timeout)
        await view.update_pages()
        await view.update_buttons()
        await view.update_categories()
        await interaction.response.edit_message(embed=embed, view=view)

class SlashHelpView(discord.ui.View):
    """View for the slash help command"""
    
    def __init__(self, bot: Bot, interaction: discord.Interaction, category: Cog, items: int = config.HELP_PAGE_ITEMS, timeout: float | None = None) -> None:
        super().__init__(timeout=timeout)

        self.interaction = interaction
        self.bot = bot
        self.category = category
        self.page = 1
        self.pages: list[list[app_commands.Command | commands.HybridCommand]] = []
        self.items = items
    
    async def update_pages(self) -> None:
        self.page = 1
        
        all_cmds = [
            command for command in self.bot.walk_commands()
            if self.bot.tree.get_cog(command) == self.category
        ] + [
            command for command in self.bot.tree.walk_commands()
            if self.bot.tree.get_cog(command) == self.category
        ]
        cmds = []
        def recurse(cmds_list: list[app_commands.Command, app_commands.Group, app_commands.AppCommandGroup]) -> None:
            for cmd in cmds_list:
                if isinstance(cmd, app_commands.Group):
                    recurse(cmd.commands)
                    continue
                
                cmds.append(cmd)
        recurse(all_cmds)
        
        self.pages = utils.paginate(cmds, self.items)
    
    async def update_buttons(self) -> None:
        buttons: list[discord.ui.Button] = [child for child in self.children if child.type == discord.ComponentType.button]
        if len(buttons) == 0:
            first = discord.ui.Button(emoji="⏪", style=discord.ButtonStyle.grey, custom_id="first")
            first.callback = self.first_page
            self.add_item(first)
            
            prev = discord.ui.Button(emoji="⬅️", style=discord.ButtonStyle.grey, custom_id="prev")
            prev.callback = self.previous_page
            self.add_item(prev)
            
            next = discord.ui.Button(emoji="➡️", style=discord.ButtonStyle.grey, custom_id="next")
            next.callback = self.next_page
            self.add_item(next)
            
            last = discord.ui.Button(emoji="⏩", style=discord.ButtonStyle.grey, custom_id="last")
            last.callback = self.last_page
            self.add_item(last)
            
            buttons: list[discord.ui.Button] = [child for child in self.children if child.type == discord.ComponentType.button]
        
        buttons[0].disabled = self.page == 1
        buttons[1].disabled = self.page == 1
        buttons[2].disabled = self.page == len(self.pages)
        buttons[3].disabled = self.page == len(self.pages)

        if all([button.disabled for button in buttons]):
            while len(buttons) > 0:
                button = buttons[0]
                self.remove_item(button)
                buttons.pop(0)

        for button in buttons:
            if button.disabled:
                button.style = discord.ButtonStyle.red
            else:
                button.style = discord.ButtonStyle.green
    
    async def update_categories(self) -> None:
        dropdown: discord.ui.Select = [child for child in self.children if child.type == discord.ComponentType.select][0]
        
        dropdown.options = []
        for cog in self.bot.cogs.values():
            cog: Cog
            
            embed = await utils.slash_help.craft_slash_help_embed(self.bot, self.interaction, cog, items=self.items)
            if embed:
                dropdown.options.append(discord.SelectOption(
                    label=cog.qualified_name,
                    value=cog.__class__.__name__,
                    description=cog.short_description,
                    emoji=cog.emoji
                ))
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.interaction.user.id:
            await interaction.response.send_message(
                content = "This is not your help menu.",
                ephemeral = True
            )
            return False
        return True

    async def first_page(self, interaction: discord.Interaction) -> None:
        self.page = 1
        embed = await utils.slash_help.craft_slash_help_embed(self.bot, self.interaction, self.category, self.page, self.items)
        await self.update_buttons()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def previous_page(self, interaction: discord.Interaction) -> None:
        self.page -= 1
        embed = await utils.slash_help.craft_slash_help_embed(self.bot, self.interaction, self.category, self.page, self.items)
        await self.update_buttons()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def next_page(self, interaction: discord.Interaction) -> None:
        self.page += 1
        embed = await utils.slash_help.craft_slash_help_embed(self.bot, self.interaction, self.category, self.page, self.items)
        await self.update_buttons()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def last_page(self, interaction: discord.Interaction) -> None:
        self.page = len(self.pages)
        embed = await utils.slash_help.craft_slash_help_embed(self.bot, self.interaction, self.category, self.page, self.items)
        await self.update_buttons()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.select(placeholder="Choose category...", min_values=1, max_values=1, custom_id="categories")
    async def categories_dropdown(self, interaction: discord.Interaction, select: discord.ui.Select) -> None:
        await interaction.response.defer()
        
        self.category = self.bot.get_cog(select.values[0])
        await self.update_pages()
        embed = await utils.slash_help.craft_slash_help_embed(self.bot, self.interaction, self.category, items=self.items)
        await self.update_buttons()
        await self.update_categories()
        await interaction.edit_original_response(embed=embed, view=self)