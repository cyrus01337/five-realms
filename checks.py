"""
Custom checks for player validation
"""
import discord
from discord.ext import commands

import constants
# import database
import errors
import utils
from enums import Class


def _check(function):
    async def wrapper(*args, **kwargs):
        print(function, args, kwargs, sep="\n")
        return await function(*args, **kwargs)
    return wrapper


def confirm_existence(exists: bool):
    async def predicate(ctx):
        return await utils.ensure_existence(ctx, exists)
    return commands.check(predicate)


def confirm_class(exists: bool):
    async def predicate(ctx):
        await utils.ensure_existence(ctx, exists=True)
        user_id = ctx.author.id
        player = await ctx.bot.db.get_player(user_id)
        player_class = player.get_class()

        if exists:
            if player_class is Class.none:
                title = "You haven't selected a class yet!"
                desc = (f"How about we fix that? You can do "
                        f"`{constants.PREFIX}classes` to see the available "
                        f"classes")
                raise errors.UserClassError(title, desc, user_id, player_class)
            else:
                return player_class
        elif player_class is not Class.none:
            title = f"You're already a {player_class.name}!"
            desc = "If you're anymore different, we won't recognise you!"
            raise errors.UserClassError(title, desc, user_id, player_class)
        return player_class
    return commands.check(predicate)


def dms_enabled(ignore_author: bool = False):
    async def predicate(ctx):
        cannot_dm = []
        values = ctx.args + list(ctx.kwargs.values())

        for value in values:
            if isinstance(value, (discord.User, discord.Member)):
                try:
                    await value.send("This is a test to verify if DMs are "
                                     "enabled, please ignore this message. "
                                     "Thank you!")
                except discord.Forbidden:
                    cannot_dm.append(value)

        if len(cannot_dm) > 0:
            joined = (", ").join(cannot_dm)

            raise errors.DisabledDMs("Aww...", f"It seems that the following "
                                               f"members do not have DMs "
                                               f"enabled: {joined}")
        return True
    return commands.check(predicate)
