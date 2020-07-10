"""

"""
from discord.ext import commands

# import checks
# from enums import Class


# command_attrs=dict(hidden=True)
class TestingCog(commands.Cog, name="Testing"):
    def __init__(self, bot):
        self.bot = bot
        # self.hidden = True

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    async def default(self, ctx):
        await ctx.send("Working!")

    @commands.group(invoke_without_command=True)
    async def test(self, ctx):
        await self.default(ctx)

    @test.group(name="group", invoke_without_command=True)
    async def test_group(self, ctx):
        await self.default(ctx)

    @test.command(name="grope")
    async def test_grope(self, ctx):
        await self.default(ctx)

    @test_group.group(name="sub", invoke_without_command=True)
    async def test_group_sub(self, ctx):
        await self.default(ctx)

    @test_group_sub.command(name="inner")
    async def test_group_sub_inner(self, ctx):
        await self.default(ctx)

    @test_group_sub.command(name="other")
    async def test_group_sub_other(self, ctx):
        await self.default(ctx)


def setup(bot):
    bot.add_cog(TestingCog(bot))
