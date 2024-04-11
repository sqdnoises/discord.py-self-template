"""
Objects that may be used to mock a particular class or feature
"""

from dataclasses import dataclass

from prisma import Prisma
from discord.ext import commands

__all__ = (
    "MockBot",
    "Statistics",
    "Configuration"
)

class MockBot(commands.Bot):
    prisma: Prisma

@dataclass
class Statistics:
    commands_used: int

@dataclass
class Configuration:
    prefix: str
    no_permissions_message: str