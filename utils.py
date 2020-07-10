"""
Helper functions that assist with niche tasks
"""
import os
from collections.abc import Iterable

import discord
from discord.ext import commands

import constants
# import database
import errors
from objects import Field


def get_cogs():
    ret = []

    for obj in os.listdir("./cogs"):
        if obj.endswith(".py"):
            name = obj.replace(".py", "")
            ret.append(name)
    return tuple(ret)


def multi_pop(mapping, *keys):
    for key in keys:
        try:
            return mapping.pop(key)
        except KeyError:
            continue
    return None


def embed(bot, **kwargs):
    title = kwargs.pop("title", None)
    description = multi_pop(kwargs, "description", "desc", None)
    embed = discord.Embed(title=title, description=description)
    author = kwargs.pop("author", bot.user)
    fields = kwargs.pop("fields", tuple())

    embed.set_author(name=author.name, icon_url=str(author.avatar_url))

    if fields is not None:
        to_add = []

        if isinstance(fields, Iterable):
            for field in fields:
                to_add.append(field.kwargs)
        elif isinstance(fields, Field):
            to_add.append(fields.kwargs)

        for kwargs in to_add:
            embed.add_field(**kwargs)
    return embed


def clear_screen(bot):
    commands = {
        "nt": "cls",
        "posix": "clear"
    }
    os.system(commands.get(os.name))
    print(bot.user.name, end="\n\n")


def multi_sorted(iterable, *filters):
    for key in filters:
        iterable = sorted(iterable, key=key)
    return iterable


async def command_prefix(bot, message):
    return commands.when_mentioned_or(constants.PREFIX)(bot, message)


async def ensure_existence(member, exists: bool, bot=None):
    if isinstance(member, commands.Context):
        ctx = member
        member = ctx.author
        bot = bot or ctx.bot
    member_id = member.id
    database = bot.db
    player = await database.get_player(member_id)

    if exists:
        if player is None:
            title = "You haven't registered yet!"
            desc = (f"Use `{constants.PREFIX}register` to join the Five "
                    f"Realms adventure!")
            raise errors.UserRegistrationError(title, desc, member_id)
        else:
            return True
    elif player is not None:
        title = "You've already registered, silly!"
        desc = "We can't have two of you!"
        raise errors.UserRegistrationError(title, desc, member_id)
    return True
