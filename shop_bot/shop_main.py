import asyncio
import logging
import sys

from aiogram import Dispatcher

from shop_bot.database.db_config import async_main
from shop_bot.bot_config.handlers import router
from shop_bot.bot_config.bot import bot


async def main():
    await async_main()
    dp = Dispatcher()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down")
