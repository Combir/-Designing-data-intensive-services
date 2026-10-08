import asyncio
from app.database import engine
from app.models import Base


async def create_tables():
    async with engine.begin() as conn:
        # Синхронно выполняем создание таблиц на основе метаданных моделей
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Таблицы успешно созданы в базе данных!")


if __name__ == "__main__":
    asyncio.run(create_tables())