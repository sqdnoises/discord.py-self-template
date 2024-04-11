"""
## `discord.py` bot template
A template Discord Bot made in `discord.py`.

Copyright (c) SqdNoises 2024-present
Licensed under the MIT License
https://github.com/sqdnoises/discord.py-bot-template
"""

import os
import sys
import pkg_resources
from dotenv import load_dotenv

from .        import config
from .utils   import bot     as botutils 
from .utils   import console 
from .logger  import logging
from .classes import Bot

logging.info(f"python {sys.version}")
logging.info(f"discord.py {pkg_resources.get_distribution('discord.py').version}")

load_dotenv()
logging.info("loaded environmental variables")

bot = Bot(command_prefix=botutils.get_prefix, strip_after_prefix=True, help_command=None)

console.show_terminal_size()

def start():
    """Start the bot"""
    logging.info(f"starting {config.BOT_NAME}")
    bot.run(os.getenv("TOKEN"))

if __name__ == "__main__":
    start()