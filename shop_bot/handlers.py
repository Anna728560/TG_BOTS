import asyncio

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import shop_bot.database.requests as rq


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(
        "✨ Hello! I'm your Magic Brews bot 🧙‍♂️.\n"
        "I have a cauldron full of magical potions!\n"
        "Choose the category of potion you need:\n"
    )
