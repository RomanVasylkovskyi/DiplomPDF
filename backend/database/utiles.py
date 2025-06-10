import sqlalchemy
from sqlalchemy import Column, Integer, String, Enum, Numeric
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from config import settings

engine = sqlalchemy.create_engine(settings.database_url)
Base = declarative_base()

def create_db():
    Base.metadata.create_all(engine)


def get_session():
    return Session()


def db_insert(data):
    session = get_session()
    try:
        session.add(data)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
    finally:
        session.close()

Session = scoped_session(sessionmaker(bind=engine))