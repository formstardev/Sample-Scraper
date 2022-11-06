import os

try:
    from . import enums
except:
    import enums

BASE_DIRECTORY = os.getcwd()

DB = enums.Database.FireBase.value
DB_SETTINGS = {
    enums.Database.FireBase.value: {
        "serviceAccountKeyFilePath": "data_storage/alta-etl-4ef596932931.json",
        # "serviceAccountKeyFilePath": "data_storage/alta-playground-81cf99e731c4.json",
    }
}

ACTOR_SETTINGS = {
    "id": "0d286f61d6574c98a89f8360062cabd7",
    "email": "scraper1@alta.systems",
    "uid": "n6mMj4I28hZhELVUfr4es0VmNfj2",
}


DEFAULT_CATALOG_OBJ = {
    "_createdBy": {
        "actorId": ACTOR_SETTINGS["id"],
        "displayName": None,
        "email": ACTOR_SETTINGS["email"],
        "emailVerified": True,
        "isAnonymous": False,
        "photoURL": None,
        "timestamp": None,
        "uid": ACTOR_SETTINGS["uid"],
    },
    "_updatedBy": {
        "actorId": ACTOR_SETTINGS["id"],
        "displayName": None,
        "email": ACTOR_SETTINGS["email"],
        "emailVerified": True,
        "isAnonymous": False,
        "photoURL": None,
        "timestamp": None,
        "uid": ACTOR_SETTINGS["uid"],
    },
    "actorId": ACTOR_SETTINGS["id"],
    "actorSchedule": None,
    "brand": None,
    "parentId": None,
    "catalogUrl": "",
    "type": enums.CatalogType.Catalog.value,
    "vendor": "",
}

DEFAULT_ITEM_OBJ = {
    "itemName": {"type": "string", "value": None},
    "itemUrl": {"type": "string", "value": None},
    "manufacturerSku": {"type": "string", "value": None},
    "vendorSku": {"type": "string", "value": None},
}

DEFAULT_VENDOR_OBJ = {
    "dataAcquisitionMethod": None,
    "name": None,
    "type": [],
    "website": None,
}

DEFAULT_ITEM_PRICE_OBJ = {
    "amount": {"type": "number", "value": 0},
    "currencyCode": {"type": "string", "value": None},
    "priceType": {"type": "array", "values": {"type": "string", "value": None}},
}


DEFAULT_FIRESTORE_QUERY_OBJ = {
    "collection": None,
    "document_id": None,
    "query_obj": [],
    "nested_collection": None,
}

DEFAULT_VENDOR_QUERY_OBJ = [
    {
        "field": "website",
        "operator": "==",
        "value": None,
    }
]

DEFAULT_CATALOG_QUERY_OBJ = [
    {
        "field": "catalogUrl",
        "operator": "==",
        "value": None,
    }
]

DEFAULT_ITEM_QUERY_OBJ = [
    {
        "field": "itemUrl",
        "operator": "==",
        "value": None,
    }
]

DEFAULT_PRICE_QUERY_OBJ = [
    {
        "field": "priceType",
        "operator": "==",
        "value": None,
    },
    {
        "field": "isHistoric",
        "operator": "==",
        "value": False,
    },
]
