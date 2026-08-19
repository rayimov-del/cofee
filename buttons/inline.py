from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.crud import get_products

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="☕ Menyu", callback_data="menu"),
         InlineKeyboardButton(text="🛒 Savatcha", callback_data="cart")],
        [InlineKeyboardButton(text="🤖 Bot tafsiyalar", callback_data="coffee_ai"),
         InlineKeyboardButton(text="📋 Mening buyurtmalarim", callback_data="orders")],
        [InlineKeyboardButton(text="ℹ️ Coffee haqida", callback_data="about")]
    ])

def categories():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="☕ Issiq", callback_data="cat:Issiq"),
         InlineKeyboardButton(text="🧊 Sovuq", callback_data="cat:Sovuq")],
        [InlineKeyboardButton(text="✨ Maxsus", callback_data="cat:Maxsus"),
         InlineKeyboardButton(text="🍰 Desert", callback_data="cat:Desert")],
        [InlineKeyboardButton(text="🔙 Bosh menyu", callback_data="home")]
    ])

def product_list(category):
    products=get_products(category)
    rows=[]
    for p in products:
        rows.append([InlineKeyboardButton(
            text=f"{p[5]} {p[1]} — {p[3]:,} so'm".replace(",", " "),
            callback_data=f"product:{p[0]}"
        )])
    rows.append([InlineKeyboardButton(text="🔙 Kategoriyalar", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def product_card(product_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Savatchaga qo'shish", callback_data=f"add:{product_id}")],
        [InlineKeyboardButton(text="🔙 Menyuga", callback_data="menu"),
         InlineKeyboardButton(text="🛒 Savatcha", callback_data="cart")]
    ])

def cart_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Buyurtma berish", callback_data="checkout")],
        [InlineKeyboardButton(text="🗑 Savatchani tozalash", callback_data="clear_cart")],
        [InlineKeyboardButton(text="☕ Menyuga qaytish", callback_data="menu")]
    ])

def admin_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats"),
         InlineKeyboardButton(text="📦 Buyurtmalar", callback_data="admin_orders")],
        [InlineKeyboardButton(text="☕ Menyuni ko'rish", callback_data="menu")]
    ])
