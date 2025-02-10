import sys
import logging       as logg
import pkg_resources
from typing   import TYPE_CHECKING
from datetime import datetime

from ..            import cogs
from ..            import utils
from ..            import config
from ..utils       import mprint
from ..logger      import logging
from ..termcolors  import *
from ..termcolors  import rgb

from .context import Context

if TYPE_CHECKING:
    from .custom_types import (
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
    uptime: datetime | None
    prisma: Prisma
    
    def __init__(self, command_prefix: "PrefixType", *args, **kwargs) -> None:
        super().__init__(command_prefix=command_prefix, *args, **kwargs, help_command=commands.DefaultHelpCommand())
        self.uptime = None
        self.prisma = Prisma(auto_register=True)
    
    async def connect_db(self) -> None:
        if self.prisma.is_connected():
            logging.warn("tried to connect to database while already connected")
            return
        
        await self.prisma.connect()
        logging.info(f"connected to database {config.DATABASE_LOCATION}")
    
    async def disconnect_db(self) -> None:
        if not self.prisma.is_connected():
            logging.warn("tried to disconnect from database while already disconnected")
            return
        
        await self.prisma.disconnect()
        logging.info("disconnected from database")
    
    async def enable_wal_mode(self) -> None:
        try:
            await self.prisma.execute_raw("PRAGMA journal_mode=WAL;")
            print("SQLite3 journal mode set to WAL.")
        except Exception as e:
            print(f"Error setting WAL mode: {e}")
    
    async def _load_all_cogs(self) -> None:
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
    
    async def setup_hook(self) -> None:
        self.uptime = discord.utils.utcnow()
        
        mprint()
        mprint(f"{white}~{reset} {bold}{green}{config.BOT_NAME.upper()}{reset} {white}~{reset}")
        mprint(f"{bright_green}running on{reset} {yellow}python{reset} {blue}{sys.version.split()[0]}{reset}; {yellow}discord.py{reset} {blue}{pkg_resources.get_distribution('discord.py').version}{reset}")
        mprint()
        
        await self.connect_db()
        await self._load_all_cogs()
        
        if TYPE_CHECKING and self.user is None:
            return  # to satisfy the type checker
        
        logging.info(f"commands loaded: {len(self.commands)}")
        
        logging.info("logged in successfully")
        logging.info(f"user: {self.user} ({self.user.id})")
    
    async def close(self, *, abandon: bool = False) -> None:
        """Disconnect from the database, close the bot, flush stdout & stderr and shutdown loggers"""
        # Disconnect from the database
        await self.disconnect_db()
        
        # Close the bot
        await super().close()
        
        # Flush stdout & stderr
        sys.stdout.flush()
        sys.stderr.flush()
        
        # Shutdown loggers
        logging.critical("bot process exited" if not abandon else "bot process exited (abandoned)")
        logg.shutdown()
        logging.close()
        
        if abandon:
            print()
    
    async def get_context(self, message: discord.Message, *, cls: type["ContextT_co"] = Context) -> "ContextT_co":
        """Get Context from a discord.Message"""
        return await super().get_context(message, cls=cls)