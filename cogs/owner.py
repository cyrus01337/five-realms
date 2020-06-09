"""

"""
import discord
from discord.ext import commands

import database
import utils
from enums import Emoji


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True

    def auto_complete(self, name):
        for cog in utils.get_cogs():
            if cog.startswith(name):
                return cog
        return None

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    async def cog_before_invoke(self, ctx):
        if ctx.command.name == "close":
            await ctx.message.add_reaction(Emoji.WHITE_HEAVY_CHECK_MARK)

    async def cog_after_invoke(self, ctx):
        if ctx.command_failed is False:
            await ctx.message.add_reaction(Emoji.WHITE_HEAVY_CHECK_MARK)

    @commands.command()
    async def clear(self, ctx, medium="screen"):
        medium = medium.lower()

        if medium == "screen":
            utils.clear_screen(self.bot)
        elif medium in ["database", "db"]:
            await database.clear()
        elif medium == "me":
            await database.remove(ctx.author.id)

    @commands.command()
    async def close(self, ctx):
        await self.bot.close()

    @commands.command(aliases=["load", "unload", "reload"])
    async def manipulate_extension(self, ctx, *extensions):
        extensions = map(str.lower, extensions)
        manipulated = ""
        to_manipulate = []
        function = getattr(self.bot, f"{ctx.invoked_with}_extension")

        for extension in extensions:
            if extension == "all":
                to_manipulate = utils.get_cogs()
                break
            is_duplicate = extension not in to_manipulate
            extension = self.auto_complete(extension)

            if extension is None:
                continue
            elif extension in utils.get_cogs() and is_duplicate:
                to_manipulate.append(extension)

        if len(to_manipulate) == 0:
            return

        for path in to_manipulate:
            function(f"cogs.{path}")
        manipulated = (", ").join(f"`{e}`" for e in to_manipulate)
        await ctx.send(f"{str.title(ctx.invoked_with)}ed {manipulated}")

    @commands.command()
    async def invite(self, ctx):
        url = discord.utils.oauth_url(
            self.bot.user.id,
            permissions=self.bot.invite_perms,
            guild=ctx.guild
        )
        embed = utils.embed(self.bot, title="Invite", desc=f"[URL]({url})")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Owner(bot))
