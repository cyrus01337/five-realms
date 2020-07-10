"""
Classes to prepare data for procedural use
"""


# class FiveRealmsObject(object):
#     def __init__(self, name, emoji, desc=None):
#         self.name = name
#         self.desc = desc or "desc"
#         self.emoji = emoji

#     def format(self):
#         return self.name.replace("_", " ")


class BaseRealm(object):
    def __init__(self, emoji, desc=None):
        self.desc = desc or "desc"
        self.emoji = emoji


class BaseRace(object):
    # desc omitted
    def __init__(self, name, realm, emoji, desc=None):
        self.name = name
        self.desc = desc or "desc"
        self.realm = realm
        self.emoji = emoji


class Field(object):
    def __init__(self, name=None, value=None, inline=False):
        self.name = name
        self.value = value
        self.inline = inline
        self.kwargs = dict(name=name, value=value, inline=inline)


class BaseClass(object):
    def __init__(self, emoji, desc=None):
        self.desc = desc or "desc"
        self.emoji = emoji


class Statistics(object):
    MAX = 25
    MIN = 0

    def __init__(self, health, strength):
        self.health = health
        self.strength = strength

    def __iadd__(self, value):
        if self.health + value > self.MAX:
            self.health = self.MAX
        else:
            self.health += value

    def __isub__(self, value):
        if self.health - value < self.MIN:
            self.health = self.MIN
        else:
            self.health -= value
