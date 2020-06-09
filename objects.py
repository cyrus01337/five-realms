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
