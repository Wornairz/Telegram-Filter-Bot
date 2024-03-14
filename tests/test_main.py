import pytest
from unittest.mock import MagicMock, patch
from main import (
    get_channel_identifier,
    is_user_subscribed_to_channel,
)


@pytest.mark.parametrize(
    "user_channels,channel_identifier,expected_result",
    [
        (["channel1", "channel2", "channel3"], "channel2", True),
        (["channel1", "channel3"], "channel2", False),
        ([], "channel1", False),
    ],
)
@patch("src.functions.get_user_channels")
def test_is_user_subscribed_to_channel(
    mock_get_user_channels, user_channels, channel_identifier, expected_result
):
    mock_get_user_channels.return_value = user_channels
    with patch("src.functions.get_user") as mock_get_user:
        mock_get_user.return_value = {"user": "test_user_id", "channels": user_channels}
        result = is_user_subscribed_to_channel("test_user_id", channel_identifier)
        assert (
            result == expected_result
        ), f"Expected {expected_result} but got {result} when checking subscription to {channel_identifier}"


@pytest.mark.parametrize(
    "username, chat_id, expected",
    [
        ("testchannel", None, "testchannel"),  # Scenario with username
        (None, 123456, 123456),  # Scenario without username, using chat_id
    ],
)
def test_get_channel_identifier(username, chat_id, expected):
    # Create a mock Message object with necessary attributes
    mock_message = MagicMock()
    mock_message.chat.username = username
    mock_message.chat_id = chat_id
    if username is None:
        mock_message.chat = None
    identifier = get_channel_identifier(mock_message)
    assert (
        identifier == expected
    ), f"Expected identifier to be {expected}, got {identifier}"
