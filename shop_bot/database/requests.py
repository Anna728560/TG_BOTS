from shop_bot.database.db_config import async_session
from shop_bot.database.models import User, Category, Item
from sqlalchemy import select


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
