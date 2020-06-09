"""
Player system
"""
import database
from enums import Class
from enums import Race
from enums import Realm


class Player(object):
    def __init__(self, user_id, realm,
                 race, level, exp,
                 class_type=Class.none.name):
        self.id = user_id
        self.realm = Realm[realm]
        self.race = Race[race]
        self.level = level
        self.exp = exp
        self._class_type = class_type
        self._altered = {}

    @property
    def needed_exp(self):
        # return round(self.level * ((self.level+1**2)*1.2))
        return self.level * (self.level+1**2)

    def get_class(self):
        return Class[self._class_type]

    def add_exp(self, amount: int):
        leveled_up = False
        levels = 0
        self.exp += amount
        self._altered["exp"] = self.exp

        while self.exp < self.needed_exp:
            levels += 1

            if leveled_up is False:
                leveled_up = True
        return leveled_up, levels

    def set_class(self, class_type):
        self._class_type = class_type.name
        self._altered["class_type"] = self._class_type

    async def save(self):
        await database.update(self.id, **self._altered)
        self._altered = {}
