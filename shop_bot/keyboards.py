from aiogram.types import (
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from shop_bot.database.models import Category
from shop_bot.database.db_config import async_session
from sqlalchemy import select


async def get_categories():
    async with async_session() as session:
        query = await session.execute(select(Category.name))
        categories = query.scalars().all()
        return categories


async def inline_categories():
    categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in categories:
        keyboard.add(InlineKeyboardButton(text=category, url="https://www.google.com"))
    return keyboard.adjust(2).as_markup()
