from telegram import InlineKeyboardButton
from src.utils import create_keyboard


def test_create_keyboard():
    items = ["item1", "item2", "item3", "item4", "item5"]
    items_per_row = 2
    callback_filter = "filter"

    expected_keyboard = [
        [
            InlineKeyboardButton("item1", callback_data="filter?item1"),
            InlineKeyboardButton("item2", callback_data="filter?item2"),
        ],
        [
            InlineKeyboardButton("item3", callback_data="filter?item3"),
            InlineKeyboardButton("item4", callback_data="filter?item4"),
        ],
        [InlineKeyboardButton("item5", callback_data="filter?item5")],
    ]

    assert create_keyboard(items, items_per_row, callback_filter) == expected_keyboard
