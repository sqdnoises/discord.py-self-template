import os
from dotenv import load_dotenv

import utils

import logging
import discord
from classes import Bot

discord.utils.setup_logging()
logging.info("logging initiated")

load_dotenv()
logging.info("loaded environmental variables")

try:
    terminal = os.get_terminal_size()
except:
    logging.warning("could not detect terminal size")
else:
    logging.info(f"detected current terminal size: {terminal.columns}x{terminal.lines}")

bot = Bot(command_prefix=utils.get_prefix, strip_after_prefix=True)

logging.info("starting template bot")
bot.run(os.getenv("TOKEN"), log_handler=None)