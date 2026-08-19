from aiogram import Router, types
from buttons.inline import cart_buttons, main_menu
from database.crud import get_product, add_order
from states.order_state import OrderState
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID

router=Router()
carts={}

def cart_text(user_id):
    cart=carts.get(user_id,[])
    if not cart:
        return "🛒 <b>Savatcha bo'sh</b>\n\nMenyudan mazali coffee tanlang."
    total=0
    lines=["🛒 <b>SIZNING SAVATCHANGIZ</b>\n"]
    for pid,qty in cart:
        p=get_product(pid)
        if p:
            subtotal=p[3]*qty; total+=subtotal
            lines.append(f"{p[5]} {p[1]} × {qty} = <b>{subtotal:,} so'm</b>".replace(","," "))
    lines.append(f"\n💰 Jami: <b>{total:,} so'm</b>".replace(","," "))
    return "\n".join(lines)

@router.callback_query(lambda c: c.data.startswith("add:"))
async def add(callback: types.CallbackQuery):
    pid=int(callback.data.split(":")[1])
    cart=carts.setdefault(callback.from_user.id,[])
    for i,(x,q) in enumerate(cart):
        if x==pid: cart[i]=(x,q+1); break
    else: cart.append((pid,1))
    await callback.answer("✅ Savatchaga qo'shildi!")
    await callback.message.edit_text(cart_text(callback.from_user.id),reply_markup=cart_buttons())

@router.callback_query(lambda c: c.data=="cart")
async def cart(callback: types.CallbackQuery):
    await callback.message.edit_text(cart_text(callback.from_user.id),reply_markup=cart_buttons())
    await callback.answer()

@router.callback_query(lambda c: c.data=="clear_cart")
async def clear_cart(callback: types.CallbackQuery):
    carts.pop(callback.from_user.id,None)
    await callback.message.edit_text("🗑 Savatcha tozalandi.",reply_markup=main_menu())
    await callback.answer()

@router.callback_query(lambda c: c.data=="checkout")
async def checkout(callback: types.CallbackQuery,state:FSMContext):
    if not carts.get(callback.from_user.id):
        await callback.answer("Savatcha bo'sh!",show_alert=True); return
    await callback.message.answer("📱 Buyurtma uchun telefon raqamingizni yuboring:\nMasalan: +998901234567")
    await state.set_state(OrderState.phone)
    await callback.answer()

@router.message(OrderState.phone)
async def phone(message: types.Message,state:FSMContext):
    phone=message.text.strip()
    if len(phone)<7:
        await message.answer("❌ Telefon raqam noto'g'ri. Qaytadan yuboring.")
        return
    await state.update_data(phone=phone)
    await message.answer("📍 Yetkazib berish manzilini yozing:")
    await state.set_state(OrderState.address)

@router.message(OrderState.address)
async def address(message: types.Message,state:FSMContext):
    uid=message.from_user.id
    data=await state.get_data()
    cart=carts.get(uid,[])
    items=[]; total=0
    for pid,qty in cart:
        p=get_product(pid)
        if p:
            items.append(f"{p[1]} x{qty}")
            total+=p[3]*qty
    order_id=add_order(uid,message.from_user.full_name,data["phone"],message.text.strip(),", ".join(items),total)
    await state.clear(); carts.pop(uid,None)
    await message.answer(
        f"🎉 <b>Buyurtma #{order_id} qabul qilindi!</b>\n\n"
        f"💰 Jami: <b>{total:,} so'm</b>\n"
        "🚚 Tez orada siz bilan bog'lanamiz. Rahmat! ☕".replace(","," ")
    )
    if ADMIN_ID:
        await message.bot.send_message(
            ADMIN_ID,
            f"🔔 <b>YANGI BUYURTMA #{order_id}</b>\n"
            f"👤 {message.from_user.full_name}\n"
            f"📱 {data['phone']}\n📍 {message.text.strip()}\n"
            f"☕ {', '.join(items)}\n💰 <b>{total:,} so'm</b>".replace(","," ")
        )
