"""
Help Command-related utilities
"""

from ..        import utils
from .         import colors       as colorutils
from ..        import config
from ..classes import Cog, Context

import discord
from discord.ext import commands

__all__ = (
    "craft_usage",
    "craft_aliases",
    "craft_hidden",
    "craft_help_embed"
)

def craft_usage(ctx: Context, command: commands.Command) -> str:
    """Create usage for a command"""
    return f"{ctx.clean_prefix}{command.qualified_name} {command.signature}"

def craft_aliases(ctx: Context, command: commands.Command) -> str:
    """Create aliases text for a command"""
    return f"***aliases**: {', '.join(f'{ctx.prefix}{alias}' for alias in command.aliases)}*" if command.aliases else ""

def craft_hidden(ctx: Context, command: commands.Command) -> str:
    """Create hidden command text for a command"""
    return f"Oh what's that? Looks like you found a *hidden* command!" if command.hidden else ""

async def craft_help_embed(ctx: Context, category_or_command: Cog | commands.Command, page: int = 1, items: int = config.HELP_PAGE_ITEMS) -> discord.Embed:
    """Create a help embed for a category or command"""
    bot = ctx.bot
    
    category: Cog = None
    command: commands.Command = None
    if isinstance(category_or_command, Cog):
        category = category_or_command
    else:
        command = category_or_command
    
    if category:
        if category.hidden:
            return None
        
        embed = discord.Embed(
            title = f"{category.emoji} Category `{category.qualified_name}`",
            description = category.description.format(
                prefix=ctx.prefix,
                clean_prefix=ctx.clean_prefix,
                guild=ctx.guild,
                author=ctx.author
            ),
            color = colorutils.get_random_dominant_color(await bot.user.display_avatar.read()),
            timestamp = discord.utils.utcnow()
        )

        cmds = []
        for command in bot.commands:
            try:
                if command.cog == category and await command.can_run(ctx) and not command.hidden:
                    cmds.append(command)
            
            except commands.CheckFailure:
                continue

        cmds.sort(key=lambda command: command.qualified_name)
        paginated_commands: list[list[commands.Command]] = utils.paginate(cmds, items)
        pages = len(paginated_commands)
        cmds: list[commands.Command] = paginated_commands[page-1:page]
        
        embed.set_footer(
            text = f"Requested by {ctx.author.display_name} | Page {page}/{pages}",
            icon_url = ctx.author.display_avatar
        )
        
        if len(cmds) == 0:
            return None
        cmds = cmds[0]
        
        for command in cmds:
            embed.add_field(
                name = "✨ " + craft_usage(ctx, command),
                value = f"{utils.code(command.help or 'No description provided.')}\n"
                        f"{craft_aliases(ctx, command)}",
                inline = False
            )

        embed.set_thumbnail(
            url = bot.user.display_avatar
        )
    
    else:
        try:
            if not await command.can_run(ctx):
                return None
        except commands.MissingPermissions:
            return None
        
        embed = discord.Embed(
            title = f"✨ Command `{command.qualified_name}`",
            description = f"Viewing help page for command `{ctx.prefix}{command.qualified_name}`\n"
                          f"Category: **{command.cog_name or 'N/A'}** {'(hidden)' if command.cog and command.cog.hidden else ''}\n"
                          f"\n"
                          f"{craft_hidden(ctx, command)}",
            color = colorutils.get_random_dominant_color(await bot.user.display_avatar.read()),
            timestamp = discord.utils.utcnow()
        )
        
        embed.set_footer(
            text = f"Requested by {ctx.author.display_name} | Viewing command help",
            icon_url = ctx.author.display_avatar
        )
        
        embed.add_field(
            name = "Usage: " + craft_usage(ctx, command),
            value = f"{utils.code(command.help or 'No description provided.')}\n"
                    f"{craft_aliases(ctx, command)}",
            inline = False
        )
        
        embed.set_thumbnail(
            url = bot.user.display_avatar
        )
    
    return embed