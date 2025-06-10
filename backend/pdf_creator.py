from fpdf import FPDF

import os
import hashlib
import uuid


def generate_pdf(filename, participants, questions):
    pdf = FPDF()
    pdf.add_page()

    pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=14)
    
    pdf.cell(200, 10, txt="Discussion Protocol", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("DejaVu", size=14)
    pdf.cell(200, 10, "Participants:", ln=True)

    pdf.set_font("DejaVu", size=14)
    for item in participants:
        name = item.get("name")
        role = item.get("role")
        if name and role:
            pdf.cell(200, 10, f"- {name}, {role}", ln=True)

    pdf.ln(10)
    pdf.set_font("DejaVu", size=14)
    pdf.cell(200, 10, "Questions and Decisions:", ln=True)

    pdf.set_font("DejaVu", size=14)
    for item in questions:
        question = item.get("question")
        decision = item.get("decision")
        if question and decision:
            pdf.multi_cell(0, 10, f"Question: {question}\nDecision: {decision}\n", border=1)

    hash_object = hashlib.sha256(str(uuid.uuid4()).encode())
    hashed_filename = hash_object.hexdigest()

    path = f"files/{hashed_filename}.pdf"

    os.makedirs("files", exist_ok=True)
    pdf.output(path)

    return path
