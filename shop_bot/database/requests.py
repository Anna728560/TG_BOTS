from typing import List
from sqlalchemy import select

from shop_bot.database.db_config import async_session
from shop_bot.database.models import User, Category, Item


async def set_user(tg_id: int) -> None:
    """
    Adds a new user to the database
    if the user with the specified Telegram ID doesn't exist.

    Parameters:
        tg_id (int): Telegram ID of the user.

    Returns:
        None
    """
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_categories() -> List[Category]:
    """
    Retrieves the list of categories from the database.

    Returns:
        list[Category]: List of category names.
    """
    async with async_session() as session:
        return await session.scalars(select(Category))


async def get_category_items(category_id: int) -> List[Item]:
    """
    Retrieves items belonging to the specified category.

    Parameters:
        category_id (int): ID of the category.

    Returns:
        List[Item]: List of items belonging to the specified category.
    """
    async with async_session() as session:
        return await session.scalars(
            select(Item).where(Item.category == category_id)
        )


async def get_item(item_id: int) -> Item:
    """
    Retrieves the item with the specified ID.

    Parameters:
        item_id (int): ID of the item.

    Returns:
        Item: Item with the specified ID.
    """
    async with async_session() as session:
        return await session.scalar(
            select(Item).where(Item.id == item_id)
        )
