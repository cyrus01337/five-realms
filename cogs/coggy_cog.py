"""
"""
from discord.ext import commands


class Cog(commands.Cog, name="Category"):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.id == self.bot.owner_id

    @commands.command()
    async def close(self, ctx):
        await self.bot.close()


def setup(bot):
    bot.add_cog(Cog(bot))
