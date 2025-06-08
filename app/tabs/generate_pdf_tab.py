import customtkinter as ctk
from tkcalendar import DateEntry
import datetime
import tkinter as tk  # потрібен для tkcalendar

def create_pdf_tab(tab_frame):
    # Заголовок
    label = ctk.CTkLabel(tab_frame, text="Генерація PDF", font=ctk.CTkFont(size=16))
    label.pack(pady=(20, 10))

    # Ряд із назвою файлу та датою
    row_frame = ctk.CTkFrame(tab_frame)
    row_frame.pack(fill="x", padx=10, pady=5)

    # Поле "Назва файлу"
    filename_entry = ctk.CTkEntry(row_frame, placeholder_text="Назва файлу")
    filename_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

    # Поле "Дата" (tkcalendar DateEntry)
    today = datetime.date.today()
    date_entry = DateEntry(row_frame, width=12, background='darkblue',
                           foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    date_entry.set_date(today)
    date_entry.pack(side="left")

    # Кнопка "Згенерувати PDF"
    generate_button = ctk.CTkButton(tab_frame, text="Згенерувати PDF")
    generate_button.pack(pady=(15, 10))

