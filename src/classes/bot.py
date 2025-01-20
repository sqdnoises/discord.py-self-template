import sys
import pkg_resources
from typing   import (
    TYPE_CHECKING,
    Literal
)
from datetime import datetime

import cogs
import utils
import config
from utils               import mprint
from logger              import logging
from termcolors          import *
from termcolors          import rgb
from classes.context     import Context

if TYPE_CHECKING:
    from classes.custom_types import (
        ContextT_co,
        PrefixType
    )

from prisma import Prisma

import discord
from discord.ext import commands

__all__ = (
    "Bot",
)

class Bot(commands.Bot):
    """The main bot class which handles everything, including handling of events, commands, interactions, cogs, extensions, etc. and the bot itself."""
    uptime: datetime | None
    prisma: Prisma
    
    def __init__(self, command_prefix: "PrefixType", *args, **kwargs) -> None:
        super().__init__(command_prefix=command_prefix, *args, **kwargs, help_command=commands.DefaultHelpCommand())
        self.uptime = None
        self.prisma = Prisma(auto_register=True)
    
    async def connect_db(self) -> None:
        await self.prisma.connect()
    
    async def disconnect_db(self) -> None:
        await self.prisma.disconnect()
    
    async def setup_hook(self) -> None:
        self.uptime = discord.utils.utcnow()
        
        mprint()
        mprint(f"{white}~{reset} {bold}{green}{config.BOT_NAME.upper()}{reset} {white}~{reset}")
        mprint(f"{bright_green}running on{reset} {yellow}python{reset} {blue}{sys.version.split()[0]}{reset}; {yellow}discord.py{reset} {blue}{pkg_resources.get_distribution('discord.py-self').version}{reset}")
        mprint()
        
        await self.connect_db()
        logging.info("connected to database ./database/database.db")
        
        loaded = []
        excluded = []
        
        exclude = config.COGS_EXCLUDE
        for module in utils.list_modules(cogs):
            if module in exclude or module.replace(cogs.__package__+".", "", 1) in exclude: # pyright: ignore[reportOptionalOperand]
                excluded.append(module + f" {rgb(49, 49, 49)}(excluded in config){reset}")
                continue
            
            try:
                await self.load_extension(module)
            
            except commands.NoEntryPointError:
                logging.warn(f"excluding `{module}` because there is no entry point (no 'setup' function found)")
                excluded.append(module + f" {rgb(49, 49, 49)}(no 'setup' function){reset}")
            
            except Exception as e:
                logging.critical(f"excluding `{module}` because there was an error while loading it (this may cause unintended behaviour)", exc_info=e)
                excluded.append(module + f" {rgb(49, 49, 49)}(error: {e.__class__.__name__}){reset}")
            
            else:
                loaded.append(module)
        
        loaded_paginated = utils.paginate(loaded, 3)
        excluded_paginated = utils.paginate(excluded, 2)
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
        
        if TYPE_CHECKING and self.user is None:
            return  # to satisfy the type checker
        
        logging.info("logged in successfully")
        logging.info(f"user: {self.user} ({self.user.id})")
    
    async def get_context(self, message: discord.Message, *, cls: type["ContextT_co"] = Context) -> "ContextT_co":
        """Get Context from a discord.Message"""
        return await super().get_context(message, cls=cls)
    
    def create_activity(
        self,
        name: str,
        type: Literal["playing", "streaming", "listening", "watching"] = "playing",
        *args,
        **kwargs
    ) -> discord.Activity | discord.Game | discord.Streaming:
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
