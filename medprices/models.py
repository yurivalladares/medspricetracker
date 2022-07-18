"""crawl/crawl/models.py"""
from sqlalchemy import Column, Integer, String, create_engine, Identity, Float, Time
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

from medprices import settings

DeclarativeBase = declarative_base()


def db_connect() -> Engine:
    """
    Creates database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_items_table(engine: Engine):
    """
    Create the Items table
    """
    DeclarativeBase.metadata.create_all(engine)


class Items(DeclarativeBase):
    """
    Defines the items model
    """

    __tablename__ = "medprices_db"

    id = Column('id', Integer, Identity(start=42, cycle=True), primary_key=True)
    product_name = Column("product_name", String)
    manufacturer = Column("manufacturer", String)
    price = Column("price", Float)
    product_url = Column("product_url", String)
    scraped_at = Column("scraped_at", Time)
    store = Column("store", String)