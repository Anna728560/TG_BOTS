import asyncio

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import shop_bot.database.requests as rq
import shop_bot.keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(
        "✨ Hello! I'm your Magic Brews bot 🧙‍♂️.\n"
        "I have a cauldron full of magical potions!\n"
        "Choose the category of potion you need:\n",
        reply_markup=await kb.inline_keyboard()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Some help text")
