from aiogram import Router, types
from buttons.inline import main_menu

router=Router()

@router.callback_query(lambda c: c.data=="about")
async def about(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "☕ <b>COFFEE BOT</b>\n\n"
        "Mazali coffee, qulay buyurtma va zamonaviy xizmat.\n\n"
        "✨ Har bir buyurtma — yaxshi kayfiyat.\n"
        "🚀 Tezkor menyu\n"
        "🛒 Savatcha\n"
        "📦 Buyurtma nazorati\n"
        "🤖 Bot tavsiyasi",
        reply_markup=main_menu()
    )
    await callback.answer()
