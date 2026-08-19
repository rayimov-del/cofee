from aiogram import Router, types
from buttons.inline import main_menu
from database.crud import get_user_orders

router = Router()

@router.callback_query(lambda c: c.data == "orders")
async def my_orders(callback: types.CallbackQuery):
    orders = get_user_orders(callback.from_user.id)

    if not orders:
        await callback.message.edit_text(
            "📦 <b>Mening buyurtmalarim</b>\n\n"
            "Sizda hali buyurtma yo'q.\n"
            "☕ Menyudan coffee tanlab buyurtma bering!",
            reply_markup=main_menu()
        )
    else:
        text = "📦 <b>MENING BUYURTMALARIM</b>\n\n"
        for order_id, items, total, status, created_at in orders:
            text += (
                f"🧾 <b>Buyurtma #{order_id}</b>\n"
                f"☕ {items}\n"
                f"💰 {total:,} so'm\n"
                f"📌 Holat: <b>{status}</b>\n"
                f"🕐 {created_at}\n\n"
            ).replace(",", " ")
        await callback.message.edit_text(text, reply_markup=main_menu())

    await callback.answer()
