from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import shop_bot.database.requests as rq
import shop_bot.bot_config.keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(
        "✨ Hello! I'm your Magic Brews bot 🧙‍♂️.\n"
        "I have a cauldron full of magical potions!\n"
        "Choose the category of potion you need 🐍: \n",
        reply_markup=await kb.inline_categories()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Some help text")


@router.callback_query(F.data.startswith("category_"))
async def category_items(callback: CallbackQuery):
    await callback.answer("You made your choice, and that's perfectly fine!")
    await callback.message.answer(
        text="Chose the potion you need 🧪",
        reply_markup=await kb.inline_items(int(callback.data.split("_")[1]))
    )


@router.callback_query(F.data.startswith("item_"))
async def item(callback: CallbackQuery):
    item_data = await rq.get_item(int(callback.data.split("_")[1]))
    await callback.answer("You made your choice, and that's perfectly fine!")
    await callback.message.answer(
        text=f"__Name__\n"
             f"{item_data.name}\n\n"
             f"__Description__\n"
             f"🪄{item_data.description}\n\n"
             f"Price: $ {item_data.price}",
        # reply_markup=await kb.inline_items(int(callback.data.split("_")[1]))
        reply_markup=await kb.item_details()
    )


@router.callback_query(F.data.startswith("back_"))
async def back_to_categories(callback: CallbackQuery):
    await callback.answer("Return to the Magic Brews Menu... 🍵")
    await callback.message.answer(
        text="Chose the potion you need 🧪",
        reply_markup=await kb.inline_categories()
    )

