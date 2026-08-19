import asyncio
import logging

from bot import bot, dp
from database.crud import init_db
from handlers import start, menu, cart, ai, about, admin, orders

logging.basicConfig(level=logging.INFO)

async def main():
    init_db()
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(cart.router)
    dp.include_router(ai.router)
    dp.include_router(about.router)
    dp.include_router(orders.router)
    dp.include_router(admin.router)
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
