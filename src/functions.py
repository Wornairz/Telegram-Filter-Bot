from .settings import get_db_collection

def get_all_users_data():
    return get_db_collection().find()


def get_user_keywords(user):
    find_query = {"user": user}
    return get_db_collection().find_one(find_query).get("keywords", [])


def get_user_channels(user):
    find_query = {"user": user}
    var = get_db_collection().find_one(find_query)
    if var is None:
        return []
    return get_db_collection().find_one(find_query).get("channels", [])

def remove_channel(user, channel):
    find_query = {"user": user}
    return get_db_collection().update_one(find_query, {"$pull": {"channels": channel}})

def remove_keyword(user, keyword):
    find_query = {"user": user}
    return get_db_collection().update_one(find_query, {"$pull": {"keywords": keyword}})

def create_user(user):
    find_query = {"user": user}
    get_db_collection().update_one(find_query, {"$set": {"user": user}}, upsert=True)
    
