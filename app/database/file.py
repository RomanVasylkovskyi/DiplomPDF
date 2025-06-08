from database.utiles import *
from sqlalchemy import DateTime
from datetime import datetime

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
        return session.query(DBFile).all()
    except SQLAlchemyError as e:
        print(f"❌ Error fetching all files: {e}")
        return []
    finally:
        session.close()


def get_file(id):
    session = get_session()
    try:
        return session.query(DBFile).filter_by(id=id).first()
    except SQLAlchemyError as e:
        print(e)
        return None
    finally:
        session.close()


def update_file(updated_file):
    session = get_session()
    try:
        file = get_file(updated_file.id)
        if file:
            file.name = updated_file.name
            file.path = updated_file.path
            file.datetime = updated_file.datetime
            file.description = updated_file.description

            session.add(file)
            session.commit()
            return True
        else:
            return False
    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error updating file: {e}")
        return False
    finally:
        session.close()


def start_generate():
    for i in range(10):
        new_file = DBFile(
            name=f"Report2025 #{i}",
            path="/files/report_2025.pdf",
            datetime=datetime.now(),
            description="Фінансовий звіт за 2025 рік"
        )
        db_insert(new_file)

# start_generate()