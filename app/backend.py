from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import requests

from decimal import Decimal
from enum import Enum
import config

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
    response = requests.get(f"{config.BACKEND_URL}/get_all_files")

    if response.status_code == 200:
        raw_data = response.json()
        parsed_files = [DBFileSchema(**item) for item in raw_data]
        if parsed_files:
            print(parsed_files[0].name)
        return parsed_files
    
    return []

def get_all_worker_request():
    response = requests.get(f"{config.BACKEND_URL}/get_all_workers")

    if response.status_code == 200:
        raw_data = response.json()
        parsed_workers = [WorkerSchema(**item) for item in raw_data]
        if parsed_workers:
            print(parsed_workers[0].name)
        return parsed_workers
    
    return []

def send_pdf_request(request_data: PDFRequest):
    response = requests.post(
        f"{config.BACKEND_URL}/generate_pdf/",
        json=request_data.model_dump(mode="json")
    )

def download_pdf(filename, path):
    url = f"{config.BACKEND_URL}/{path}"
    response = requests.get(
        url,
    )
    
    from tkinter import filedialog
    save_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialfile=f"{filename}.pdf",
        title="Save PDF as..."
    )
    print("save_path", save_path, response.status_code)
    print("url", url)

    if not save_path:
        print("❌ Save cancelled.")
        return False, ""

    response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"✅ PDF saved as '{save_path}'")
        return True, save_path
    else:
        print("❌ Error:", response.status_code, response.text)
        return False, ""

def delete_pdf(file_id, admin_password):
    url = f"{config.BACKEND_URL}/admin/delete_file/{file_id}"
    
    headers = {
        "x-admin-password": admin_password
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        print(f"✅ File with ID {file_id} deleted successfully")
        return True
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return False