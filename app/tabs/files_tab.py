import customtkinter as ctk
from datetime import datetime
from database.file import *

def create_files_tab(tab_frame):
    search_frame = ctk.CTkFrame(tab_frame)
    search_frame.pack(pady=10, padx=10, fill="x")

    search_entry = ctk.CTkEntry(search_frame, placeholder_text="Введіть назву файлу")
    search_entry.pack(side="left", padx=(10, 5), expand=True, fill="x")

    def on_search():
        query = search_entry.get()
        update_file_list(["test1.pdf", "test2.docx"] if query else [])

    search_button = ctk.CTkButton(search_frame, text="Пошук", command=on_search)
    search_button.pack(side="left", padx=5)

    # Область з результатами
    results_frame = ctk.CTkScrollableFrame(tab_frame, width=850, height=550)
    results_frame.pack(padx=10, pady=(5, 10), fill="both", expand=True)

    file_rows = []

    # fake_edit_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    def update_file_list(file_list):
        for widget in file_rows:
            widget.destroy()
        file_rows.clear()

        for file in file_list:
            row = ctk.CTkFrame(
                results_frame,
                border_width=1,
                corner_radius=8,
                fg_color="transparent"
            )
            row.pack(fill="x", padx=10, pady=5)

            name_label = ctk.CTkLabel(row, text=file.name, anchor="w")
            name_label.pack(side="left", padx=5, pady=10, expand=True)

            date_label = ctk.CTkLabel(row, text=file.datetime.strftime("%Y-%m-%d %H:%M"), anchor="w")
            date_label.pack(side="left", padx=5, pady=10, expand=True)

            download_button = ctk.CTkButton(row, text="Скачати", width=100, command=lambda f=file.name: download_file(f))
            download_button.pack(side="right", padx=5)

            delete_button = ctk.CTkButton(row, text="Видалити", width=100, command=lambda f=file.name: delete_file(f))
            delete_button.pack(side="right", padx=5)

            file_rows.append(row)



    def download_file(filename):
        print(f"Завантаження: {filename}")

    def delete_file(filename):
        print(f"Видалення: {filename}")


    # Початкове оновлення (якщо потрібно)
    update_file_list(get_all_files())
