from database.utiles import *
from enum import Enum as PyEnum

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

    def __init__(self, name, surname, patronymic, age, gender, position, salary):
        super().__init__(name=name, surname=surname, patronymic=patronymic,
                         age=age, gender=gender)
        self.position = position
        self.salary = salary

    def __str__(self):
        return f"{self.name} {self.surname}, position: {self.position}, salary: {self.salary}"


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


