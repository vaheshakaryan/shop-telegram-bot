# Telegram E-Commerce Shop Bot 🛒

A professional Telegram bot for digital storefronts, built with **Python**, **Aiogram 3**, and **SQLite3**. This bot allows users to browse a product catalog, manage a simple cart, and place orders directly through the chat.

## 🚀 Key Features
- **Interactive Catalog:** Browse products categorized into different sections (Electronics, Clothes, etc.).
- **Inline Ordering:** Users can select items and start the checkout process using interactive inline buttons.
- **FSM Checkout (Finite State Machine):** A step-by-step ordering process (Name -> Phone -> Address).
- **Persistent Storage:** Uses **SQLite3** to store products, categories, and user orders.
- **Admin Notifications:** Instant alerts sent to the administrator whenever a new order is placed.
- **Purchase History:** A "Cart" feature that displays the user's last order details.

## 🛠 Tech Stack
- **Framework:** [Aiogram 3.x](https://docs.aiogram.dev/) (Asynchronous Telegram Bot API)
- **Database:** SQLite3 (Local relational database)
- **Language:** Python 3.10+
- **State Management:** FSM (Finite State Machine) for handling user input flow.

## 📁 Project Structure
- `bot.py` — The main entry point and message handlers.
- `keyboards.py` — Logic for Reply and Inline keyboards.
- `database.py` — SQLite3 database initialization and CRUD operations.
- `config.py` — Sensitive data (Bot Token, Admin ID).
- `shop.db` — Generated SQLite database file (automatically created on first run).

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/vaheshakaryan/shop-telegram-bot.git](https://github.com/vaheshakaryan/shop-telegram-bot.git)
   cd shop-telegram-bot