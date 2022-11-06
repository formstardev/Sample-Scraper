import copy
from . import utils
from . import db
from . import settings
from . import enums


def populate_actors():
    actor_data = {
        "_createdBy": {
            "displayName": None,
            "email": settings.ACTOR_SETTINGS["email"],
            "emailVerified": True,
            "isAnonymous": False,
            "photoURL": None,
            "timestamp": utils.get_current_time(),
            "uid": settings.ACTOR_SETTINGS["uid"],
        },
        "_updatedBy": {
            "displayName": None,
            "email": settings.ACTOR_SETTINGS["email"],
            "emailVerified": True,
            "isAnonymous": False,
            "photoURL": None,
            "timestamp": utils.get_current_time(),
            "uid": settings.ACTOR_SETTINGS["uid"],
        },
        "type": enums.CatalogType.Catalog.value,
    }

    db.save_data(enums.Collections.Actors.value, actor_data)


def populate_super_catalog():
    actor_docs = db.get_data(
        enums.Collections.Actors.value,
        [
            {
                "field": "_createdBy.email",
                "operator": "==",
                "value": settings.ACTOR_SETTINGS["email"],
            }
        ],
    )
    actor_id = None
    for actor_doc in actor_docs:
        actor_id = actor_doc.id
        break

    default_catalog_data = {
        "_createdBy": {
            "actorId": actor_id,
            "displayName": None,
            "email": settings.ACTOR_SETTINGS["email"],
            "emailVerified": True,
            "isAnonymous": False,
            "photoURL": None,
            "timestamp": None,
            "uid": settings.ACTOR_SETTINGS["uid"],
        },
        "_updatedBy": {
            "actorId": actor_id,
            "displayName": None,
            "email": settings.ACTOR_SETTINGS["email"],
            "emailVerified": True,
            "isAnonymous": False,
            "photoURL": None,
            "timestamp": None,
            "uid": settings.ACTOR_SETTINGS["uid"],
        },
        "actorId": actor_id,
        "actorSchedule": None,
        "catalogUrl": "",
        "type": "",
        "vendor": "",
    }

    super_catalogs = [
        (
            enums.SuperCatalog.BH.value,
            "https://www.bhphotovideo.com/c/browse/Shop-by-Brand/ci/9028/N/4291093803",
        )(
            enums.SuperCatalog.EmpirePro.value,
            "https://www.empirepro.com/catalog/category/view/s/pro-brands/id/8/",
        ),
        (
            enums.SuperCatalog.FullCompass.value,
            "https://www.fullcompass.com/brands_show_all.php",
        ),
        (
            enums.SuperCatalog.OneSourceVideo.value,
            "https://1sourcevideo.com/shop/index.php/brands",
        ),
        (
            enums.SuperCatalog.SweetWater.value,
            "https://www.sweetwater.com/store/manufacturer/all",
        ),
        (enums.SuperCatalog.TecNec.value, "https://www.tecnec.com/shop-by-brand"),
    ]

    for super_catalog in super_catalogs:
        catalog_data = copy.deepcopy(default_catalog_data)
        catalog_data["_createdBy"]["timestamp"] = utils.get_current_time()
        catalog_data["_updatedBy"]["timestamp"] = utils.get_current_time()
        catalog_data["actorSchedule"] = enums.ActorSchedules.RANDOM.value
        catalog_data["catalogUrl"] = super_catalog[1]
        catalog_data["type"] = enums.CatalogType.SuperCatalog.value
        catalog_data["vendor"] = super_catalog[0]

        db.save_data(enums.Collections.Catalogs.value, catalog_data)


def populate_catalog():
    actor_docs = db.get_data(
        enums.Collections.Actors.value,
        [
            {
                "field": "_createdBy.email",
                "operator": "==",
                "value": settings.ACTOR_SETTINGS["email"],
            }
        ],
    )
    actor_id = None
    for actor_doc in actor_docs:
        actor_id = actor_doc.id
        break

    default_catalog_data = {
        "_createdBy": {
            "actorId": actor_id,
            "displayName": None,
            "email": settings.ACTOR_SETTINGS["email"],
            "emailVerified": True,
            "isAnonymous": False,
            "photoURL": None,
            "timestamp": None,
            "uid": settings.ACTOR_SETTINGS["uid"],
        },
        "_updatedBy": {
            "actorId": actor_id,
            "displayName": None,
            "email": settings.ACTOR_SETTINGS["email"],
            "emailVerified": True,
            "isAnonymous": False,
            "photoURL": None,
            "timestamp": None,
            "uid": settings.ACTOR_SETTINGS["uid"],
        },
        "actorId": actor_id,
        "actorSchedule": None,
        "brand": None,
        "parentId": None,
        "catalogUrl": "",
        "type": enums.CatalogType.Catalog.value,
        "vendor": "",
    }

    super_catalogs = [
        (enums.SuperCatalog.BH.value, "BHBrands.json"),
        (enums.SuperCatalog.EmpirePro.value, "EmpireProBrands.json"),
        (enums.SuperCatalog.FullCompass.value, "FullCompassBrands.json"),
        (enums.SuperCatalog.OneSourceVideo.value, "OneSourceVideoBrands.json"),
        (enums.SuperCatalog.SweetWater.value, "SweetWaterBrands.json"),
        (enums.SuperCatalog.TecNec.value, "TecNecBrands.json"),
    ]

    base_data_file_path = settings.DATA_FILE_PATH + "/Brands/"

    for super_catalog in super_catalogs:
        super_catalog_docs = db.get_super_catalog(actor_id, super_catalog[0])
        vendor = parent_id = None
        for super_catalog_doc in super_catalog_docs:
            parent_id = super_catalog_doc.id
            vendor = super_catalog_doc._data["vendor"]
            break

        super_catalog_data = copy.deepcopy(default_catalog_data)
        super_catalog_data["vendor"] = vendor
        super_catalog_data["parentId"] = parent_id

        file_path = base_data_file_path + super_catalog[1]
        brands = utils.get_json_from_file(file_path)

        for brand in brands:
            catalog_data = copy.deepcopy(super_catalog_data)
            catalog_data["_createdBy"]["timestamp"] = utils.get_current_time()
            catalog_data["_updatedBy"]["timestamp"] = utils.get_current_time()
            catalog_data["actorSchedule"] = enums.ActorSchedules.RANDOM.value
            catalog_data["catalogUrl"] = brand["TargetURL"]
            catalog_data["brand"] = brand["BrandName"]

            db.save_data(enums.Collections.Catalogs.value, catalog_data)

        #     break
        # break


if __name__ == "__main__":
    # populate_actors()
    # populate_super_catalog()
    # populate_catalog()
    pass
