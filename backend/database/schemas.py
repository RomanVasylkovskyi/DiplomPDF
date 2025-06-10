from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from enum import Enum

class DBFileSchema(BaseModel):
    id: int
    name: str
    path: str
    datetime: datetime
    description: Optional[str]

    class Config:
        from_attributes = True

class GenderEnum(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

class WorkerSchema(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: Optional[str]
    age: Optional[int]
    gender: GenderEnum
    position: str
    salary: Decimal

    class Config:
        from_attributes = True
        use_enum_values = True  # важливо для коректного JSON-формату



class Participant(BaseModel):
    name: str
    role: str

class QuestionItem(BaseModel):
    question: str
    decision: str

class PDFRequest(BaseModel):
    filename: str
    participants: List[Participant]
    questions: List[QuestionItem]
    datetime: datetime