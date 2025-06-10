BACKEND_URL = "http://127.0.0.1:8000"
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import requests

from decimal import Decimal
from enum import Enum

class DBFileSchema(BaseModel):
    id: int
    name: str
    path: str
    datetime: datetime
    description: Optional[str]

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

class Question(BaseModel):
    question: str
    decision: str

class PDFRequest(BaseModel):
    filename: str
    participants: List[Participant]
    questions: List[Question]
    datetime: datetime

def get_all_files_request():
    response = requests.get(f"{BACKEND_URL}/get_all_files")

    if response.status_code == 200:
        raw_data = response.json()
        parsed_files = [DBFileSchema(**item) for item in raw_data]
        if parsed_files:
            print(parsed_files[0].name)
        return parsed_files
    
    return []

def get_all_worker_request():
    response = requests.get(f"{BACKEND_URL}/get_all_workers")

    if response.status_code == 200:
        raw_data = response.json()
        parsed_workers = [WorkerSchema(**item) for item in raw_data]
        if parsed_workers:
            print(parsed_workers[0].name)
        return parsed_workers
    
    return []

def send_pdf_request(request_data: PDFRequest):
    response = requests.post(
        f"{BACKEND_URL}/generate_pdf/",
        json=request_data.model_dump(mode="json")  # ✅
    )


    if response.status_code == 200:
        pdf_filename = f"{request_data.filename}.pdf"
        with open(pdf_filename, "wb") as f:
            f.write(response.content)
        print(f"✅ PDF saved as {pdf_filename}")
    else:
        print("❌ Error:", response.status_code, response.text)
