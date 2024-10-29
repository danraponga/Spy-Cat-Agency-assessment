from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.main.config import DbConfig

engine: AsyncEngine = create_async_engine(DbConfig.from_env().build_db_url())
SessionLocal: AsyncSession = async_sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False
)
