import customtkinter as ctk
import database.db as db
from fpdf import FPDF

from tabs.participants_tab import create_participants_tab
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
tabview.add("Generate PDF")
tabview.add("Files")
tabview.add("Admin Menu")

create_participants_tab(tabview.tab("Participants"))
create_pdf_tab(tabview.tab("Generate PDF"))
create_files_tab(tabview.tab("Files"))
create_admin_menu_tab(tabview.tab("Admin Menu"))

app.mainloop()