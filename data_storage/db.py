try:
    from data_storage import settings
    from data_storage import firebase
    from data_storage import enums
except:
    import settings
    import firebase
    import enums


def save_data(query_data, new_data):
    if enums.Database.FireBase.value == settings.DB:
        firebase.save_data(query_data, new_data)


def save_update_data(query_data, new_updated_data):
    if enums.Database.FireBase.value == settings.DB:
        firebase.save_update_data(
            query_obj=query_data,
            new_updated_data=new_updated_data,
        )


def save_batch_data(collection, list_data):
    if enums.Database.FireBase.value == settings.DB:
        firebase.save_batch_data(collection=collection, data=list_data)


def get_data(query_obj):
    if enums.Database.FireBase.value == settings.DB:
        return firebase.get_data(query_obj=query_obj)
    return []


def get_collection(collection_obj, query_obj):
    if enums.Database.FireBase.value == settings.DB:
        return firebase.get_collection(
            collection_obj=collection_obj, query_obj=query_obj
        )
    return []


def update_data(query_obj, document_uuid, json_data):
    if enums.Database.FireBase.value == settings.DB:
        firebase.update_data(
            query_obj=query_obj, document_uuid=document_uuid, data=json_data
        )


def create_collection(data):
    if enums.Database.FireBase.value == settings.DB:
        firebase.create_collection(data=data)
