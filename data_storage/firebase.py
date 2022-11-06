from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

try:
    from . import utils
    from . import settings
    from . import enums
except:
    import utils
    import settings
    import enums

firebase_settings = settings.DB_SETTINGS[enums.Database.FireBase.value]

cred = credentials.Certificate(firebase_settings["serviceAccountKeyFilePath"])
# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred)


def get_db_client():
    return firestore.client()


def save_update_data(query_obj={}, new_updated_data={}):

    docs = get_data(query_obj)

    document_uuid = None
    for doc in docs:
        document_uuid = doc.id
        break

    if document_uuid:
        update_data(query_obj, document_uuid, data=new_updated_data)
    else:
        save_data(query_obj=query_obj, data=new_updated_data)


def save_data(query_obj={}, data={}):
    document_uuid = utils.get_uuid()
    db = get_db_client()

    doc_ref = None
    while True:
        if query_obj.get("collection"):
            if doc_ref:
                doc_ref = doc_ref.collection(query_obj.get("collection"))
            else:
                doc_ref = db.collection(query_obj.get("collection"))
        if query_obj.get("document_id"):
            doc_ref = doc_ref.document(query_obj.get("document_id"))
        query_obj = query_obj.get("nested_collection")
        if not query_obj:
            break
    doc_ref.document(document_uuid).set(data)


def update_data(query_obj="", document_uuid="", data={}):
    db = get_db_client()
    doc_ref = None
    while True:
        if query_obj.get("collection"):
            if doc_ref:
                doc_ref = doc_ref.collection(query_obj.get("collection"))
            else:
                doc_ref = db.collection(query_obj.get("collection"))
        if query_obj.get("document_id"):
            doc_ref = doc_ref.document(query_obj.get("document_id"))
        query_obj = query_obj.get("nested_collection")
        if not query_obj:
            break
    doc_ref = doc_ref.document(document_uuid)
    doc_ref.update(utils.flatten_json(data))


def save_batch_data(collection="", data=[]):

    db = get_db_client()
    batch = db.batch()
    counter = 0
    for item in data:

        document_uuid = utils.get_uuid()
        print(f"Collection: {collection}, Document UUID: {document_uuid}")
        doc_ref = db.collection(collection).document(document_uuid)

        batch.set(doc_ref, item)
        counter += 1
        if counter >= 500:
            counter = 0
            batch.commit()
            batch = db.batch()
    if counter:
        batch.commit()


def get_data(query_obj={}):
    db = get_db_client()
    query_ref = None
    try:
        while True:
            if query_obj.get("collection"):
                if query_ref:
                    query_ref = query_ref.collection(query_obj.get("collection"))
                else:
                    query_ref = db.collection(query_obj.get("collection"))
            if query_obj.get("document_id"):
                query_ref = query_ref.document(query_obj.get("document_id"))
            if query_obj.get("query_obj"):
                for item in query_obj.get("query_obj"):
                    query_ref = query_ref.where(
                        item["field"], item["operator"], item["value"]
                    )
            query_obj = query_obj.get("nested_collection")
            if not query_obj:
                break
    except Exception as e:
        print(e)
    return query_ref.stream()


def create_collection(data={}):
    db = get_db_client()
    doc_ref = None
    for item in data:
        if doc_ref:
            doc_ref = doc_ref.collection(item.get("collection"))
        else:
            doc_ref = db.collection(item.get("collection"))
        if item.get("document_id"):
            doc_id = item.get("document_id")
        else:
            doc_id = utils.get_uuid()
        doc_ref = doc_ref.document(doc_id)
    doc_ref.set({})


def get_collection(collection_obj=None, query_obj={}):
    db = get_db_client()
    if collection_obj:
        collections = (
            collection_obj.collection(query_obj["collection"])
            .document(query_obj["document_id"])
            .collections()
        )
    else:
        collections = (
            db.collection(query_obj["collection"])
            .document(query_obj["document_id"])
            .collections()
        )

    return collections


def get_document_from_collection(collection=None, document_id=None):
    for doc in collection.stream():
        if doc.id == document_id:
            return doc
    return None


def main():
    data = [
        {"collection": "Vendors", "document_id": "zzzzzzzzzzzzzzzzzzzy"},
        {"collection": "T", "document_id": None},
    ]
    # create_collection(data)
    update_document(
        "Tasks", "Z9BSTGuVDir5RWFzjVOz", {"actorEndTime": datetime.utcnow()}
    )


if __name__ == "__main__":
    main()
