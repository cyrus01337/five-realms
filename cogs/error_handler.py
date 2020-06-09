"""
"""
from discord.ext import commands

import errors
# import utils


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        self.names = {}
        self.ignored = (
            commands.CommandNotFound,
        )

    @commands.Cog.listener()
    async def on_error(self, error):
        raise error

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = None
        error = getattr(error, "original", error)

        if isinstance(error, self.ignored):
            return

        if isinstance(error, errors.FiveRealmsError):
            embed = error.to_embed(self.bot)
        else:
            raise error
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
