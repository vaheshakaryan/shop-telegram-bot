import logging
import aiosqlite
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

# Կարգավորումներ
TOKEN = "8778873310:AAEhXuHxDeobhYPZrfPHlSNL3DgnsmpD6QI"
ADMIN_ID = 1371857311
DB_PATH = "applications.db"

# 1. Բազայի սկզբնավորում (ստեղծում ենք աղյուսակը, եթե չկա)
async def post_init(application):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                username TEXT,
                data TEXT,
                date TEXT
            )
        """)
        await db.commit()
    print("Database is ready and table is checked.")

# 2. Տվյալների պահպանման ֆունկցիա
async def save_to_db(name, username, data):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO applications (name, username, data, date) VALUES (?, ?, ?, ?)",
            (name, username, str(data), current_time)
        )
        await db.commit()

# --- Բոտի գործողությունները ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["To choose auto parts", "Contact manager"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Welcome to the auto parts bot \nChoose an action.",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    username = f"@{user.username}" if user.username else "No Username"

    # Տրամաբանական ճյուղավորում
    if text == "To choose auto parts":
        # Այստեղ բազայում ոչինչ չենք գրում, ուղղակի հարցնում ենք տվյալները
        await update.message.reply_text(
            "Send car details.\n\n"
            "Mark\n"
            "Model\n"
            "Year\n"
            "VIN code or technical drawing"
        )

    elif text == "Contact manager":
        # Գրանցում ենք մենեջերի հետ կապի հարցումը բազայում
        await save_to_db(user.first_name, username, "Contact manager request")

        # Ուղարկում ենք ծանուցում մենեջերին
        message = f"Customer wants to contact the manager\n\nCustomer: {user.first_name}\nUsername: {username}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=message)
        
        await update.message.reply_text("Your request has been sent to the manager.")

    else:
        # Սա այն դեպքն է, երբ հաճախորդը ուղարկել է մեքենայի տվյալները
        # Պահպանում ենք տվյալները մեկ տողով
        await save_to_db(user.first_name, username, text)

        # Ծանուցում մենեջերին
        message = f"New application\n\nCustomer: {user.first_name}\nUsername: {username}\n\nData:\n{text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=message)
        
        await update.message.reply_text(
            "Your application has been accepted.\n"
            "Manager will contact you soon."
        )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = f"@{user.username}" if user.username else "No Username"
    photo_id = update.message.photo[-1].file_id

    # Պահպանում ենք նշում բազայում, որ նկար է ուղարկվել
    await save_to_db(user.first_name, username, "Drawing/Photo sent")

    caption = f"New application (drawing)\n\nCustomer: {user.first_name}\nUsername: {username}"

    await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo_id, caption=caption)
    await update.message.reply_text("Picture received.\nManager will contact you soon.")

# --- Բոտի մեկնարկ ---

if __name__ == "__main__":
    # Օգտագործում ենք post_init բազան պատրաստելու համար
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    # Ավելացնում ենք հենդլերները
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot is running...")
    app.run_polling()