"""
## `discord.py` bot template
a discord.py bot template that I use for my bots.

Copyright (c) 2023-present SqdNoises
Licensed under the MIT License
For more information, please check the provided LICENSE file.
"""

import os
import logging as logg
from datetime import datetime

import config
import utils.bot 
import utils.console
from logger  import logging
from classes import Bot

import discord
from dotenv import load_dotenv

logging.info("initialising")

if config.SAVE_DISCORD_LOGS:
    os.makedirs(logging.logs_folder or "logs", exist_ok=True)
    filepath = logging.log_file or os.path.join(logging.logs_folder or "logs", f"{logging.name} {datetime.now().strftime(config.LOG_FILE_NAME_TIME_FORMAT)}.log")
    discord.utils.setup_logging(
        handler = logg.FileHandler(filepath),
        formatter = logg.Formatter("{asctime} {levelname:<8} {name} > {message}", config.LOGGER_TIME_FORMAT, style="{"),
        root = False
    )
    logging.debug("discord.py file handler set up")

if config.DEBUG:
    logging.log_level = 5
    logging.debug("Houston, we have a code GRAY (DEBUG)")
    logging.debug("debug mode enabled")

utils.console.print_versions()

load_dotenv()
logging.info("loaded environment variables")

bot = Bot(
    command_prefix = utils.bot.get_prefix,
    strip_after_prefix = True,
    status = discord.Status.idle,
    activity = discord.Activity(type=discord.ActivityType.watching, name="the world burn")
)

utils.console.print_terminal_size()

def start(*args, **kwargs):
    """Start the bot"""
    logging.info(f"starting {config.BOT_NAME}")
    
    if not config.ADMINS:
        logging.critical("no admins found in the config file, please add atleast one user ID")
        return
    
    token = os.getenv("TOKEN")
    
    if token:
        bot.run(token, *args, **kwargs)
    else:
        logging.critical("environment variable 'TOKEN' not found. are you sure you have setup your `.env` file correctly?")

if __name__ == "__main__":
    start()
    logging.critical("bot process exited")