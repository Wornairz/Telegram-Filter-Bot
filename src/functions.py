from .settings import get_db_collection


def get_all_users_data() -> list:
    return get_db_collection().find()


def get_user_keywords(user) -> list:
    user_document = get_user(user)
    if user_document is None:
        return []
    return user_document.get("keywords", [])


def get_user(user_id) -> dict:
    find_query = {"user": user_id}
    return get_db_collection().find_one(find_query)


def get_user_channels(user_id) -> list:
    user_document = get_user(user_id)
    if user_document is None:
        return []
    return user_document.get("channels", [])


def remove_channel(user, channel) -> None:
    find_query = {"user": user}
    get_db_collection().update_one(find_query, {"$pull": {"channels": channel}})


def remove_keyword(user, keyword) -> None:
    find_query = {"user": user}
    get_db_collection().update_one(find_query, {"$pull": {"keywords": keyword}})


def create_user(user) -> None:
    find_query = {"user": user}
    get_db_collection().update_one(find_query, {"$set": {"user": user}}, upsert=True)
