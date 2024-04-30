"""
Console-related utilities.
"""

import os
import sys
import pkg_resources
from logger import logging

__all__ = (
    "show_terminal_size",
)

def show_versions():
    logging.info(f"python {sys.version}")
    logging.info(f"discord.py {pkg_resources.get_distribution('discord.py').version}")

def show_terminal_size():
    """Log the terminal size to console"""
    
    try:
        terminal = os.get_terminal_size()
    except:
        logging.warn("could not detect terminal size")
    else:
        logging.info(f"detected current terminal size: {terminal.columns}x{terminal.lines}")