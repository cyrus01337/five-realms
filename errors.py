from discord.ext import commands

import utils


class FiveRealmsError(commands.CommandError):
    def __init__(self, title: str, desc: str, user_id: int):
        self.title = title
        self.desc = desc
        self.user_id = user_id

    def to_embed(self, bot: commands.Bot):
        return utils.embed(bot, title=self.title, desc=self.desc)


class DatabaseError(FiveRealmsError):
    def __init__(self, title, desc, user_id):
        super().__init__(title, desc, user_id)


class UserClassError(FiveRealmsError):
    def __init__(self, title, desc, user_id, class_type):
        super().__init__(title, desc, user_id)
        self._class_type = class_type

    def get_class(self):
        return self._class_type


class UserRegistrationError(DatabaseError):
    def __init__(self, title, desc, user_id):
        super().__init__(title, desc, user_id)
