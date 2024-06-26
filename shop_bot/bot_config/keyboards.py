from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from shop_bot.database.requests import get_categories, get_category_items


async def inline_categories():
    categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in categories:
        keyboard.add(InlineKeyboardButton(
            text=category.name,
            callback_data=f"category_{category.id}")
        )
    return keyboard.adjust(1).as_markup()


async def inline_items(category_id: int):
    items = await get_category_items(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in items:
        keyboard.add(InlineKeyboardButton(
            text=item.name,
            callback_data=f"item_{item.id}")
        )
    keyboard.add(InlineKeyboardButton(
        text="Back",
        callback_data="back_to_categories")
    )
    return keyboard.adjust(2).as_markup()


async def item_details(item_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text="I'm buying!📦",
        callback_data=f"to_pay_item_{item_id}")
    )
    keyboard.add(InlineKeyboardButton(
        text="Back",
        callback_data="back_to_categories")
    )
    return keyboard.adjust(2).as_markup()
