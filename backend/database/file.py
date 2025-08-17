from database.utiles import *
from sqlalchemy import DateTime, ForeignKey, select
from sqlalchemy.orm import relationship
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

import os
from random import choice

# 🔗 Модель DBFile з прив'язкою до Worker
class DBFile(Base):
    __tablename__ = 'dbfile'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    path = Column(String(100), nullable=False)
    datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    description = Column(String(100), nullable=True)

    # Зовнішній ключ на Worker
    creator_id = Column(Integer, ForeignKey('worker.id'), nullable=False)
    
    # Зв’язок до Worker
    creator = relationship("Worker", back_populates="files")

    def __init__(self, name, path, datetime, description, creator_id):
        self.name = name
        self.path = path
        self.datetime = datetime
        self.description = description
        self.creator_id = creator_id

    def __str__(self):
        return f"{self.name}, {self.datetime}, {self.description[:20]}"


# 🔍 Отримати всі файли
def get_all_files():
    session = get_session()
    try:
        result = session.execute(select(DBFile)).scalars().all()
        return result
    except SQLAlchemyError as e:
        print(f"❌ Error fetching all files: {e}")
        return []
    finally:
        session.close()


# 🔍 Отримати файл по ID
def get_file(id):
    session = get_session()
    try:
        return session.query(DBFile).filter_by(id=id).first()
    except SQLAlchemyError as e:
        print(e)
        return None
    finally:
        session.close()


# ❌ Видалити файл (з диску і БД)
def delete_file(file_id):
    session = get_session()
    try:
        file_obj = session.query(DBFile).filter_by(id=file_id).first()
        if not file_obj:
            raise HTTPException(status_code=404, detail="Файл не знайдено в базі даних")

        # Видалення з файлової системи
        if os.path.exists(file_obj.path):
            try:
                os.remove(file_obj.path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Не вдалося видалити файл з диска: {e}")
        else:
            print(f"⚠️ Файл {file_obj.path} не існує на диску — буде видалено лише з бази")
        session.delete(file_obj)
        session.commit()
        return True
    except SQLAlchemyError as db_err:
        session.rollback()
        print(f"❌ DB error while deleting file ID {file_id}: {db_err}")
        raise HTTPException(status_code=500, detail="Помилка бази даних під час видалення файлу")
    finally:
        session.close()


# 🧪 Генерація фейкових файлів для випадкових працівників
def start_generate_fake_files():
    session = get_session()
    try:
        workers = session.query(Worker).all()
        if not workers:
            print("⚠️ Немає працівників у базі для створення файлів.")
            return

        for i in range(10):
            random_worker = choice(workers)
            new_file = DBFile(
                name=f"Report2025 #{i}",
                path=f"files/report_2025_{i}.pdf",
                datetime=datetime.now(),
                description="Фінансовий звіт за 2025 рік",
                creator_id=random_worker.id
            )
            session.add(new_file)

        session.commit()
        print("✅ Успішно згенеровано фейкові файли.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ DB error while generating fake files: {e}")
    finally:
        session.close()
