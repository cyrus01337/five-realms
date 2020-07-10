"""

"""
import asyncio
# import random
import time

import discord
from discord.ext import commands

import checks
import constants
# import database
import utils
from enums import Class
from enums import Emoji
from enums import Race
from enums import Realm
from objects import Field


class FiveRealmsCog(commands.Cog, name="RPG"):
    def __init__(self, bot):
        self.bot = bot
        self.DEFAULT_PARAMS = {
            "level": 1,
            "exp": 0,
            "class_type": Class.none.name
        }

    def check(self, author_id, message, iterable):
        def predicate(reaction, user):
            return (user.id == author_id
                    and message.id == reaction.message.id
                    and str(reaction.emoji) in iterable)
        return predicate

    async def wait_for(self, message, reactions, timeout,
                       title=None, desc=None, fields=None, enums=None,
                       author_id=None):
        ret = []
        author_id = author_id or message.author.id
        embed = utils.embed(self.bot, title=title,
                            desc=desc, fields=fields)

        if isinstance(message, discord.abc.Messageable):
            message = await message.send(embed=embed)
            ret.append(message)
        elif isinstance(message, discord.Message):
            await message.edit(embed=embed)
        kwargs = dict(check=self.check(author_id, message, reactions),
                      timeout=timeout)

        for emoji in reactions:
            await message.add_reaction(emoji)

        try:
            received, _ = await self.bot.wait_for("reaction_add", **kwargs)
        except asyncio.TimeoutError as e:
            await message.clear_reactions()
            raise e
        else:
            received = str(received)
            ret.append(received)

            if enums is not None:
                for enum in enums:
                    if received == enum.value.emoji:
                        ret.append(enum)
                        break
        if len(ret) == 1:
            ret = ret[0]
        return ret

    @checks.confirm_existence(exists=False)
    @commands.command()
    async def register(self, ctx):
        """
        Create your character, start your adventure!
        """
        player_realm = None
        player_race = None
        races = None
        user_id = ctx.author.id
        fields = []
        reactions = []
        realms = Realm.all()

        for realm in realms:
            emoji = realm.value.emoji
            field = Field(f"{emoji} {realm.name}", realm.value.desc)
            fields.append(field)
            reactions.append(emoji)

        embed = utils.embed(
            self.bot,
            desc=("Welcome to the character registration! What realm would "
                  "you like to be in? Take your time to think on it."),
            fields=fields
        )
        message = await ctx.send(embed=embed)

        for reaction in reactions:
            await message.add_reaction(reaction)

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add",
                check=self.check(user_id, message, reactions),
                timeout=120.0
            )
        except asyncio.TimeoutError:
            return await message.clear_reactions()
        else:
            for realm in realms:
                if str(reaction.emoji) == realm.value.emoji:
                    player_realm = realm
                    break

        fields.clear()
        reactions.clear()
        races = Race.within(player_realm)

        for race in races:
            emoji = race.value.emoji
            field = Field(f"{emoji} {race.name}", race.value.desc)
            fields.append(field)
            reactions.append(emoji)

        embed = utils.embed(
            self.bot,
            desc=(f"Alright, so you'd like to join the **{player_realm.name}** "
                  f"realm. Here are the races from there, please take your "
                  f"pick."),
            fields=fields
        )
        await message.clear_reactions()
        await message.edit(embed=embed)

        for reaction in reactions:
            await message.add_reaction(reaction)

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add",
                check=self.check(user_id, message, reactions),
                timeout=120.0
            )
        except asyncio.TimeoutError:
            return await message.clear_reactions()
        else:
            for race in races:
                if str(reaction.emoji) == race.value.emoji:
                    player_race = race
                    break

        fields = (
            Field("Realm", f"{player_realm.value.emoji} {player_realm.name}"),
            Field("Race", f"{player_race.value.emoji} {player_race.name}")
        )
        reactions = (
            Emoji.WHITE_HEAVY_CHECK_MARK,
            Emoji.CROSS_MARK
        )
        embed = utils.embed(
            self.bot,
            desc=("Here is what you've selected. Are these details correct?\n\n"

                  "**Note**\n"
                  "Once you've selected them, you cannot change them until the "
                  "first Friday of this/next month!"),
            fields=fields
        )
        await message.clear_reactions()
        await message.edit(embed=embed)

        for reaction in reactions:
            await message.add_reaction(reaction)

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add",
                check=self.check(user_id, message, reactions),
                timeout=30.0
            )
        except asyncio.TimeoutError:
            return await message.clear_reactions()
        else:
            title = "Oh... Uh oh"
            desc = ("It seems we've made a mistake... We can go through the "
                    "registration process again if you like! Just run the "
                    "command again when you're ready and we'll start over from "
                    "scratch!")

            if str(reaction.emoji) == Emoji.WHITE_HEAVY_CHECK_MARK:
                title = "Registration Complete"
                desc = (f"Done! You are now a(n) {player_race.value.emoji} "
                        f"**{player_race.name}** from the "
                        f"**{player_realm.name}** realm. Welcome to the "
                        f"**Five Realms** family!")
                params = (user_id, player_realm.name, player_race.name)

                await self.bot.db.insert(*params, **self.DEFAULT_PARAMS)

            embed = utils.embed(
                self.bot,
                title=title,
                desc=desc
            )
            await message.clear_reactions()
            await message.edit(embed=embed)

    @checks.confirm_existence(exists=True)
    @commands.command()
    async def profile(self, ctx):
        """
        View your character and check up on how you're doing!
        """
        notes = None
        fields = None
        player = await self.bot.db.get_player(ctx.author.id)
        race_name = player.race.name.replace("_", " ")
        cls = player.get_class()

        if cls is Class.none:
            notes = constants.NO_CLASS

        if notes is not None:
            fields = Field("Notes", f"{Emoji.CLIPBOARD} {notes}")

        embed = utils.embed(
            self.bot,
            title=ctx.author.display_name,
            desc=(
                f"**Class:** {cls.value.emoji} {cls.name.title()}\n"
                f"**Lv. {player.level}** "
                f"({player.exp:,}/{player.needed_exp:,})\n\n"

                f"**Realm:** {player.realm.value.emoji} {player.realm.name}\n"
                f"**Race:** {player.race.value.emoji} {race_name}"
            ),
            fields=fields
        )
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def classes(self, ctx):
        """
        Visit the Colosseum, see what you can be!
        """
        fields = []
        command = constants.PREFIX + ctx.command.name

        for cls in Class.all():
            if cls is not Class.none:
                field = Field(f"{cls.value.emoji} {cls.name}", cls.value.desc)
                fields.append(field)
        embed = utils.embed(
            self.bot,
            title="Classes",
            desc=(f"To select a class, do `{command} choose <class>`\n"
                  f"E.g. `{command} choose warrior`"),
            fields=fields
        )
        await ctx.send(embed=embed)

    @checks.confirm_existence(exists=True)
    @checks.confirm_class(exists=False)
    @classes.command(name="choose")
    async def classes_choose(self, ctx, class_type):
        """
        Be whatever you want to be!
        """
        player = await self.bot.db.get_player(ctx.author.id)
        classes = {str.lower(cls.name): cls for cls in Class.all()}
        class_type = class_type.lower()

        if class_type not in classes.keys():
            return

        key = class_type.title()
        class_type = Class[key]
        player.set_class(class_type)
        embed = utils.embed(
            self.bot,
            title="Congratulations!",
            desc=f"You're now a **{class_type.name}!**"
        )
        await self.bot.db.save(player)
        await ctx.send(embed=embed)

    @checks.confirm_existence(exists=True)
    @checks.dms_enabled()
    @commands.command()
    async def fight(self, ctx, member: discord.Member):
        """
        Get some practice in and spar with a friend or test your mettle
        against a fearsome fighter
        """
        await utils.ensure_existence(member, exists=True, bot=self.bot)
        kwargs = {}

        if ctx.author == member:
            kwargs.setdefault("title", "So...")
            kwargs.setdefault("desc", "Care to explain how that would work?")
        elif member.bot:
            desc = "They have lasers!"

            if member.id == self.bot.user.id:
                desc += " Including me..."
            kwargs.setdefault("title", "You shouldn't be fighting robots...")
            kwargs.setdefault("desc", desc)

        if kwargs != dict():
            embed = utils.embed(self.bot, **kwargs)
            await ctx.send(embed=embed)
        else:
            start_time = time.time()
            reactions = (Emoji.WHITE_HEAVY_CHECK_MARK, Emoji.CROSS_MARK)
            # replace self.wait_for() with comprising functions/methods
            message, reaction = await self.wait_for(
                ctx,
                reactions,
                timeout=30.0,
                title="Ooo...",
                desc=(f"{member.mention}, your **mettle** has been challenged "
                      f"by {ctx.author.mention}! Do you accept?"),
                author_id=member.id
            )

            if reaction == Emoji.CROSS_MARK:
                coroutine = message.edit
                embed = utils.embed(
                    self.bot,
                    title="That was unexpected...",
                    desc=f"Maybe {member.mention}'s having a bad day?"
                )

                if time.time() - start_time >= 20:
                    coroutine = ctx.send
                await coroutine(embed=embed)
            elif reaction == Emoji.WHITE_HEAVY_CHECK_MARK:
                coroutines = []
                members = (ctx.author, member)
                reactions = (
                    Emoji.CROSSED_SWORDS,
                    Emoji.SHIELD,
                    Emoji.ARROW_LEFT
                )
                actions = (
                    "Fight",
                    "Defend",
                    "Flee"
                )
                fields = []

                for emoji, action in zip(reactions, actions):
                    field = Field(f"{emoji} {action}")
                    fields.append(field)

                for member in members:
                    coroutines.append(
                        self.wait_for(
                            member,
                            reactions,
                            timeout=30.0,
                            title="Fight",
                            desc="What would you like to do?",
                            fields=fields,
                            author_id=member.id
                        )
                    )
                done, pending = await asyncio.wait(
                    coroutines,
                    timeout=30.0,
                    return_when=asyncio.ALL_COMPLETED
                )

                print(done, len(done), *done, pending,
                      len(pending), *pending, sep="\n")
                if len(pending) > 0:
                    for task in pending:
                        task.cancel()
                else:
                    print(done)

                    for task in done:
                        print(task)


def setup(bot):
    bot.add_cog(FiveRealmsCog(bot))
