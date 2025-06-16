import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database.models import Model


async_engine = create_async_engine(
    "sqlite+aiosqlite:///telegrambot.db"
)

new_session = async_sessionmaker(async_engine, expire_on_commit=False, autoflush=False)

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())