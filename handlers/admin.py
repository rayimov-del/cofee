from aiogram import Router, types
from aiogram.filters import Command
from config import ADMIN_ID
from database.crud import stats,get_orders
from buttons.inline import admin_menu

router=Router()

@router.message(Command("admin"))
async def admin(message:types.Message):
    if message.from_user.id!=ADMIN_ID: return
    await message.answer("🔐 <b>COFFEE ADMIN</b>\n\nPanel tayyor.",reply_markup=admin_menu())

@router.callback_query(lambda c:c.data=="admin_stats")
async def admin_stats(callback:types.CallbackQuery):
    if callback.from_user.id!=ADMIN_ID: return
    u,o,r=stats()
    await callback.message.edit_text(
        f"📊 <b>STATISTIKA</b>\n\n👥 Userlar: {u}\n📦 Buyurtmalar: {o}\n💰 Tushum: {r:,} so'm".replace(","," "),
        reply_markup=admin_menu()
    )
    await callback.answer()

@router.callback_query(lambda c:c.data=="admin_orders")
async def admin_orders(callback:types.CallbackQuery):
    if callback.from_user.id!=ADMIN_ID: return
    orders=get_orders()
    if not orders:
        text="📦 Hozircha buyurtmalar yo'q."
    else:
        text="📦 <b>SO'NGGI BUYURTMALAR</b>\n\n"
        for x in orders[:10]:
            text += f"#{x[0]} • {x[2]}\n☕ {x[5]}\n💰 {x[6]:,} so'm • {x[7]}\n\n".replace(","," ")
    await callback.message.edit_text(text,reply_markup=admin_menu())
    await callback.answer()
