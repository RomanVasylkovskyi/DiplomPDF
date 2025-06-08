import customtkinter as ctk
import database.db as db
from fpdf import FPDF

from tabs.participants_tab import create_participants_tab
from tabs.topics_tab import create_topics_tab
from tabs.generate_pdf_tab import create_pdf_tab
from tabs.files_tab import create_files_tab
from tabs.admin_menu_tab import create_admin_menu_tab

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("900x700")
app.title("Discussion Protocol")

tabview = ctk.CTkTabview(app, width=880, height=660)
tabview.pack(padx=10, pady=1)


tabview.add("Participants")
tabview.add("Topics")
tabview.add("Generate PDF")
tabview.add("Files")
tabview.add("Admin Menu")

create_participants_tab(tabview.tab("Participants"))
create_topics_tab(tabview.tab("Topics"))
create_pdf_tab(tabview.tab("Generate PDF"))
create_files_tab(tabview.tab("Files"))
create_admin_menu_tab(tabview.tab("Admin Menu"))

app.mainloop()
# # --- Participants ---
# participants = []
#
# participants_frame_label = ctk.CTkLabel(app, text="Participants:", font=ctk.CTkFont(size=16, weight="bold"))
# participants_frame_label.pack(anchor="w", padx=10)
#
# participants_scroll = ctk.CTkScrollableFrame(app, height=180)
# participants_scroll.pack(padx=10, pady=(0, 10), fill="x")
#
# def add_participant():
#     frame = ctk.CTkFrame(participants_scroll)
#     frame.pack(pady=5, fill="x", padx=5)
#
#     name_entry = ctk.CTkEntry(frame, placeholder_text="Full Name")
#     name_entry.pack(side="left", padx=(0, 5), expand=True, fill="x")
#
#     role_entry = ctk.CTkEntry(frame, placeholder_text="Position")
#     role_entry.pack(side="left", padx=(0, 5), expand=True, fill="x")
#
#     def remove_this():
#         participants.remove((name_entry, role_entry))
#         frame.destroy()
#
#     remove_btn = ctk.CTkButton(frame, text="✖", width=30, command=remove_this)
#     remove_btn.pack(side="left")
#
#     participants.append((name_entry, role_entry))
#
# ctk.CTkButton(app, text="+ Add Participant", command=add_participant).pack()
#
# # --- Questions and Decisions ---
# questions = []
#
# ctk.CTkLabel(app, text="Discussion Topics:", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10)
#
# questions_scroll = ctk.CTkScrollableFrame(app, height=250)
# questions_scroll.pack(padx=10, pady=(0, 10), fill="both", expand=True)
#
# def add_question():
#     frame = ctk.CTkFrame(questions_scroll, border_width=1, corner_radius=8)
#     frame.pack(pady=10, padx=5, fill="x")
#
#     question_entry = ctk.CTkEntry(frame, placeholder_text="Question")
#     question_entry.pack(fill="x", padx=10, pady=(5, 5))
#
#     decision_entry = ctk.CTkEntry(frame, placeholder_text="Decision")
#     decision_entry.pack(fill="x", padx=10, pady=(0, 5))
#
#     def remove_this():
#         questions.remove((question_entry, decision_entry))
#         frame.destroy()
#
#     remove_btn = ctk.CTkButton(frame, text="Remove Question", fg_color="red", hover_color="#800000", command=remove_this)
#     remove_btn.pack(pady=5)
#
#     questions.append((question_entry, decision_entry))
#
# ctk.CTkButton(app, text="+ Add Question", command=add_question).pack()
#
# # --- PDF Generation ---
# def generate_pdf():
#     pdf = FPDF()
#     pdf.add_page()
#
#     pdf.set_font("Times", size=14)
#     pdf.cell(200, 10, txt="Discussion Protocol", ln=True, align="C")
#
#     pdf.ln(10)
#     pdf.set_font("Times", style='B', size=14)
#     pdf.cell(200, 10, "Participants:", ln=True)
#
#     pdf.set_font("Times", size=14)
#     for name_entry, role_entry in participants:
#         try:
#             name = name_entry.get()
#             role = role_entry.get()
#             if name and role:
#                 pdf.cell(200, 10, f"- {name}, {role}", ln=True)
#         except:
#             continue
#
#     pdf.ln(10)
#     pdf.set_font("Times", style='B', size=14)
#     pdf.cell(200, 10, "Questions and Decisions:", ln=True)
#
#     pdf.set_font("Times", size=14)
#     for q_entry, d_entry in questions:
#         try:
#             q = q_entry.get()
#             d = d_entry.get()
#             if q and d:
#                 pdf.multi_cell(0, 10, f"Question: {q}\nDecision: {d}\n", border=1)
#         except:
#             continue
#
#     pdf.output("discussion_protocol.pdf")
#     print("✅ PDF saved as 'discussion_protocol.pdf'")
#
# ctk.CTkButton(app, text="Generate PDF", command=generate_pdf).pack(pady=15)


