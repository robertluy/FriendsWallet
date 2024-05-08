import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SqlAlchemyBase = declarative_base()


class Database:
    def __init__(self):
        self.async_engine = None
        self.async_session_factory = None

    async def init_db(self):
        try:
            self.async_engine = create_async_engine(
                url=settings.DATABASE_URL_asyncpg,
                echo=False
            )
            self.async_session_factory = async_sessionmaker(
                bind=self.async_engine,
                class_=AsyncSession
            )
        except Exception as e:
            logger.error(f"Ошибка при инициализации базы данных: {e}")
            raise


db_instance = Database()
