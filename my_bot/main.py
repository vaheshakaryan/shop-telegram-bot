

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
from aiogram import Router, types
from aiogram.filters import Command
from config import TOKEN, ADMIN_ID

router = Router()



@router.message(Command("start"))
async def start_handler(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Hello, my boss")
    else:
        await message.answer("Hello! You are not the boss.")

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
    db.update_order(callback.from_user.id, callback.from_user.username, "chosen_product", callback.data)
    await callback.message.answer("Enter your Full Name:")
    await state.set_state(Checkout.name)

@dp.message(Checkout.name)
async def get_name(message: Message, state: FSMContext):
    db.update_order(message.from_user.id, message.from_user.username, "full_name", message.text)
    await state.update_data(name=message.text)
    await message.answer("Enter your phone number:")
    await state.set_state(Checkout.phone)

@dp.message(Checkout.phone)
async def get_phone(message: Message, state: FSMContext):
    db.update_order(message.from_user.id, message.from_user.username, "phone", message.text)
    await state.update_data(phone=message.text)
    await message.answer("Enter delivery address:")
    await state.set_state(Checkout.address)

@dp.message(Checkout.address)
async def get_address(message: Message, state: FSMContext):
    db.update_order(message.from_user.id, message.from_user.username, "address", message.text)
    
    data = await state.get_data()
    
    order_text = (f"🔔 NEW ORDER!\n"
                  f"👤 Name: {data.get('name')}\n"
                  f"📞 Phone: {data.get('phone')}\n"  
                  f"📍 Address: {message.text}")      
    
    try:
        await message.bot.send_message(ADMIN_ID, order_text)
        await message.answer("Order complete! Everything saved in DB.", reply_markup=kb.main_menu())
    except Exception as e:
        await message.answer("Order saved, but admin not notified.")
    
    await state.clear()

async def main():
    db.db_start() 
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
