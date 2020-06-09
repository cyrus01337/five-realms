"""
Helper functions that assist with niche tasks
"""
import os

import discord
from discord.ext import commands

import constants
import database
import errors


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
        for field in fields:
            embed.add_field(**field.kwargs)
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


async def ensure_existence(ctx, exists: bool):
    user_id = ctx.author.id
    user = await database.get_user(user_id)

    if exists:
        if user is None:
            title = "You haven't registered yet!"
            desc = (f"Use `{constants.PREFIX}register` to join the Five "
                    f"Realms adventure!")
            raise errors.UserRegistrationError(title, desc, user_id)
        else:
            return True
    elif user is not None:
        title = "You've already registered, silly!"
        desc = "We can't have two of you!"
        raise errors.UserRegistrationError(title, desc, user_id)
    return True
