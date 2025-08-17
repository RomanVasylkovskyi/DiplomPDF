from database.utiles import *
from enum import Enum as PyEnum
from sqlalchemy import select
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Gender(PyEnum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

class Worker(Base):
    __tablename__ = 'worker'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    patronymic = Column(String(50))
    age = Column(Integer)
    gender = Column(Enum(Gender), default=Gender.OTHER)
    position = Column(String(100), nullable=False)
    salary = Column(Numeric(10, 2))

    files = relationship("DBFile", back_populates="creator", cascade="all, delete-orphan")

    def __init__(self, name, surname, patronymic, age, gender, position, salary):
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.age = age
        self.gender = gender
        self.position = position
        self.salary = salary

    def __str__(self):
        return f"{self.surname} {self.name} — {self.position}"

def get_all_workers():
    session = get_session()
    try:
        return session.execute(select(Worker)).scalars().all()
    except SQLAlchemyError as e:
        print(f"❌ Error fetching workers: {e}")
        return []
    finally:
        session.close()

def get_worker(id):
    session = get_session()
    try:
        return session.query(Worker).filter_by(id=id).first()
    except SQLAlchemyError as e:
        print(e)
        return None
    finally:
        session.close()


def update_worker(updated_worker):
    session = get_session()
    try:
        worker = get_worker(updated_worker.id)
        if worker:
            worker.name = updated_worker.name
            worker.surname = updated_worker.surname
            worker.patronymic = updated_worker.patronymic
            worker.age = updated_worker.age
            worker.gender = updated_worker.gender
            worker.position = updated_worker.position
            worker.salary = updated_worker.salary

            session.add(worker)
            session.commit()
            return True
        else:
            return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error updating worker: {e}")
        return False
    finally:
        session.close()

def generate_fake_worker():
    from faker import Faker
    import random

    fake = Faker('uk_UA')

    roles = [
        "Доцент", "Професор", "Асистент", "Старший викладач",
        "Інженер-програміст", "Завідувач кафедри", "Методист",
        "Лаборант", "Куратор", "Секретар кафедри"
    ]

    gender_str = random.choice(['male', 'female'])
    name = fake.first_name_male() if gender_str == 'male' else fake.first_name_female()
    surname = fake.last_name_male() if gender_str == 'male' else fake.last_name_female()
    patronymic = name + ('ович' if gender_str == 'male' else 'івна')
    age = random.randint(25, 65)
    position = random.choice(roles)
    salary = round(random.uniform(10000, 40000), 2)

    gender_enum = Gender.MALE if gender_str == 'male' else Gender.FEMALE

    return Worker(
        name=name,
        surname=surname,
        patronymic=patronymic,
        age=age,
        gender=gender_enum,
        position=position,
        salary=salary
    )
