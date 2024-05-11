import json

import aiofiles
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(100))
    price: Mapped[str] = mapped_column()
    category: Mapped[int] = mapped_column(ForeignKey("categories.id"))


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
        await fill_database()
