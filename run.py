"""
Main file - creates the bot, override methods and events, handle
shutdown logic,
"""
import os

from discord.ext import commands

with open("_TOKEN", "r") as f:
    TOKEN = str.strip(f.read())


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        os.system("clear")
        print(self.user.name, end="\n\n")


if __name__ == '__main__':
    bot = Bot(command_prefix="5!", owner_id=668906205799907348)
    bot.run(TOKEN)
