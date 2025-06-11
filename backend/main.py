from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status, Header
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import database.db as db
from database.file import get_all_files, start_generate_fake_files, DBFile
from database.worker import get_all_workers, db_insert, generate_fake_worker
from database.schemas import DBFileSchema, WorkerSchema, PDFRequest

from database.file import delete_file
from pdf_creator import generate_pdf
import config

app = FastAPI()

def admin_auth(x_admin_password: str = Header(...)):
    if x_admin_password != config.ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin password"
        )

app.mount("/files", StaticFiles(directory="files"), name="files")

@app.get("/get_all_files", response_model=List[DBFileSchema])
def get_all_files_view():
    print("/get_all_files:\n", get_all_files())
    return get_all_files()[::-1]

@app.get("/get_all_workers", response_model=List[WorkerSchema])
def get_workers_view():
    return get_all_workers()

@app.post("/generate_pdf/")
def generate_pdf_view(data: PDFRequest):
    pdf_path = generate_pdf(data.filename, [p.model_dump() for p in data.participants], [q.model_dump() for q in data.questions])
    print(f"✅ PDF saved as '{pdf_path}'")
    new_file = DBFile(
        name=data.filename,
        path=pdf_path,
        datetime=data.datetime,
        description=", ".join([q.question for q in data.questions])
    )
    db_insert(new_file)
    return FileResponse(pdf_path, filename=f"{data.filename}.pdf", media_type="application/pdf")

@app.get("/db_seed")
def db_seed_view():
    for i in range(20):
        db_insert(generate_fake_worker())
    start_generate_fake_files()
    return JSONResponse({"message": "ok"})

@app.delete("/admin/delete_file/{file_id}")
def delete_file_view(file_id: int, authorized: None = Depends(admin_auth)):
    result = delete_file(file_id)
    if result:
        return {"message": f"✅ Файл з ID {file_id} успішно видалено"}
    else:
        return {"message": f"❌ Сталась помилка! Файл з ID {file_id} не видалено"}