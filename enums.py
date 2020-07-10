"""
Groups of game elements
"""
import enum

from objects import BaseClass
from objects import BaseRace
from objects import BaseRealm


class Emoji:
    ARROW_LEFT = "\U00002b05\N{VARIATION SELECTOR-16}"
    BABY_ANGEL = "\U0001f47c"
    BIRD = "\U0001f426"
    BOW_AND_ARROW = "\U0001f3f9"
    BUST_IN_SILHOUETTE = "\U0001f464"
    CLIPBOARD = "\U0001f4cb"
    CLOUD_WITH_SNOW = "\U0001f328\N{VARIATION SELECTOR-16}"
    COLLISION_SYMBOL = "\U0001f4a5"
    COMET = "\U00002604\N{VARIATION SELECTOR-16}"
    CROSSED_SWORDS = "\U00002694\N{VARIATION SELECTOR-16}"
    CROSS_MARK = "\U0000274c"
    DAGGER = "\U0001f5e1\N{VARIATION SELECTOR-16}"
    DRAGON = "\U0001f409"
    DROPLET = "\U0001f4a7"
    EVERGREEN_TREE = "\U0001f332"
    EXTRATERRESTRIAL_ALIEN = "\U0001f47d"
    FALLEN_LEAF = "\U0001f343"
    FIRE = "\U0001f525"
    FISH = "\U0001f41f"
    GEAR = "\U00002699"
    GOAT = "\U0001f410"
    HIBISCUS = "\U0001f33a"
    HIGH_VOLTAGE_SIGN = "\U000026a1"
    HOLE = "\U0001f573\N{VARIATION SELECTOR-16}"
    HORSE_FACE = "\U0001f434"
    LEAF_FLUTTERING_IN_WIND = "\U0001f343"
    LION_FACE = "\U0001f981"
    MOUNT_FUJI = "\U0001f5fb"
    NEW_MOON_SYMBOL = "\U0001f311"
    ROUND_PUSHPIN = "\U0001f4cd"
    SEEDLING = "\U0001f331"
    SHIELD = "\U0001f6e1"
    SKULL_AND_CROSSBONES = "\U00002620\N{VARIATION SELECTOR-16}"
    SLEUTH_OR_SPY = "\U0001f575\N{VARIATION SELECTOR-16}"
    SNOWFLAKE = "\U00002744\N{VARIATION SELECTOR-16}"
    SNOWMAN = "\U00002603\N{VARIATION SELECTOR-16}"
    SNOWMAN_WITHOUT_SNOW = "\U000026c4"
    SPARKLES = "\U00002728"
    SQUID = "\U0001f991"
    UNICORN_FACE = "\U0001f984"
    VAMPIRE = "\U0001f9db"
    WATER_wAVE = "\U0001f30a"
    WHITE_HEAVY_CHECK_MARK = "\U00002705"
    WIND_BLOWING_FACE = "\U0001f32c\N{VARIATION SELECTOR-16}"


class Realm(enum.Enum):
    Fire = BaseRealm(Emoji.FIRE)
    Ice = BaseRealm(Emoji.SNOWFLAKE)
    Water = BaseRealm(Emoji.DROPLET)
    Nature = BaseRealm(Emoji.FALLEN_LEAF)
    Space = BaseRealm(Emoji.SPARKLES)

    @classmethod
    def all(cls):
        return list(cls)

    @classmethod
    def all_by(cls, **kwargs):
        collection = None
        collected = {r: [] for r in cls.all()}

        for key, collect in kwargs.items():
            if collect is True:
                for realm in cls.all():
                    value = getattr(realm, key)
                    collection = collected.get(realm)
                    collection.append(value)

        if len(collection) == 1:
            for key, value in collected.items():
                collected[key] = value[0]
        return tuple(collected.values())


class Race(enum.Enum):
    # fire
    Pheonix = BaseRace("Pheonix", Realm.Fire, Emoji.BIRD)
    Assassin = BaseRace("Assassin", Realm.Fire, Emoji.DAGGER)
    Seraphim = BaseRace("Seraphim", Realm.Fire, Emoji.BABY_ANGEL)
    Dragon = BaseRace("Dragon", Realm.Fire, Emoji.DRAGON)
    Sprite = BaseRace("Sprite", Realm.Fire, Emoji.FIRE)

    # ice
    Snowman = BaseRace("Snowman", Realm.Ice, Emoji.SNOWMAN_WITHOUT_SNOW)
    Yeti = BaseRace("Yeti", Realm.Ice, Emoji.SNOWMAN)
    Ice_Assassin = BaseRace("Ice Assassin", Realm.Ice, Emoji.DAGGER)
    Ice_Dragon = BaseRace("Ice Dragon", Realm.Ice, Emoji.DRAGON)
    Ice_Fairy = BaseRace("Ice Fairy", Realm.Ice, Emoji.SNOWFLAKE)
    Frost_Giant = BaseRace("Frost Giant", Realm.Ice, Emoji.CLOUD_WITH_SNOW)
    Ice_Mage = BaseRace("Ice Mage", Realm.Ice, Emoji.WIND_BLOWING_FACE)
    Cultist = BaseRace("Cultist", Realm.Ice, Emoji.SLEUTH_OR_SPY)
    Ice_Vampire = BaseRace("Ice Vampire", Realm.Ice, Emoji.VAMPIRE)

    # water
    Siren = BaseRace("Siren", Realm.Water, Emoji.WIND_BLOWING_FACE)
    Pirate = BaseRace("Pirate", Realm.Water, Emoji.SKULL_AND_CROSSBONES)
    Merpeople = BaseRace("Merpeople", Realm.Water, Emoji.FISH)
    Kraken = BaseRace("Kraken", Realm.Water, Emoji.SQUID)
    Naiad = BaseRace("Naiad", Realm.Water, Emoji.WATER_wAVE)

    # nature
    Hunter = BaseRace("Hunter", Realm.Nature, Emoji.BOW_AND_ARROW)
    Satyr = BaseRace("Satyr", Realm.Nature, Emoji.GOAT)
    Troll = BaseRace("Troll", Realm.Nature, Emoji.MOUNT_FUJI)
    Unicorn = BaseRace("Unicorn", Realm.Nature, Emoji.UNICORN_FACE)
    Centaur = BaseRace("Centaur", Realm.Nature, Emoji.HORSE_FACE)
    Dryad = BaseRace("Dryad", Realm.Nature, Emoji.LEAF_FLUTTERING_IN_WIND)
    Elf = BaseRace("Elf", Realm.Nature, Emoji.SEEDLING)
    Fairy = BaseRace("Fairy", Realm.Nature, Emoji.HIBISCUS)
    Tamer = BaseRace("Tamer", Realm.Nature, Emoji.LION_FACE)
    Ent = BaseRace("Ent", Realm.Nature, Emoji.EVERGREEN_TREE)

    # space
    Comet = BaseRace("Comet", Realm.Space, Emoji.COMET)
    Space_Dragon = BaseRace("Space Dragon", Realm.Space, Emoji.DRAGON)
    Titan = BaseRace("Titan", Realm.Space, Emoji.COLLISION_SYMBOL)
    Warlock = BaseRace("Warlock", Realm.Space, Emoji.HIGH_VOLTAGE_SIGN)
    Alien = BaseRace("Alien", Realm.Space, Emoji.EXTRATERRESTRIAL_ALIEN)
    Astronaut = BaseRace("Astronaut", Realm.Space, Emoji.NEW_MOON_SYMBOL)
    Black_Hole = BaseRace("Black_Hole", Realm.Space, Emoji.HOLE)
    Reaper = BaseRace("Reaper", Realm.Space, Emoji.BUST_IN_SILHOUETTE)

    @classmethod
    def all(cls):
        return list(cls)

    @classmethod
    def within(cls, realm):
        ret = []

        for race in cls.all():
            if race.value.realm is realm:
                ret.append(race)
        return tuple(ret)


class Class(enum.Enum):
    Warrior = BaseClass(Emoji.SHIELD)
    Mage = BaseClass(Emoji.ROUND_PUSHPIN)
    Rogue = BaseClass(Emoji.DAGGER)
    none = BaseClass(Emoji.GEAR)

    @classmethod
    def all(cls):
        return list(cls)
