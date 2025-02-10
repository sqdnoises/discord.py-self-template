import asyncio
from typing import (
    TYPE_CHECKING,
    Literal, Iterable
)

from ..        import utils
from ..classes import Bot, Cog, Context

import psutil
from ping3 import ping

from discord.ext import commands

class Utilities(Cog):
    """Essential tools like ping & statistics."""
    
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.emoji = "🔧"
        self.process = psutil.Process()
        self.short_description = "Essential tools"
    
    def get_latency_circle(self, latency: float | None) -> str:
        if latency is None:
            return "⚫"
        elif latency <= 0:
            return "⚪"
        elif latency <= 0.1:
            return "🟢"
        elif latency <= 0.35:
            return "🟡"
        else:
            return "🔴"
    
    async def measure_ping(self, domains: Iterable[str]) -> dict[str, float | Literal[False] | None]:
        """Measure the ping"""
        
        async def get_ping(domain: str) -> float | Literal[False] | None:
            return await self.run(ping, domain)
        
        pings = await asyncio.gather(*[get_ping(domain) for domain in domains])
        
        return {
            domain: ping  # False means error
            for domain, ping in zip(domains, pings)
        }
    
    @commands.command(aliases=["latency"])
    async def ping(self, ctx: Context) -> None:
        """Check the latency of the bot and the services being used"""
        
        def format_ping_line(name: str, latency: float | Literal[False] | None) -> str:
            if latency is None:
                value = f"{self.get_latency_circle(None)} Unreachable"
            elif latency is False:
                value = f"{self.get_latency_circle(None)} Error"
            else:
                ping_text = f"{round(latency*1000)}ms" if latency < 1000 else f"{latency:.2f}s"
                value = f"{self.get_latency_circle(latency)} {ping_text}"
            
            return f"**{name}:** `{value}`"
        
        # Create the text response
        response_lines = []
        
        domains = {
            "discord.com": "Discord"
        }
        
        pings = await self.measure_ping(domains)
        response_lines.append(format_ping_line(list(domains.values())[0], pings.pop(list(domains.keys())[0])))
        response_lines.append(format_ping_line("Discord WS Latency", self.bot.latency))
        
        for domain, ping in pings.items():
           response_lines.append(format_ping_line(domains[domain], ping))
        
        response_lines.append("-# **Pong!** 🏓")
        await ctx.reply("\n".join(response_lines), mention_author=False)
    
    @commands.command(aliases=["stats"])
    async def statistics(self, ctx: Context) -> None:
        """Statistics about the bot"""
        if TYPE_CHECKING and (
            self.bot.uptime is None
            or self.bot.user is None
        ):
            # to satisfy the typechecker
            return
        
        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_count = psutil.cpu_count()
        cpu_usage = self.process.cpu_percent() / (cpu_count or 1)
        
        # Create the text response
        response = (
            f"## 🌟 **{self.bot.user.display_name}'s Statistics**\n"
            f"**Serving:** `{len(self.bot.guilds):,} servers` & `{len(self.bot.users):,} users`\n"
            f"**Platform:** `{utils.detect_platform()}`\n"
            f"**Process:**  \n"
            f" - CPU: `{cpu_usage:.2f}%`\n"
            f" - Memory: `{round(memory_usage)} MiB`\n"
            f" - Uptime: up since <t:{int(self.bot.uptime.timestamp())}:R>"
        )
        
        await ctx.reply(response, mention_author=False)

async def setup(bot: Bot) -> None:
    await bot.add_cog(Utilities(bot))