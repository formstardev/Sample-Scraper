import copy
from datetime import datetime

try:
    from . import utils
    from . import db
    from . import settings
    from . import enums
except:
    import utils
    import db
    import settings
    import enums

actor_id = settings.ACTOR_SETTINGS["id"]
default_item_obj = settings.DEFAULT_ITEM_OBJ
default_item_price_obj = settings.DEFAULT_ITEM_PRICE_OBJ


class DataStorage:
    def __init__(self, vendor_website=""):
        self.vendor_website = vendor_website
        self.vendor_document_id = None
        self.catalog_document_id = None
        self.catalogs = []
        self.items = []
        self.set_vendor_id()

    def save_prices(self, query_obj, prices):
        for price in prices:
            query_data = copy.deepcopy(settings.DEFAULT_PRICE_QUERY_OBJ)
            query_data[0]["value"] = price["priceType"]
            query_obj["nested_collection"]["nested_collection"]["nested_collection"][
                "query_obj"
            ] = query_data

            price_docs = db.get_data(query_obj=query_obj)
            price_document_id = None
            price_document_data = None
            for price_doc in price_docs:
                price_document_id = price_doc.id
                price_document_data = price_doc._data

            if not price_document_id:
                query_obj["nested_collection"]["nested_collection"][
                    "nested_collection"
                ]["query_obj"] = None
                db.save_data(query_data=query_obj, new_data=price)

            else:
                if price["amount"] == price_document_data["amount"]:
                    db.update_data(
                        query_obj, price_document_id, {"lastSeen": price["lastSeen"]}
                    )
                else:
                    db.update_data(query_obj, price_document_id, {"isHistoric": True})
                    query_obj["nested_collection"]["nested_collection"][
                        "nested_collection"
                    ]["query_obj"] = None
                    db.save_data(query_data=query_obj, new_data=price)

    def set_catalogs(self, data):
        self.catalogs = data

    def set_items(self, data):
        self.items = data  # utils.convert_class_objects_to_list_dic(data)

    def save_items(self, catalog_url):
        self.set_catalog_id(catalog_url)
        item_default_query_obj = copy.deepcopy(settings.DEFAULT_FIRESTORE_QUERY_OBJ)
        item_default_query_obj["collection"] = enums.Collections.Vendors.value
        item_default_query_obj["document_id"] = self.vendor_document_id
        item_default_query_obj["nested_collection"] = copy.deepcopy(
            settings.DEFAULT_FIRESTORE_QUERY_OBJ
        )

        item_default_query_obj["nested_collection"][
            "collection"
        ] = enums.Collections.Catalogs.value
        item_default_query_obj["nested_collection"][
            "document_id"
        ] = self.catalog_document_id
        item_default_query_obj["nested_collection"][
            "nested_collection"
        ] = copy.deepcopy(settings.DEFAULT_FIRESTORE_QUERY_OBJ)

        item_default_query_obj["nested_collection"]["nested_collection"][
            "collection"
        ] = enums.Collections.Items.value

        for item in self.items:
            print(item)
            item_query_obj = copy.deepcopy(item_default_query_obj)
            query_data = copy.deepcopy(settings.DEFAULT_ITEM_QUERY_OBJ)
            query_data[0]["value"] = item["itemUrl"]
            item_query_obj["nested_collection"]["nested_collection"][
                "query_obj"
            ] = query_data
            prices = item["prices"]
            del item["prices"]
            db.save_update_data(query_data=item_query_obj, new_updated_data=item)

            item_docs = db.get_data(query_obj=item_query_obj)
            item_document_id = None
            for item_doc in item_docs:
                item_document_id = item_doc.id
            item_query_obj["nested_collection"]["nested_collection"][
                "document_id"
            ] = item_document_id
            item_query_obj["nested_collection"]["nested_collection"]["query_obj"] = None
            item_query_obj["nested_collection"]["nested_collection"][
                "nested_collection"
            ] = copy.deepcopy(settings.DEFAULT_FIRESTORE_QUERY_OBJ)
            item_query_obj["nested_collection"]["nested_collection"][
                "nested_collection"
            ]["collection"] = enums.Collections.Prices.value

            self.save_prices(item_query_obj, prices)

    def save_vendor(self, name, data_acquisition_method, vendor_type):
        if not self.vendor_document_id:
            vendor_query_obj = copy.deepcopy(settings.DEFAULT_FIRESTORE_QUERY_OBJ)
            vendor_query_obj["collection"] = enums.Collections.Vendors.value
            vendor_data_obj = copy.deepcopy(settings.DEFAULT_VENDOR_OBJ)
            vendor_data_obj["name"] = name
            vendor_data_obj["dataAcquisitionMethod"] = data_acquisition_method
            vendor_data_obj["website"] = self.vendor_website
            vendor_data_obj["type"] = vendor_type

            db.save_data(vendor_query_obj, vendor_data_obj)

    def save_catalogs(self):
        print("DDDDDDDDDDDDDDDDD@@@@@@@@@@@@@@@@DDDDDDDDDDDDDDDDDDDDDDDDD")
        # catalog_default_query_obj = copy.deepcopy(settings.DEFAULT_FIRESTORE_QUERY_OBJ)
        # catalog_default_query_obj["collection"] = enums.Collections.Vendors.value
        # catalog_default_query_obj["document_id"] = self.vendor_document_id

        # catalog_default_query_obj["nested_collection"] = copy.deepcopy(
        #     settings.DEFAULT_FIRESTORE_QUERY_OBJ
        # )
        # catalog_default_query_obj["nested_collection"][
        #     "collection"
        # ] = enums.Collections.Catalogs.value

        # for catalog in self.catalogs:
        #     catalog_query_obj = copy.deepcopy(catalog_default_query_obj)
        #     query_data = copy.deepcopy(settings.DEFAULT_CATALOG_QUERY_OBJ)
        #     query_data[0]["value"] = catalog["catalogUrl"]
        #     catalog_query_obj["nested_collection"]["query_obj"] = query_data

        #     catalog_docs = db.get_data(query_obj=catalog_query_obj)
        #     catalog_document_id = None
        #     catalog_document_data = None

        #     for catalog_doc in catalog_docs:
        #         catalog_document_id = catalog_doc.id
        #         catalog_document_data = catalog_doc._data

        #     if not catalog_document_id:
        #         db.save_data(query_data=catalog_query_obj, new_data=catalog)

        #     else:
        #         if "type" in catalog_document_data:
        #             del catalog["type"]
        #         if "actorSchedule" in catalog_document_data:
        #             del catalog["actorSchedule"]
        #         db.update_data(catalog_query_obj, catalog_document_id, catalog)

    def set_vendor_id(self):
        query_obj = copy.deepcopy(settings.DEFAULT_FIRESTORE_QUERY_OBJ)
        query_obj["collection"] = enums.Collections.Vendors.value

        vendor_query_obj = copy.deepcopy(settings.DEFAULT_VENDOR_QUERY_OBJ)
        vendor_query_obj[0]["value"] = self.vendor_website

        query_obj["query_obj"] = vendor_query_obj

        vendor_docs = db.get_data(query_obj=query_obj)
        for vendor_doc in vendor_docs:
            self.vendor_document_id = vendor_doc.id
            break

    def set_catalog_id(self, catalog_url):
        query_obj = copy.deepcopy(settings.DEFAULT_FIRESTORE_QUERY_OBJ)
        query_obj["collection"] = enums.Collections.Vendors.value
        query_obj["document_id"] = self.vendor_document_id

        query_obj["nested_collection"] = copy.deepcopy(
            settings.DEFAULT_FIRESTORE_QUERY_OBJ
        )
        query_obj["nested_collection"]["collection"] = enums.Collections.Catalogs.value
        query_obj["nested_collection"]["query_obj"] = copy.deepcopy(
            settings.DEFAULT_CATALOG_QUERY_OBJ
        )
        query_obj["nested_collection"]["query_obj"][0]["value"] = catalog_url

        catalog_docs = db.get_data(query_obj=query_obj)
        for catalog_doc in catalog_docs:
            self.catalog_document_id = catalog_doc.id
            break

        if not self.catalog_document_id:
            data = [
                {
                    "collection": enums.Collections.Vendors.value,
                    "document_id": self.vendor_document_id,
                },
                {"collection": enums.Collections.Catalogs.value, "document_id": None},
            ]
            db.create_collection(data)

            catalog_docs = db.get_data(query_obj=query_obj)
            for catalog_doc in catalog_docs:
                self.catalog_document_id = catalog_doc.id
                break

    def update_actor_time(self, document_path="", field_name=""):
        actor_query_obj = copy.deepcopy(settings.DEFAULT_FIRESTORE_QUERY_OBJ)
        path_list = document_path.split("/")

        query_objs = []
        for i in range(0, len(path_list), 2):
            obj = copy.deepcopy(settings.DEFAULT_FIRESTORE_QUERY_OBJ)
            obj["collection"] = path_list[i]
            obj["document_id"] = path_list[i + 1]
            query_objs.append(obj)

        query_objs.reverse()
        actor_query_obj = None

        for query_obj in query_objs:
            if not actor_query_obj:
                actor_document_id = query_obj["document_id"]
                query_obj["document_id"] = None

            else:
                query_obj["nested_collection"] = actor_query_obj

            actor_query_obj = query_obj

        actor_schedule = {field_name: datetime.utcnow()}
        db.update_data(actor_query_obj, actor_document_id, actor_schedule)


def main():
    vendor_website = "https://www.bhphotovideo.com/"

    data_storage = DataStorage(vendor_website)
    # data_storage.save_items()


if __name__ == "__main__":
    main()
