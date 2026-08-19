from aiogram import Router, types
from buttons.inline import categories, product_list, product_card
from database.crud import get_product

router=Router()

@router.callback_query(lambda c: c.data=="menu")
async def menu(callback: types.CallbackQuery):
    await callback.message.edit_text("☕ <b>COFFEE MENYU</b>\n\nKategoriyani tanlang:",reply_markup=categories())
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("cat:"))
async def category(callback: types.CallbackQuery):
    cat=callback.data.split(":",1)[1]
    await callback.message.edit_text(f"☕ <b>{cat} ichimliklar</b>\n\nTanlang:",reply_markup=product_list(cat))
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("product:"))
async def product(callback: types.CallbackQuery):
    pid=int(callback.data.split(":")[1])
    p=get_product(pid)
    if not p:
        await callback.answer("Mahsulot topilmadi",show_alert=True); return
    text=(f"{p[5]} <b>{p[1]}</b>\n\n"
          f"💰 Narxi: <b>{p[3]:,} so'm</b>\n"
          f"📝 {p[4]}\n\n"
          "🔥 Sifatli ingredientlar • ⚡ Tez tayyorlanadi")
    await callback.message.edit_text(text,reply_markup=product_card(pid))
    await callback.answer()
