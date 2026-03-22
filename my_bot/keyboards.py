from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database as db

def main_menu():
   
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
        
        builder.add(InlineKeyboardButton(text=str(cat[1]), callback_data=f"cat_{cat[0]}"))
    builder.adjust(2)
    return builder.as_markup()

def items_keyboard(items):
    builder = InlineKeyboardBuilder()
    for item in items:
       
        builder.add(InlineKeyboardButton(text=f"{item[2]} - {item[4]}$", callback_data=f"buy_{item[0]}"))
    builder.adjust(1) 
    return builder.as_markup()
