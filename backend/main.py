from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import database.db as db
from database.file import get_all_files, start_generate_fake_files, DBFile
from database.worker import get_all_workers, db_insert, generate_fake_worker
from database.schemas import DBFileSchema, WorkerSchema, PDFRequest

from pdf_creator import generate_pdf

app = FastAPI()

# Serve files from "files/" directory at "/files" URL path
app.mount("/files", StaticFiles(directory="files"), name="files")
@app.get("/get_all_files", response_model=List[DBFileSchema])
def get_all_files_view():
    print("/get_all_files:\n", get_all_files())
    return get_all_files()

@app.get("/get_all_workers", response_model=List[WorkerSchema])
def get_workers():
    return get_all_workers()

@app.post("/generate_pdf/")
def generate_pdf_endpoint(data: PDFRequest):
    pdf_path = generate_pdf(data.filename, [p.model_dump() for p in data.participants], [q.model_dump() for q in data.questions])
    new_file = DBFile(
        name=data.filename,
        path=pdf_path,
        datetime=data.datetime,
        description=", ".join([q.question for q in data.questions])
    )
    db_insert(new_file)
    return FileResponse(pdf_path, filename=f"{data.filename}.pdf", media_type="application/pdf")

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"files/{filename}"
    return FileResponse(path=file_path, filename=filename, media_type='application/octet-stream')

@app.get("/db_seed")
def db_seed():
    for i in range(20):
        db_insert(generate_fake_worker())
    start_generate_fake_files()


# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     content = await file.read()  # Reads entire content
#     return JSONResponse(content={"filename": file.filename, "content_type": file.content_type})
# @app.post("/upload-multiple/")
# async def upload_multiple(files: List[UploadFile] = File(...)):
#     return [{"filename": file.filename, "content_type": file.content_type} for file in files]