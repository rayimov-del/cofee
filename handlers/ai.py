from aiogram import Router, types
from buttons.inline import main_menu

router=Router()

@router.callback_query(lambda c: c.data=="coffee_ai")
async def coffee_ai(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🤖 <b>COFFEE AI BARISTA</b>\n\n"
        "Kayfiyatingizga qarab tavsiya:\n\n"
        "⚡ <b>Energiya kerakmi?</b> → Espresso yoki Americano\n"
        "🥛 <b>Yumshoq ta'mmi?</b> → Latte yoki Cappuccino\n"
        "🍫 <b>Shirinlik xohlaysizmi?</b> → Mocha + Cheesecake\n"
        "🧊 <b>Sovuq ichimlikmi?</b> → Iced Latte\n"
        "✨ <b>Premium tanlovmi?</b> → Caramel Macchiato\n\n"
        "☕ bot barista bugungi tanlovingizga tayyor!",
        reply_markup=main_menu()
    )
    await callback.answer()
