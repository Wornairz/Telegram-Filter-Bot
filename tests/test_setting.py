from src.settings import get_logger
from src.settings import get_telegram_application
from src.settings import get_telegram_client
import logging
import pytest
from unittest.mock import patch, MagicMock
from telethon import TelegramClient
from telegram.ext import Application


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


@patch("src.settings.telegram_client", new_callable=MagicMock)
def test_get_telegram_client_returns_telegram_client_instance(mock_telegram_client):
    mock_telegram_client_instance = MagicMock(spec=TelegramClient)
    mock_telegram_client.return_value = mock_telegram_client_instance
    returned_client = get_telegram_client()
    assert isinstance(
        returned_client, MagicMock
    ), "get_telegram_client should return an instance of TelegramClient"


@patch("src.settings.telegram_application", new_callable=MagicMock)
def test_get_telegram_application_returns_application_instance(
    mocked_telegram_application,
):
    mocked_application_instance = MagicMock(spec=Application)
    mocked_telegram_application.return_value = mocked_application_instance
    returned_application = get_telegram_application()
    assert (
        returned_application == mocked_telegram_application
    ), "get_telegram_application should return the mocked Application instance"
