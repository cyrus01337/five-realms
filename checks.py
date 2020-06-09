"""
Custom checks for player validation
"""
from discord.ext import commands

import constants
import database
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
        user = await database.get_user(user_id)
        user_class = user.get_class()

        if exists:
            if user_class is Class.none:
                title = "You haven't selected a class yet!"
                desc = (f"How about we fix that? You can do "
                        f"`{constants.PREFIX}classes` to see the available "
                        f"classes")
                raise errors.UserClassError(title, desc, user_id, user_class)
            else:
                return user_class
        elif user_class is not Class.none:
            title = f"You're already a {user_class.name}!"
            desc = "If you're anymore different, we won't recognise you!"
            raise errors.UserClassError(title, desc, user_id, user_class)
        return user_class
    return commands.check(predicate)
