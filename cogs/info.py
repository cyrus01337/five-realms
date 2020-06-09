"""
Query information about the bot or it's commands
"""
# import inspect
from inspect import Parameter
from typing import Union

from discord.ext import commands

import constants
import utils
from objects import Field


class HelpCommand(commands.HelpCommand):
    def __init__(self, **kwargs):
        command_attrs = {
            "help": "Find out how you can use me!",
            "aliases": ["commands"]
        }
        super().__init__(command_attrs=command_attrs)

    def is_hidden(self, command):
        return command.hidden or self.is_cog_hidden(command.cog)

    def is_cog_hidden(self, cog):
        return getattr(cog, "hidden", False)

    def get_group_subcommands(self, group):
        subcommands = []

        for command in group.commands:
            if isinstance(command, commands.Group):
                for appending in self.get_group_subcommands(command):
                    subcommands.append(appending)
            spacing = ""

            if command.full_parent_name:
                spacing = " "
            append = (f"`{constants.PREFIX}{command.full_parent_name}"
                      f"{spacing}{command.name}`")
            subcommands.append(append)
        return utils.multi_sorted(subcommands, str, len)

    async def send_help(self, medium: Union[commands.Command, commands.Group]):
        if self.is_hidden(medium):
            return
        signature = self.get_command_signature(medium)
        title = medium.name.title()

        if signature is not None:
            signature = f"`{signature}`"
        else:
            signature = "None"

        if medium.full_parent_name:
            title = f"{medium.full_parent_name.capitalize()} {medium.name}"
        fields = (
            Field("Description", medium.help),
            Field("Arguments", signature)
        )

        if isinstance(medium, commands.Group):
            subcommands = self.get_group_subcommands(medium)
            joined = ("\n").join(subcommands)
            fields += (
                Field("Subcommands", joined),
            )

        if medium.cog is not None:
            title += f" ({medium.cog.qualified_name})"

        if medium.aliases:
            aliases = (", ").join(medium.aliases)
            fields += (
                Field("Aliases", f"`{aliases}`"),
            )

        embed = utils.embed(
            self.context.bot,
            title=title,
            desc=("Arguments formatted like `*this` are required to run the "
                  "command. Arguments without the format are not required, "
                  "but can be used to add additional features to the "
                  "command."),
            fields=fields
        )
        await self.context.send(embed=embed)

    def get_command_signature(self, command):
        params = []

        for param in command.clean_params.values():
            prepend = ""

            if param.kind is Parameter.POSITIONAL_OR_KEYWORD:
                prepend = "*"
            params.append(prepend + param.name)

        if params == []:
            return None
        return (" ").join(params)

    async def filter_commands(self, commands, *args, **kwargs):
        return sorted(commands, key=lambda c: c.name)

    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot
        fields = []
        mapping.pop(None)
        sorted_cogs = sorted(mapping.keys(), key=lambda c: c.qualified_name)
        mapping = {c: mapping[c] for c in sorted_cogs if mapping[c] != []}
        is_not_owner = await bot.is_owner(self.context.author) is False

        for cog, cog_commands in mapping.items():
            if self.is_cog_hidden(cog) and is_not_owner:
                continue

            cog_commands = await self.filter_commands(cog_commands)
            title = cog.qualified_name
            desc = (", ").join(f"`{c.name}`" for c in cog_commands)
            field = Field(title, desc)
            fields.append(field)
        embed = utils.embed(
            bot,
            title=ctx.invoked_with.title(),
            fields=fields
        )
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        await self.send_help(command)

    async def send_group_help(self, group):
        await self.send_help(group)


class InfoCog(commands.Cog, name="Info"):
    def __init__(self, bot):
        self.bot = bot
        bot.help_command = HelpCommand()
        bot.help_command.cog = self

    @commands.command()
    async def prefix(self, ctx):
        """
        Find out what my prefix is! (You can mention me to find this out too)
        """
        desc = f"Use `{constants.PREFIX}` or mention me!"
        embed = utils.embed(self.bot, title="Prefix", desc=desc)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(InfoCog(bot))
