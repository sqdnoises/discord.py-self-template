import os
from dotenv import load_dotenv

import utils
import config

from logger import logging
from classes import Bot

load_dotenv()
logging.info("loaded environmental variables")

bot = Bot(command_prefix=utils.get_prefix, strip_after_prefix=True)

utils.show_terminal_size()

logging.info(f"starting {config.BOT_NAME}")
bot.run(os.getenv("TOKEN"))