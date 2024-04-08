import config
from classes import Bot, Context
from discord.ext import commands

class Admin(commands.Cog):
    """Server management commands"""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    async def update_prefix(self, guild_id: int, new_prefix: str) -> None:
        prisma = self.bot.prisma
        
        prisma.prefixes.update(
            data = {"prefix": new_prefix},
            where = {"guild_id": guild_id}
        )
    
    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx: Context, *, new_prefix: str | None = None):
        """Show or change the prefix"""
        
        if new_prefix is None:
            await ctx.send(f"Current prefix: `{ctx.prefix}.`")
        
        elif new_prefix == "default":
            await self.update_prefix(ctx.guild.id, config.DEFAULT_PREFIX)
            await ctx.send(f"Prefix changed to `{config.DEFAULT_PREFIX}`.")
        
        elif new_prefix == ctx.prefix:
            await ctx.send("The current prefix is already set to that.")
        
        else:
            await self.update_prefix(ctx.guild.id, new_prefix)
            await ctx.send(f"Prefix changed to `{new_prefix}`.")

async def setup(bot: Bot) -> None:
    await bot.add_cog(Admin(bot))