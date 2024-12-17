from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.bot import Bot
    from classes.cog import Cog

from discord import app_commands
from discord.ext import commands

__all__ = (
    "CommandTree",
)

class CommandTree(app_commands.CommandTree):
    """Represents a container that holds application command information."""
    bot: "Bot"
    
    def __init__(
        self,
        client: "Bot",
        *,
        fallback_to_global = True
    ) -> None:
        super().__init__(client=client, fallback_to_global=fallback_to_global)
        self.bot = client
    
    def get_cog(
        self,
        command: app_commands.Command | commands.hybrid.HybridAppCommand
    ) -> "Cog | commands.Cog | None":
        """Get the cog that contains the app or hybrid command."""
        
        for cog in self.bot.cogs.values():
            if command in cog.get_app_commands():
                return cog
            
            if isinstance(command, commands.hybrid.HybridAppCommand):
                cmds = [cmd.qualified_name for cmd in cog.get_commands() if isinstance(cmd, commands.HybridCommand)]
                if command.qualified_name in cmds:
                    return cog
            
            if isinstance(command, commands.HybridCommand):
                if command in cog.get_commands():
                    return cog
        
        return None