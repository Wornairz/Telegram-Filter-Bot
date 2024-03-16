from src.handlers import (
    add_channels,
    add_keywords,
    confirm_delete_channel,
    confirm_delete_keyword,
    get_add_channel_handler,
    get_add_keywords_handler,
    get_channel_list,
    get_keyword_list,
    get_remove_channel_handler,
    get_remove_keywords_handler,
    remove_channels,
    remove_keywords,
    start,
    stop_interact,
    __add_channels_state,
    __add_keywords_state,
)
from unittest.mock import AsyncMock, patch, MagicMock
import pytest
from src.handlers import button_handler_channel
from src.handlers import start, button_handler_channel
from unittest.mock import AsyncMock, patch, MagicMock
from telegram.ext import CommandHandler


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


@pytest.mark.asyncio
async def test_start():
    update = AsyncMock()
    context = AsyncMock()
    chat_id = 12345
    update.message.chat_id = chat_id
    update.message.reply_text = AsyncMock()
    with patch("src.handlers.create_user") as mock_create_user:
        mock_create_user.return_value = None
        await start(update, context)
        update.message.reply_text.assert_called_once_with(
            "Ciao! Sono il tuo bot. Sono in ascolto su diversi canali."
        )


@pytest.mark.asyncio
async def test_button_handler_channel():
    callback_query = AsyncMock()
    callback_query.data = "command?test_channel"
    callback_query.answer = AsyncMock()
    update = AsyncMock()
    update.callback_query = callback_query
    context = MagicMock()
    await button_handler_channel(update, context)
    callback_query.answer.assert_awaited_once()
    callback_query.edit_message_text.assert_awaited_once()


@pytest.mark.asyncio
async def test_button_handler_keyword():
    callback_query = AsyncMock()
    callback_query.data = "command?test_keyword"
    callback_query.answer = AsyncMock()
    update = AsyncMock()
    update.callback_query = callback_query
    context = MagicMock()
    reply_markup = MagicMock()
    with patch("src.handlers.InlineKeyboardMarkup", return_value=reply_markup):
        await button_handler_channel(update, context)
    callback_query.answer.assert_awaited_once()
    callback_query.edit_message_text.assert_awaited_once_with(
        text=f"Sei sicuro di voler cancellare 'test_keyword'?",
        reply_markup=reply_markup,
    )


@pytest.mark.asyncio
async def test_confirm_delete_keyword():
    callback_query = AsyncMock()
    callback_query.data = "command?test_keyword"
    callback_query.answer = AsyncMock()
    update = AsyncMock()
    update.callback_query = callback_query
    context = MagicMock()
    await button_handler_channel(update, context)
    callback_query.answer.assert_awaited_once()
    callback_query.edit_message_text.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_keyword_confirmation():
    query = MagicMock()
    query.data = "deleteKeyword?testKeyword"
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()
    update = MagicMock()
    update.callback_query = query
    update.effective_chat.id = 12345
    context = MagicMock()
    context.bot = MagicMock()
    with patch("src.handlers.remove_keyword") as mock_remove_keyword:
        await confirm_delete_keyword(update, context)
        query.edit_message_text.assert_called_once_with(
            text="Keyword 'testKeyword' cancellata."
        )


@pytest.mark.asyncio
async def test_delete_channel_confirmation():
    query = MagicMock()
    query.data = "deleteChannel?testChannel"
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()
    update = MagicMock()
    update.callback_query = query
    update.effective_chat.id = 12345
    context = MagicMock()
    context.bot = MagicMock()
    with patch("src.handlers.remove_channel") as mock_remove_channel:
        await confirm_delete_channel(update, context)
        query.edit_message_text.assert_called_once_with(
            text="Canale 'testChannel' cancellato."
        )


@pytest.mark.asyncio
async def test_cancel_deletion():
    query = MagicMock()
    query.data = "cancel"
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()
    update = MagicMock()
    update.callback_query = query
    context = MagicMock()
    context.bot = MagicMock()
    await confirm_delete_keyword(update, context)
    query.edit_message_text.assert_called_once_with(text="Cancellazione annullata.")


@pytest.mark.asyncio
async def test_confirm_delete_channel():
    callback_query = AsyncMock()
    callback_query.data = "command?test_channel"
    callback_query.answer = AsyncMock()
    update = AsyncMock()
    update.callback_query = callback_query
    context = MagicMock()
    await button_handler_channel(update, context)
    callback_query.answer.assert_awaited_once()
    callback_query.edit_message_text.assert_awaited_once()


@pytest.mark.asyncio
@patch("src.functions.get_user_channels")
async def test_get_channel_list(mock_get_user_channels):
    mock_get_user_channels.return_value = ["channel1", "channel2"]
    update = AsyncMock()
    context = MagicMock()
    with patch("src.functions.get_user") as mock_get_user:
        mock_get_user.return_value = {
            "user": "test_user_id",
            "channels": ["channel1", "channel2"],
        }
        await get_channel_list(update, context)
        update.message.reply_text.assert_called_once_with(
            "Canali tracciati:\n<a href='https://t.me/channel1'>channel1</a>\n<a href='https://t.me/channel2'>channel2</a>\n",
            parse_mode="HTML",
            disable_web_page_preview=True,
        )


@pytest.mark.asyncio
@patch("src.functions.get_user_keywords")
async def test_get_keyword_list(mock_get_user_keywords):
    mock_get_user_keywords.return_value = ["keyword1", "keyword2"]
    update = AsyncMock()
    context = MagicMock()
    with patch("src.functions.get_user") as mock_get_user:
        mock_get_user.return_value = {
            "user": "test_user_id",
            "keywords": ["keyword1", "keyword2"],
        }
        await get_keyword_list(update, context)
        update.message.reply_text.assert_called_once_with(
            "Keywords tracciate:\n•keyword1\n• keyword2"
        )


@pytest.mark.asyncio
async def test_get_remove_channel_handler():
    update = AsyncMock()
    context = MagicMock()
    with patch("src.functions.get_user_channels") as mock_get_user_channels:
        mock_get_user_channels.return_value = ["channel1", "channel2"]
        with patch("src.functions.get_user") as mock_get_user:
            mock_get_user.return_value = {
                "user": "test_user_id",
                "channels": ["channel1", "channel2"],
            }
            with patch(
                "src.handlers.InlineKeyboardButton"
            ) as mock_inline_keyboard_button:
                with patch(
                    "src.handlers.InlineKeyboardMarkup"
                ) as mock_inline_keyboard_markup:
                    await get_remove_channel_handler(update, context)
                    update.message.reply_text.assert_called_once_with(
                        "Seleziona il canale da rimuovere",
                        reply_markup=mock_inline_keyboard_markup.return_value,
                    )


@pytest.mark.asyncio
async def test_get_add_channel_handler():
    conversationHandler = get_add_channel_handler()
    assert conversationHandler.entry_points[0].callback == add_channels
    assert conversationHandler.states[0][0].callback == __add_channels_state


@pytest.mark.asyncio
async def test_get_add_keywords_handler():
    conversationHandler = get_add_keywords_handler()
    assert conversationHandler.entry_points[0].callback == add_keywords


@pytest.mark.asyncio
async def test_get_remove_keywords_handler():
    update = AsyncMock()
    context = MagicMock()
    with patch("src.functions.get_user_keywords") as mock_get_user_keywords:
        mock_get_user_keywords.return_value = ["keyword1", "keyword2"]
        with patch("src.functions.get_user") as mock_get_user:
            mock_get_user.return_value = {
                "user": "test_user_id",
                "keywords": ["keyword1", "keyword2"],
            }
            with patch(
                "src.handlers.InlineKeyboardButton"
            ) as mock_inline_keyboard_button:
                with patch(
                    "src.handlers.InlineKeyboardMarkup"
                ) as mock_inline_keyboard_markup:
                    await get_remove_keywords_handler(update, context)
                    update.message.reply_text.assert_called_once_with(
                        "Seleziona la keyword da rimuovere",
                        reply_markup=mock_inline_keyboard_markup.return_value,
                    )


@pytest.mark.asyncio
async def test_add_channels():
    update = AsyncMock()
    context = MagicMock()
    await add_channels(update, context)
    update.message.reply_text.assert_called_once_with(
        "Inserisci i canali che vorresti tracciare. Quando hai finito usa /stop."
    )


@pytest.mark.asyncio
async def test_remove_channels():
    update = AsyncMock()
    context = MagicMock()
    await remove_channels(update, context)
    update.message.reply_text.assert_called_once_with(
        "Rimuovi i canali che non vuoi più tracciare. Quando hai finito usa /stop."
    )


@pytest.mark.asyncio
async def test_add_keywords():
    update = AsyncMock()
    context = MagicMock()
    await add_keywords(update, context)
    update.message.reply_text.assert_called_once_with(
        "Inserisci le keywords che vorresti tracciare. Quando hai finito usa /stop."
    )


@pytest.mark.asyncio
async def test_remove_keywords():
    update = AsyncMock()
    context = MagicMock()
    await remove_keywords(update, context)
    update.message.reply_text.assert_called_once_with(
        "Rimuovi le keywords che non vuoi più tracciare. Quando hai finito usa /stop."
    )


@pytest.mark.asyncio
async def test_stop_interact():
    update = AsyncMock()
    context = MagicMock()
    await stop_interact(update, context)
    update.message.reply_text.assert_called_once_with("Ok, basta")
