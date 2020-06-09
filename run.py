"""
Main file - creates the bot, override methods and events, handle
shutdown logic,
"""
import asyncio
import os
import re

import discord
from discord.ext import commands

import constants
import database
import utils


class FiveRealms(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop.create_task(self.setup())
        self.invite_perms = discord.Permissions(
            send_messages=True,
            add_reactions=True,
            manage_messages=True,
            embed_links=True
        )

        self._database_task = self.loop.create_task(database.init())
        self._database_task.add_done_callback(self._database_done)

    def _database_done(self, *args):
        try:
            self.cache = self._database_task.result()
        except (asyncio.CancelledError, asyncio.InvalidStateError):
            self.cache = None

    async def setup(self):
        await self.wait_until_ready()
        self.mentioned = re.compile(rf"^<@!{self.user.id}?>$")

        message = f"{self.user.name}\n\n"
        name = f"for {constants.PREFIX} or mentions"
        activity = discord.Activity(type=discord.ActivityType.watching,
                                    name=name)

        for cog in utils.get_cogs():
            self.load_extension(f"cogs.{cog}")
            message += f"Cog loaded: {cog}\n"

        os.system("clear")
        print(message)
        await self.change_presence(activity=activity)

    def run(self, *args, **kwargs):
        with open("_TOKEN", "r") as f:
            TOKEN = str.strip(f.read())
        super().run(TOKEN, *args, **kwargs)

    async def on_message(self, message):
        if self.mentioned.fullmatch(message.content):
            ctx = await bot.get_context(message)
            command = bot.get_command("prefix")

            return await command(ctx)
        await bot.process_commands(message)


if __name__ == '__main__':
    bot = FiveRealms(command_prefix=utils.command_prefix,
                     owner_id=668906205799907348)
    bot.run()
