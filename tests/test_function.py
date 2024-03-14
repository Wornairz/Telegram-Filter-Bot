import pytest
from unittest.mock import patch, MagicMock
from src.functions import (
    get_all_users_data,
    get_user_keywords,
    get_user_keywords,
    remove_channel,
    remove_keyword,
    create_user,
    create_user,
    get_user,
    get_user_channels,
    remove_channel,
    remove_keyword,
)


@pytest.fixture
def mock_db_collection():
    with patch("src.functions.get_db_collection") as mock:
        collection_mock = MagicMock()
        mock.return_value = collection_mock
        yield collection_mock


def test_get_all_users_data(mock_db_collection):
    get_all_users_data()
    mock_db_collection.find.assert_called_once_with()


@pytest.mark.parametrize(
    "user_document,expected",
    [
        ({"keywords": ["keyword1", "keyword2"]}, ["keyword1", "keyword2"]),
        ({}, []),
        (None, []),
    ],
)
def test_get_user_keywords(mock_db_collection, user_document, expected):
    user = "test_user"
    mock_db_collection.find_one.return_value = user_document
    keywords = get_user_keywords(user)
    assert keywords == expected
    mock_db_collection.find_one.assert_called_once_with({"user": user})


def test_get_user_found(mock_db_collection):
    user_id = "test_user_id"
    expected_user_doc = {"user": user_id, "name": "Test User"}
    mock_db_collection.find_one.return_value = expected_user_doc
    result = get_user(user_id)
    assert result == expected_user_doc
    mock_db_collection.find_one.assert_called_once_with({"user": user_id})


def test_get_user_not_found(mock_db_collection):
    user_id = "nonexistent_user_id"
    mock_db_collection.find_one.return_value = None
    result = get_user(user_id)
    assert result is None
    mock_db_collection.find_one.assert_called_once_with({"user": user_id})


@pytest.mark.parametrize(
    "user_document,expected",
    [
        (None, []),
        ({"channels": ["channel1", "channel2"]}, ["channel1", "channel2"]),
        ({}, []),
    ],
)
def test_get_user_channels(user_document, expected):
    with patch("src.functions.get_user", return_value=user_document):
        channels = get_user_channels("dummy_user_id")
        assert channels == expected


def test_remove_channel(mock_db_collection):
    user = "test_user"
    channel = "test_channel"
    remove_channel(user, channel)
    mock_db_collection.update_one.assert_called_once_with(
        {"user": user}, {"$pull": {"channels": channel}}
    )


def test_remove_keyword(mock_db_collection):
    user = "test_user"
    keyword = "test_keyword"
    remove_keyword(user, keyword)
    mock_db_collection.update_one.assert_called_once_with(
        {"user": user}, {"$pull": {"keywords": keyword}}
    )


def test_create_user(mock_db_collection):
    user = "test_user"
    create_user(user)
    mock_db_collection.update_one.assert_called_once_with(
        {"user": user}, {"$set": {"user": user}}, upsert=True
    )
