from .settings import get_db_collection

def get_all_users_data():
    return get_db_collection().find()


def get_user_keywords(user):
    find_query = {"user": user}
    return get_db_collection().find_one(find_query).get("keywords", [])


def get_user_channels(user):
    find_query = {"user": user}
    return get_db_collection().find_one(find_query).get("channels", [])