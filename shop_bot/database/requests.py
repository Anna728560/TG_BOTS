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


async def get_categories() -> List[str]:
    """
    Retrieves the list of categories from the database.

    Returns:
        list[str]: List of category names.
    """
    async with async_session() as session:
        query = await session.execute(select(Category.name))
        categories = query.scalars().all()
        return categories
