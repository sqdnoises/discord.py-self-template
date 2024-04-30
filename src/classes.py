"""
Classes that will be used in the bot replacing the default `discord.py` ones.
"""

import sys
import pkg_resources
from typing import Optional, Literal
from datetime import datetime

import cogs
import utils
import config
from utils import mprint
from logger import logging
from termcolors import *
from termcolors import rgb

import discord
from prisma import Prisma
from discord import app_commands
from discord.ext import commands

__all__ = (
    "Context",
    "Bot",
    "Cog"
)

class Context(commands.Context):
    """Utility class for commands that is used to easily interact with commands."""
    bot: "Bot"
    
    def __init__(self, *args, **kwargs) -> None: # initialize the class
        super().__init__(*args, **kwargs)
        self.voice: Optional[discord.VoiceState] = self.author.voice
        self.cleaned_up_code = utils.cleanup_code(self.message.content)
        self.output: bool = True # for exec
    
    async def react(self, emoji: discord.Emoji) -> discord.Reaction:
        """Add reaction to a message"""
        return await self.message.add_reaction(emoji)
    
    def create_board(self, title: str = None, description: str = None, url: str = None, timestamp: datetime = None) -> discord.Embed:
        """Return a discord.Embed"""
        return discord.Embed(
            title=title,
            description=description,
            url=url,
            color=discord.Color.dark_embed(), # Dark Gray Embed Background
            timestamp=timestamp
        )

    async def board(self, title: str = None, description: str = None, url: str = None, timestamp: datetime = None, reply: bool = False) -> discord.Message:
        """Send a board message"""
        board = self.create_board(title, description, url, timestamp)
        if reply:
            return await self.reply(embed=board)
        else:
            return await self.send(embed=board)
    
    async def yes(self) -> discord.Message:          return await self.react("✅")
    async def tick(self) -> discord.Message:         return await self.react("✅")
    async def check(self) -> discord.Message:        return await self.react("✅")
    async def green(self) -> discord.Message:        return await self.react("✅")
    async def success(self) -> discord.Message:      return await self.react("✅")

    async def x(self) -> discord.Message:            return await self.react("❌")
    async def no(self) -> discord.Message:           return await self.react("❌")
    async def red(self) -> discord.Message:          return await self.react("❌")
    async def fail(self) -> discord.Message:         return await self.react("❌")
    async def cross(self) -> discord.Message:        return await self.react("❌")
    async def failure(self) -> discord.Message:      return await self.react("❌")
    async def unsuccessful(self) -> discord.Message: return await self.react("❌")

class CommandTree(app_commands.CommandTree):
    """Represents a container that holds application command information."""
    
    def __init__(self, client: "Bot", *, fallback_to_global=True) -> None:
        super().__init__(client=client, fallback_to_global=fallback_to_global)
        # edit the command tree
        self.bot = client
    
    def get_cog(self, command: app_commands.Command | commands.hybrid.HybridAppCommand) -> "Cog | None":
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

class Bot(commands.Bot):
    """The main bot class which handles everything, including handling of events, database, commands, interactions and the bot itself."""
    tree: CommandTree
    
    def __init__(
        self,
        command_prefix: str,
        *args,
        intents: discord.Intents = discord.Intents.all(),
        tree_cls: app_commands.CommandTree = CommandTree,
        **kwargs
    ) -> None: # initialize the class
        super().__init__(command_prefix=command_prefix, intents=intents, tree_cls=tree_cls, *args, **kwargs)
        # edit the bot
        self.uptime: datetime = None
        self.prisma = Prisma()
        self.log_channel_id: int = config.LOG_CHANNEL
        self.log_channel: discord.TextChannel = None

    async def connect_db(self) -> None:
        await self.prisma.connect()
    
    async def disconnect_db(self) -> None:
        await self.prisma.disconnect()
    
    async def setup_hook(self) -> None:
        self.uptime = discord.utils.utcnow()
        
        mprint()
        mprint(f"{white}~{reset} {bold}{green}{config.BOT_NAME.upper()}{reset} {white}~{reset}")
        mprint(f"{bright_green}running on{reset} {yellow}python{reset} {blue}{sys.version.split()[0]}{reset}; {yellow}discord.py{reset} {blue}{pkg_resources.get_distribution('discord.py').version}{reset}")
        mprint()
        
        loaded = []
        excluded = []
        
        exclude = config.COGS_EXCLUDE
        for module in utils.list_modules(cogs):
            if module in exclude or module.replace(cogs.__package__+".", "", 1) in exclude:
                excluded.append(module)
                continue
            
            loaded.append(module)
            await self.load_extension(module)
        
        loaded_paginated = utils.paginate(loaded, 3)
        excluded_paginated = utils.paginate(excluded, 3)
        prefix_length = len(utils.strip_color(logging._prefix_handler("info")))
        
        loaded_str = f"the following cogs have been {underline}loaded{reset}:\n"
        for x in loaded_paginated:
            loaded_str += (" "*prefix_length)+ f"{', '.join(x)}\n"
        
        excluded_str = f"the following cogs have been {underline}excluded{reset}:\n"
        for x in excluded_paginated:
            excluded_str += (" "*prefix_length)+ f"{', '.join(x)}\n"
        
        logging.info(loaded_str.strip())
        logging.info(excluded_str.strip())
        
        logging.info(f"commands loaded: {len(self.commands)}")
        
        logging.info("logged in successfully")
        logging.info(f"user: {self.user} ({self.user.id})")
        
        logging.info(f"invite: https://discord.com/oauth2/authorize?client_id={self.user.id}&permissions=8&scope=bot+applications.commands")
                
        await self.connect_db()
        logging.info("connected to database ./database/database.db")
    
    async def get_context(self, message: discord.Message, *, cls: commands.Context = Context) -> Context:
        """Get Context from a discord.Message"""
        return await super().get_context(message, cls=cls)
    
    def create_activity(self, name: str, type: Literal["playing", "streaming", "listening", "watching"] = "playing", *args, **kwargs) -> discord.Activity:
        """Create an activity for a given type"""

        match type:
            case "playing":
                return discord.Game(name=name, *args, **kwargs)
            case "streaming":
                return discord.Streaming(name=name, *args, **kwargs)
            case "listening":
                return discord.Activity(type=discord.ActivityType.listening, name=name, *args, **kwargs)
            case "watching":
                return discord.Activity(type=discord.ActivityType.watching, name=name, *args, **kwargs)

class Cog(commands.Cog):
    bot: Bot
    emoji: str = None
    hidden: bool = False
    short_description: str | None = None