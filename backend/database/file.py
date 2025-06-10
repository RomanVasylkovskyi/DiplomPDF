from database.utiles import *
from sqlalchemy import DateTime, select
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

import os

class DBFile(Base):
    __tablename__ = 'dbfile'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    path = Column(String(100), nullable=False)
    datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    description = Column(String(100), nullable=True)

    def __init__(self, name, path, datetime, description):
        self.name = name
        self.path = path
        self.datetime = datetime
        self.description = description

    def __str__(self):
        return f"{self.name} {self.name},  {self.datetime},  {self.description[:20]}"


def get_all_files():
    session = get_session()
    try:
        result = session.execute(select(DBFile)).scalars().all()
        session.close()
        return result
    except SQLAlchemyError as e:
        print(f"❌ Error fetching all files: {e}")
        return []

def get_file(id):
    session = get_session()
    try:
        return session.query(DBFile).filter_by(id=id).first()
    except SQLAlchemyError as e:
        print(e)
        return None
    finally:
        session.close()

def delete_file(file_id):
    session = get_session()
    try:
        file_obj = session.query(DBFile).filter_by(id=file_id).first()
        if not file_obj:
            raise HTTPException(status_code=404, detail="Файл не знайдено в базі даних")

        # Спроба видалити файл із файлової системи
        if os.path.exists(file_obj.path):
            try:
                os.remove(file_obj.path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Не вдалося видалити файл з диска: {e}")
        else:
            print(f"⚠️ Файл {file_obj.path} не існує на диску — буде видалено лише з бази")

        # Видалення з бази даних
        session.delete(file_obj)
        session.commit()

        return True
    except SQLAlchemyError as db_err:
        session.rollback()
        print(f"❌ DB error while deleting file ID {file_id}: {db_err}")
        raise HTTPException(status_code=500, detail="Помилка бази даних під час видалення файлу")
        return False
    finally:
        session.close()

def start_generate_fake_files():
    for i in range(10):
        new_file = DBFile(
            name=f"Report2025 #{i}",
            path="files/report_2025.pdf",
            datetime=datetime.now(),
            description="Фінансовий звіт за 2025 рік"
        )
        db_insert(new_file)