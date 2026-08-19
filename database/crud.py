import sqlite3
from datetime import datetime

DB = "coffee.db"

def connect():
    return sqlite3.connect(DB)

def init_db():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            username TEXT,
            created_at TEXT NOT NULL
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price INTEGER NOT NULL,
            description TEXT,
            emoji TEXT DEFAULT '☕'
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            full_name TEXT,
            phone TEXT,
            address TEXT,
            items TEXT NOT NULL,
            total INTEGER NOT NULL,
            status TEXT DEFAULT 'Yangi',
            created_at TEXT NOT NULL
        )""")
        conn.commit()
    seed_products()

def seed_products():
    with connect() as conn:
        cur=conn.cursor()
        cur.execute("SELECT COUNT(*) FROM products")
        if cur.fetchone()[0]: return
        products=[
            ("Espresso","Issiq",18000,"Kuchli va klassik qahva","☕"),
            ("Cappuccino","Issiq",26000,"Mayin sut ko'pigi bilan","🥛"),
            ("Latte","Issiq",28000,"Yumshoq va qaymoqli latte","🤎"),
            ("Americano","Issiq",22000,"Toza, yengil va tetiklantiruvchi","☕"),
            ("Mocha","Maxsus",32000,"Shokolad va qahvaning ajoyib uyg'unligi","🍫"),
            ("Caramel Macchiato","Maxsus",34000,"Karamel ta'mi bilan shirin coffee","🍯"),
            ("Iced Latte","Sovuq",29000,"Muzdek, yumshoq va tetiklantiruvchi","🧊"),
            ("Iced Americano","Sovuq",24000,"Sovuq klassika","❄️"),
            ("Hot Chocolate","Maxsus",27000,"Issiq shokoladli ichimlik","🍫"),
            ("Cheesecake","Desert",30000,"Qahvaga mos yumshoq desert","🍰"),
        ]
        cur.executemany(
            "INSERT INTO products(name,category,price,description,emoji) VALUES(?,?,?,?,?)",
            products
        )
        conn.commit()

def add_user(user_id, full_name, username):
    with connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO users(user_id,full_name,username,created_at) VALUES(?,?,?,?)",
            (user_id,full_name,username,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()

def get_user(user_id):
    with connect() as conn:
        return conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()

def get_products(category=None):
    with connect() as conn:
        if category:
            return conn.execute(
                "SELECT id,name,category,price,description,emoji FROM products WHERE category=? ORDER BY id",
                (category,)
            ).fetchall()
        return conn.execute(
            "SELECT id,name,category,price,description,emoji FROM products ORDER BY id"
        ).fetchall()

def get_product(product_id):
    with connect() as conn:
        return conn.execute(
            "SELECT id,name,category,price,description,emoji FROM products WHERE id=?",
            (product_id,)
        ).fetchone()

def add_order(user_id, full_name, phone, address, items, total):
    with connect() as conn:
        cur=conn.cursor()
        cur.execute(
            "INSERT INTO orders(user_id,full_name,phone,address,items,total,status,created_at) VALUES(?,?,?,?,?,?,?,?)",
            (user_id,full_name,phone,address,items,total,"Yangi",
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        return cur.lastrowid

def get_orders(limit=30):
    with connect() as conn:
        return conn.execute(
            "SELECT id,user_id,full_name,phone,address,items,total,status,created_at FROM orders ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()

def set_order_status(order_id,status):
    with connect() as conn:
        conn.execute("UPDATE orders SET status=? WHERE id=?", (status,order_id))
        conn.commit()

def stats():
    with connect() as conn:
        users=conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        orders=conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        revenue=conn.execute("SELECT COALESCE(SUM(total),0) FROM orders WHERE status!='Bekor qilindi'").fetchone()[0]
        return users,orders,revenue


def get_user_orders(user_id, limit=20):
    with connect() as conn:
        return conn.execute(
            "SELECT id,items,total,status,created_at FROM orders WHERE user_id=? ORDER BY id DESC LIMIT ?",
            (user_id, limit)
        ).fetchall()
