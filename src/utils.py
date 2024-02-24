from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_keyboard(items, items_per_row, callback_filter):
    keyboard = []
    for i in range(0, len(items), items_per_row):
        row = [InlineKeyboardButton(items[j], callback_data=callback_filter+'?'+items[j]) for j in range(i, min(i + items_per_row, len(items)))]
        keyboard.append(row)
    return keyboard