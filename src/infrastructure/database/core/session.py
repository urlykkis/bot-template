from sqlalchemy import create_engine

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


def make_connection_string(db_url: str, async_fallback: bool = False) -> str:
    """Создает ссылку для базы данной"""
    result = db_url

    if async_fallback:
        result += "?async_fallback=True"
    return result


def get_async_engine(db_url: str, echo: bool = False):
    """Создает двигатель для БД"""
    engine = create_async_engine(make_connection_string(db_url), echo=echo)
    return engine


def get_sync_engine(db_url: str, echo: bool = False):
    engine = create_engine(db_url, echo=echo)
    return engine


def sa_sessionmaker(db_url, echo: bool = False) -> sessionmaker:
    """
    Создает sessionmaker
    :return: sessionmaker
    :rtype: sqlalchemy.orm.sessionmaker
    """
    engine = get_async_engine(db_url=db_url, echo=echo)
    return sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
        future=True,
        autoflush=False,
    )
