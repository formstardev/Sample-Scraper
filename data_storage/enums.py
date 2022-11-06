from enum import Enum
import random


class enumproperty(object):
    "like property, but on an enum class"

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, instance, ownerclass=None):
        if ownerclass is None:
            ownerclass = instance.__class__
        return self.fget(ownerclass)

    def __set__(self, instance, value):
        raise AttributeError("can't set pseudo-member %r" % self.name)

    def __delete__(self, instance):
        raise AttributeError("can't delete pseudo-member %r" % self.name)


class Database(Enum):
    FireBase = "firebase"


class Collections(Enum):
    Actors = "Actors"
    Vendors = "Vendors"
    Catalogs = "Catalogs"
    Items = "Items"
    Prices = "Prices"


class ActorSchedules(Enum):
    OnceDaily = "Once Daily"
    Every2Days = "Every 2 Days"
    Every3Days = "Every 3 Days"
    Every4Days = "Every 4 Days"
    Every5Days = "Every 5 Days"
    Every7Days = "Every 7 Days"
    Every14Days = "Every 14 Days"
    Every21Days = "Every 21 Days"
    Every28Days = "Every 28 Days"

    @enumproperty
    def RANDOM(cls):
        return random.choice(list(cls.__members__.values()))


class CatalogType(Enum):
    Catalog = "Catalog"
    SuperCatalog = "SuperCatalog"


class SuperCatalog(Enum):
    Adorama = "Adorama"
    BH = "B&H"
    CCI = "CCI"
    CDW = "CDW"
    EmpirePro = "Empire Pro"
    FullCompass = "Full Compass"
    OneSourceVideo = "1 Source Video"
    StageLightingStore = "Stage Lighting Store"
    SweetWater = "Sweet Water"
    TecNec = "TecNec"
