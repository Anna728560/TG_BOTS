import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from shop_bot.database.models import async_main


async def main():
    await async_main()
    bot = Bot(token="6919714198:AAHRbrPvSZeluxyEc6DDRfeMdkljZ2nkgeY")
    dp = Dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down")
