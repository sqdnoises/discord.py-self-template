"""
Bot-related utilities.
"""

import config
import objects

import aiohttp
import discord
from discord.ext import commands

__all__ = (
    "get_prefix",
    "get_raw_content_data"
)

async def get_prefix(bot: objects.MockBot, message: discord.Message):
    """Get the prefix for the bot"""
    prisma = bot.prisma
    
    guild = await prisma.configuration.find_unique(where={"guild_id": message.guild.id})
    
    if guild:
        prefix = guild.prefix
    
    else:
        await prisma.configuration.create(data={"guild_id": message.guild.id, "prefix": config.DEFAULT_PREFIX})
        prefix = config.DEFAULT_PREFIX
    
    return commands.when_mentioned_or(prefix)(bot, message)

async def get_raw_content_data(url: str, *args, **kwargs):
    """Get raw content like files and media as bytes"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=True if url.lower().startswith("https") else False, *args, **kwargs) as response:
            return await response.content.read()