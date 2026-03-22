import sqlite3

def db_start():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    
    
    cursor.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, name TEXT)")
    
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS items 
                   (id INTEGER PRIMARY KEY, category_id INTEGER, name TEXT, desc TEXT, price REAL)""")
    
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS orders 
                   (user_id INTEGER PRIMARY KEY, 
                    username TEXT, 
                    chosen_product TEXT, 
                    full_name TEXT, 
                    phone TEXT, 
                    address TEXT)""")
    
    
    cursor.execute("SELECT count(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO categories (name) VALUES (?)", [('Electronics',), ('Clothes',), ('Accessories',)])
        
        sample_items = [
            (1, 'iPhone 15 Pro', 'Apple smartphone', 999.99),
            (1, 'MacBook Air', 'Laptop', 1200.00),
            (2, 'Nike Hoodie', 'Sportswear', 75.0),
            (3, 'Rolex Watch', 'Luxury', 5000.0)
        ]
        cursor.executemany("INSERT INTO items (category_id, name, desc, price) VALUES (?, ?, ?, ?)", sample_items)
        print("Database initialized with sample data!")
    
    conn.commit()
    conn.close()

def update_order(user_id, username, column, value):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO orders (user_id, username) VALUES (?, ?)", (user_id, username))
    
    cursor.execute(f"UPDATE orders SET {column} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()

def get_categories():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories")
    data = cursor.fetchall()
    conn.close()
    return data

def get_items(cat_id):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE category_id = ?", (cat_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def get_last_order(user_id):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
   
    query = """
    SELECT items.name, items.price, orders.full_name, orders.phone, orders.address 
    FROM orders 
    JOIN items ON orders.chosen_product = 'buy_' || items.id
    WHERE orders.user_id = ?
    """
    cursor.execute(query, (user_id,))
    data = cursor.fetchone()
    conn.close()
    return data
