# import asyncio
# import logging
# import sys

# from aiogram import Bot, Dispatcher, types, F
# from aiogram.filters import CommandStart
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.types import Message, CallbackQuery

# import database as db
# import keyboards as kb

# # --- FILL YOUR DATA HERE ---
# TOKEN = "8785450419:AAG2HKChOD0WpFT5yrSl2qh1TZCCiOORAdg"
# ADMIN_ID = 1371857311 # Your Telegram ID
# # ---------------------------

# dp = Dispatcher()

# class Checkout(StatesGroup):
#     name = State()
#     phone = State()
#     address = State()

# @dp.message(CommandStart())
# async def cmd_start(message: Message):
#     db.db_start()
#     await message.answer("Welcome to our Shop! Please choose an option:", reply_markup=kb.main_menu())

# @dp.message(F.text == "🛍 Catalog")
# async def show_cats(message: Message):
#     await message.answer("Select a category:", reply_markup=kb.categories_keyboard())

# @dp.callback_query(F.data.startswith('cat_'))
# async def show_items(callback: CallbackQuery):
#     cat_id = callback.data.split('_')[1]
#     items = db.get_items(cat_id)
#     if not items:
#         await callback.message.answer("This category is empty.")
#     else:
#         await callback.message.answer("Available products:", reply_markup=kb.items_keyboard(items))

# @dp.callback_query(F.data.startswith('buy_'))
# async def start_order(callback: CallbackQuery, state: FSMContext):
#     await callback.message.answer("To place an order, please enter your Full Name:")
#     await state.set_state(Checkout.name)

# @dp.message(Checkout.name)
# async def get_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.answer("Please enter your phone number:")
#     await state.set_state(Checkout.phone)

# @dp.message(Checkout.phone)
# async def get_phone(message: Message, state: FSMContext):
#     await state.update_data(phone=message.text)
#     await message.answer("Finally, please enter your delivery address:")
#     await state.set_state(Checkout.address)

# @dp.message(Checkout.address)
# async def get_address(message: Message, state: FSMContext):
#     data = await state.get_data()
#     order_details = (f"🔔 NEW ORDER!\n"
#                      f"👤 Name: {data['name']}\n"
#                      f"📞 Phone: {data['phone']}\n"
#                      f"📍 Address: {message.text}")
    
#     try:
#         await message.bot.send_message(ADMIN_ID, order_details)
#         await message.answer("Thank you! Your order has been placed.", reply_markup=kb.main_menu())
#     except Exception as e:
#         await message.answer("Order received, but failed to notify admin.")
#         print(f"Error: {e}")
    
#     await state.clear()

# async def main():
#     bot = Bot(token=TOKEN)
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())

import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import database as db
import keyboards as kb

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

if message.from_user.id == ADMIN_ID:
    await message.answer("Hello, my boss")


dp = Dispatcher()

class Checkout(StatesGroup):
    name = State()
    phone = State()
    address = State()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Welcome to our Shop!", reply_markup=kb.main_menu())

@dp.message(F.text == "🛍 Catalog")
async def show_cats(message: Message):
    await message.answer("Select a category:", reply_markup=kb.categories_keyboard())


@dp.message(F.text == "🛒 Cart")
async def show_cart(message: Message):
    order = db.get_last_order(message.from_user.id)
    
    if order:
        # order[0] is Name, order[1] is Price, order[2] is Full Name...
        response = (f"📋 **Last Purchased Item:**\n\n"
                    f"📦 **Product:** {order[0]}\n"
                    f"💰 **Price:** ${order[1]}\n"
                    f"---------------------------\n"
                    f"👤 **Customer:** {order[2]}\n"
                    f"📞 **Phone:** {order[3]}\n"
                    f"📍 **Address:** {order[4]}")
        await message.answer(response, parse_mode='Markdown')
    else:
        await message.answer("🛒 Your cart is empty!")


@dp.callback_query(F.data.startswith('cat_'))
async def show_items(callback: CallbackQuery):
    cat_id = callback.data.split('_')[1]
    items = db.get_items(cat_id)
    if not items:
        await callback.message.answer("This category is empty.")
    else:
        await callback.message.answer("Available products:", reply_markup=kb.items_keyboard(items))

@dp.callback_query(F.data.startswith('buy_'))
async def start_order(callback: CallbackQuery, state: FSMContext):
    # Գրանցում ենք ընտրված ապրանքը
    db.update_order(callback.from_user.id, callback.from_user.username, "chosen_product", callback.data)
    await callback.message.answer("Enter your Full Name:")
    await state.set_state(Checkout.name)

@dp.message(Checkout.name)
async def get_name(message: Message, state: FSMContext):
    # Գրանցում ենք անունը
    db.update_order(message.from_user.id, message.from_user.username, "full_name", message.text)
    await state.update_data(name=message.text)
    await message.answer("Enter your phone number:")
    await state.set_state(Checkout.phone)

@dp.message(Checkout.phone)
async def get_phone(message: Message, state: FSMContext):
    # Գրանցում ենք հեռախոսը
    db.update_order(message.from_user.id, message.from_user.username, "phone", message.text)
    await state.update_data(phone=message.text)
    await message.answer("Enter delivery address:")
    await state.set_state(Checkout.address)

@dp.message(Checkout.address)
async def get_address(message: Message, state: FSMContext):
    # 1. Գրանցում ենք հասցեն բազայում
    db.update_order(message.from_user.id, message.from_user.username, "address", message.text)
    
    # 2. Վերցնում ենք նախորդ քայլերում պահված տվյալները (անունը և հեռախոսը)
    data = await state.get_data()
    
    # 3. Սարքում ենք ճիշտ տեքստը
    order_text = (f"🔔 NEW ORDER!\n"
                  f"👤 Name: {data.get('name')}\n"
                  f"📞 Phone: {data.get('phone')}\n"  # Հեռախոսը վերցնում ենք data-ից
                  f"📍 Address: {message.text}")       # Հասցեն հենց այս հաղորդագրությունն է
    
    try:
        await message.bot.send_message(ADMIN_ID, order_text)
        await message.answer("Order complete! Everything saved in DB.", reply_markup=kb.main_menu())
    except Exception as e:
        await message.answer("Order saved, but admin not notified.")
    
    await state.clear()

async def main():
    db.db_start() # Միացնում ենք բազան բոտը միանալուն պես
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())