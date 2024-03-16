from src.settings import get_logger
import logging
import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_db_collection():
    with patch("src.handlers.get_db_collection") as mock:
        collection_mock = MagicMock()
        mock.return_value = collection_mock
        yield collection_mock


@pytest.fixture
def mock_telegram_client():
    with patch("src.settings.get_telegram_client") as telegram_mock:
        telegram_client_mock = MagicMock()
        telegram_mock.return_value = telegram_client_mock
        yield telegram_client_mock


def test_get_logger_returns_logger_instance():
    logger = get_logger()
    assert isinstance(
        logger, logging.Logger
    ), "get_logger should return an instance of logging.Logger"


def test_get_logger_returns_same_logger_instance_for_module():
    logger1 = get_logger()
    logger2 = get_logger()
    assert (
        logger1 is logger2
    ), "get_logger should return the same logger instance for the module on repeated calls"
