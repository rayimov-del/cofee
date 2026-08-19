from aiogram import Router, types
from aiogram.filters import CommandStart
from database.crud import add_user
from buttons.inline import main_menu

router=Router()

@router.message(CommandStart())
async def start(message: types.Message):
    u=message.from_user
    add_user(u.id,u.full_name,u.username or "No username")
    await message.answer(
        f"☕ <b>COFFEE BOT</b> ga xush kelibsiz, {u.first_name}!\n\n"
        "✨ Bu yerda sevimli qahvangizni toping, savatchaga qo'shing va bir necha bosishda buyurtma bering.",
        reply_markup=main_menu()
    )

@router.callback_query(lambda c: c.data=="home")
async def home(callback: types.CallbackQuery):
    await callback.message.edit_text("☕ <b>COFFEE BOT</b>\n\nNima qilamiz?",reply_markup=main_menu())
    await callback.answer()
