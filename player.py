"""
Player system
"""
# from collections.abc import Iterable

from objects import Statistics
from enums import Class
from enums import Race
from enums import Realm

ITERABLE = (tuple, list)


class Player(object):
    def track(method):
        def predicate(self, *args, **kwargs):
            keys, values, *ret = method(self, *args, **kwargs)
            ret = tuple(ret)

            if isinstance(keys, ITERABLE) and isinstance(values, ITERABLE):
                for key, value in zip(keys, values):
                    self._altered[key] = value
            # assuming "keys" is a str and can still be used as a key...
            else:
                self._altered[keys] = values

            if len(ret) == 0:
                ret = None
            elif len(ret) == 1:
                ret = ret[0]
            return ret
        return predicate

    def __init__(self, user_id, realm, race,
                 level, exp, class_type, stats=None):
        self.id = user_id
        self.realm = Realm[realm]
        self.race = Race[race]
        self.level = level
        self.exp = exp
        self._class_type = class_type or Class.none.name
        self.stats = stats or Statistics(health=25, strength=5)
        self._altered = {}

    @property
    def needed_exp(self):
        # return round(self.level * ((self.level+1**2)*1.2))
        return self.level * (self.level+1**2)

    @track
    def add_exp(self, amount: int):
        leveled_up = False
        levels = 0
        self.exp += amount

        while self.exp < self.needed_exp:
            levels += 1

            if leveled_up is False:
                leveled_up = True
        keys = ["exp"]
        values = [self.exp]

        if levels > 0:
            self.level += levels

            keys.append("level")
            values.append(self.level)
        return keys, values, leveled_up, levels

    @track
    def set_class(self, class_type):
        self._class_type = class_type.name
        return "class_type", self._class_type

    def get_class(self):
        return Class[self._class_type]

    def get_changes(self):
        ret = self._altered.copy()
        self._altered.clear()
        return ret
