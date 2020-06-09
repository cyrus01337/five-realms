"""

"""
import asyncio
from discord.ext import commands

import checks
import constants
import database
import utils
from enums import Class
from enums import Emoji
from enums import Race
from enums import Realm
from objects import Field


class FiveRealmsCog(commands.Cog, name="RPG"):
    def __init__(self, bot):
        self.bot = bot
        self.DEFAULT = {
            "level": 1,
            "exp": 0,
            "class_type": Class.none.name
        }

    def check(self, ctx, iterable, event):
        check = None

        if event == "reaction_add":
            def check(reaction, user):
                return (user.id == ctx.author.id
                        and str(reaction.emoji) in iterable)
        return check

    @checks.confirm_existence(exists=False)
    @commands.command()
    async def register(self, ctx):
        """
        Create your character, start your adventure!
        """
        player_realm = None
        player_race = None
        races = None
        fields = []
        reactions = []
        realms = Realm.all()

        for realm in realms:
            emoji = realm.value.emoji
            field = Field(f"{emoji} {realm.name}", "desc")
            fields.append(field)
            reactions.append(emoji)
        embed = utils.embed(
            self.bot,
            desc="haha the developer is lazy",
            fields=fields
        )
        message = await ctx.send(embed=embed)

        for emoji in reactions:
            await message.add_reaction(emoji)

        try:
            selected, _ = await self.bot.wait_for(
                "reaction_add",
                check=self.check(ctx, reactions, "reaction_add"),
                timeout=120.0
            )
        except asyncio.TimeoutError:
            return await message.clear_reactions()
        else:
            selected = str(selected)

            for realm in realms:
                if selected == realm.value.emoji:
                    player_realm = realm
                    break
        races = Race.in_realm(player_realm)
        fields.clear()
        reactions.clear()

        for race in races:
            name = race.name.replace("_", " ")
            emoji = race.value.emoji
            field = Field(f"{emoji} {name}", "desc")
            fields.append(field)
            reactions.append(emoji)
        embed = utils.embed(
            self.bot,
            desc=f"Realm selected: `{player_realm.name}`",
            fields=fields
        )
        await message.clear_reactions()
        await message.edit(embed=embed)

        for emoji in reactions:
            await message.add_reaction(emoji)

        try:
            selected, _ = await self.bot.wait_for(
                "reaction_add",
                check=self.check(ctx, reactions, "reaction_add"),
                timeout=120.0
            )
        except asyncio.TimeoutError:
            return await message.clear_reactions()
        else:
            selected = str(selected)

            for race in races:
                if selected == race.value.emoji:
                    player_race = race
                    break
        race_name = player_race.name.replace("_", " ")
        reactions = (Emoji.WHITE_HEAVY_CHECK_MARK, Emoji.CROSS_MARK)
        embed = utils.embed(
            self.bot,
            desc=("Here is what you've selected. Are these details "
                  "correct?\n\n"

                  "**Note**\n"
                  "Once you've selected them you can't change them until "
                  "every first Friday of the month!"),
            fields=(
                Field("Realm", (f"{player_realm.value.emoji} "
                                f"{player_realm.name}")),
                Field("Race", f"{player_race.value.emoji} {race_name}")
            )
        )
        await message.clear_reactions()
        await message.edit(embed=embed)

        for emoji in reactions:
            await message.add_reaction(emoji)

        try:
            selected, _ = await self.bot.wait_for(
                "reaction_add",
                check=self.check(ctx, reactions, "reaction_add"),
                timeout=120.0
            )
        except asyncio.TimeoutError:
            return await message.clear_reactions()
        else:
            selected = str(selected)

            if selected == Emoji.WHITE_HEAVY_CHECK_MARK:
                desc = (f"Done! You are now a(n) {player_race.value.emoji} "
                        f"**{race_name}** from the **{player_realm.name}** "
                        f"Realm. Welcome to the Five Realms family!")
                args = (ctx.author.id, player_realm.name, player_race.name)
                embed = utils.embed(self.bot, title="Registration Complete",
                                    desc=desc)

                await database.insert(*args, **self.DEFAULT)
            elif selected == Emoji.CROSS_MARK:
                embed = utils.embed(
                    self.bot,
                    title="Oh... Uh oh",
                    desc=("It seems we've made a mistake... We can go through "
                          "the registration process again if you like! Just "
                          "run the command again and we'll start over from "
                          "scratch!")
                )
        finally:
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
        player = await database.get_user(ctx.author.id)
        race_name = player.race.name.replace("_", " ")
        cls = player.get_class()

        if cls is Class.none:
            notes = constants.NO_CLASS

        if notes is not None:
            fields = (
                Field("Notes", f"{Emoji.CLIPBOARD} {notes}"),
            )

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
        player = await database.get_user(ctx.author.id)
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
        await player.save()
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(FiveRealmsCog(bot))
