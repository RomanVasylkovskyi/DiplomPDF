import customtkinter as ctk
from datetime import datetime
import requests
from backend import get_all_files_request

def create_admin_menu_tab(tab_frame):
    search_frame = ctk.CTkFrame(tab_frame)
    search_frame.pack(pady=10, padx=10, fill="x")

    search_var = ctk.StringVar()

    def on_search_var_change(*args):
        query = search_var.get().lower()
        all_files = get_all_files_request()
        if query:
            filtered_files = [f for f in all_files if query in f.name.lower()]
            update_file_list(filtered_files)
        else:
            update_file_list(all_files)

    search_var.trace_add("write", on_search_var_change)

    search_entry = ctk.CTkEntry(search_frame, textvariable=search_var, placeholder_text="Введіть назву файлу")
    search_entry.pack(side="left", padx=(10, 5), expand=True, fill="x")

    results_frame = ctk.CTkScrollableFrame(tab_frame, width=850, height=550)
    results_frame.pack(padx=10, pady=(5, 10), fill="both", expand=True)

    file_rows = []

    def update_file_list(file_list):
        for widget in file_rows:
            widget.destroy()
        file_rows.clear()

        for file in file_list:
            row = ctk.CTkFrame(results_frame, border_width=1, corner_radius=8, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=5)

            name_label = ctk.CTkLabel(row, text=file.name, anchor="w")
            name_label.pack(side="left", padx=5, pady=10, expand=True)

            date_label = ctk.CTkLabel(row, text=file.datetime.strftime("%Y-%m-%d %H:%M"), anchor="w")
            date_label.pack(side="left", padx=5, pady=10, expand=True)

            delete_button = ctk.CTkButton(row, text="Видалити", width=100, command=lambda f=file.name: ask_password_and_delete(f))
            delete_button.pack(side="right", padx=5)

            download_button = ctk.CTkButton(row, text="Скачати", width=100, command=lambda f=file.name: download_file(f))
            download_button.pack(side="right", padx=5)



            file_rows.append(row)

    def download_file(filename):
        print(f"Завантаження: {filename}")

    def delete_file(filename):
        print(f"Видалення: {filename}")
        # Тут можеш викликати видалення з БД, якщо потрібно

    def ask_password_and_delete(filename):
        password_window = ctk.CTkToplevel(tab_frame)
        password_window.title("Підтвердження паролем")
        password_window.geometry("300x200")
        password_window.grab_set()

        label = ctk.CTkLabel(password_window, text="Введіть пароль для підтвердження:")
        label.pack(pady=10)

        password_var = ctk.StringVar()
        password_entry = ctk.CTkEntry(password_window, textvariable=password_var, show="*")
        password_entry.pack(pady=5, padx=20)

        error_label = ctk.CTkLabel(password_window, text="", text_color="red")
        error_label.pack()

        def confirm():
            password = password_var.get()
            if password == "1111":
                delete_file(filename)
                password_window.destroy()
                update_file_list(get_all_files_request())
            else:
                error_label.configure(text="❌ Невірний пароль")

        confirm_button = ctk.CTkButton(password_window, text="Підтвердити", command=confirm)
        confirm_button.pack(pady=0)

    update_file_list(get_all_files_request())
