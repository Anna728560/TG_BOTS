import json
import aiofiles

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from shop_bot.database.models import Base, Category, Item


engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")
async_session = async_sessionmaker(engine)


async def fill_database():
    async with async_session() as session:
        async with aiofiles.open(
                file="categories.json",
                mode="r",
                encoding="utf-8"
        ) as file:
            categories = json.loads(await file.read())

            for category_data in categories:
                category = Category(
                    id=category_data["pk"],
                    name=category_data["name"]
                )

                session.add(category)
            await session.commit()

        async with aiofiles.open(
                file="items.json",
                mode="r",
                encoding="utf-8"
        ) as file:
            items = json.loads(await file.read())

            for item_data in items:
                item = Item(
                    id=item_data["pk"],
                    name=item_data["name"],
                    description=item_data["description"],
                    price=item_data["price"],
                    category=int(item_data["category"])
                )

                session.add(item)
            await session.commit()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # временно комментирую. бд уже настроена
        # await fill_database()
