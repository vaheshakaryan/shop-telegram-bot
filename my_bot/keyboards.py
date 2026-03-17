from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database as db

def main_menu():
    # Սա ստեղծում է հիմնական մենյուն՝ Catalog և Cart կոճակներով
    kb = [
        [
            KeyboardButton(text="🛍 Catalog"),
            KeyboardButton(text="🛒 Cart")
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def categories_keyboard():
    builder = InlineKeyboardBuilder()
    categories = db.get_categories()
    for cat in categories:
        # cat[0] - ID, cat[1] - Name
        builder.add(InlineKeyboardButton(text=str(cat[1]), callback_data=f"cat_{cat[0]}"))
    builder.adjust(2) # 2 կոճակ ամեն տողում
    return builder.as_markup()

def items_keyboard(items):
    builder = InlineKeyboardBuilder()
    for item in items:
        # item[2] - Name, item[4] - Price
        builder.add(InlineKeyboardButton(text=f"{item[2]} - {item[4]}$", callback_data=f"buy_{item[0]}"))
    builder.adjust(1) # Ամեն ապրանք իր տողում
    return builder.as_markup()