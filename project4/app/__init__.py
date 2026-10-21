from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Text

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@postgres:5432/app_db"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# Модель Product, которую ждет твой main.py
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    price = Column(Numeric(10, 2))
    stock = Column(Integer)
    category = Column(String, index=True)
    description = Column(Text, nullable=True)

async def get_db():
    async with async_session_maker() as session:
        yield session