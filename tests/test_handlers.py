from src.handlers import (
    add_channels,
    add_keywords,
    get_channel_list,
    get_keyword_list,
    get_remove_channel_handler,
    get_remove_keywords_handler,
    remove_channels,
    remove_keywords,
    start,
)
from unittest.mock import AsyncMock, patch, MagicMock
import pytest
from src.handlers import button_handler_channel
from src.handlers import start, button_handler_channel
from unittest.mock import AsyncMock, patch, MagicMock


@pytest.mark.asyncio
async def test_start():
    update = AsyncMock()
    context = AsyncMock()
    chat_id = 12345
    update.message.chat_id = chat_id
    update.message.reply_text = AsyncMock()
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
