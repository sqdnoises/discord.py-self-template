"""
## `discord.py` bot template
a discord.py bot template that I use for my bots.

Copyright (c) 2023-present SqdNoises
Licensed under the MIT License
For more information, please check the provided LICENSE file.
"""

import os
from dotenv import load_dotenv

import config
import utils.bot 
import utils.console
from logger import logging
from classes import Bot

logging.info("initialising")

utils.console.show_versions()

load_dotenv()
logging.info("loaded environmental variables")

bot = Bot(command_prefix=utils.bot.get_prefix, strip_after_prefix=True, help_command=None)

utils.console.show_terminal_size()

def start():
    """Start the bot"""
    logging.info(f"starting {config.BOT_NAME}")
    token = os.getenv("TOKEN")
    
    if token:
        bot.run(token)
    else:
        logging.critical("environment variable 'TOKEN' not found. are you sure you have setup your `.env` file correctly?")

if __name__ == "__main__":
    start()
    logging.critical("bot process exited")