import customtkinter as ctk
from datetime import datetime
import requests
from backend import get_all_files_request, delete_pdf
from tabs.menu_utils import download_file_wraper

from tabs.message_popup import show_popup

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

            id_label = ctk.CTkLabel(row, text=file.id, anchor="w", width=30)
            id_label.pack(side="left", padx=5, pady=10, expand=True)

            name_label = ctk.CTkLabel(row, text=file.name, anchor="w", width=280)
            name_label.pack(side="left", padx=5, pady=10, expand=True)

            date_label = ctk.CTkLabel(row, text=file.datetime.strftime("%Y-%m-%d %H:%M"), anchor="w", width=130)
            date_label.pack(side="left", padx=5, pady=10, expand=True)

            delete_button = ctk.CTkButton(row, text="Видалити", width=100, command=lambda f_id=file.id: ask_password_and_delete(f_id))
            delete_button.pack(side="right", padx=5)

            download_button = ctk.CTkButton(
                row, text="Скачати", width=100, 
                command=lambda fname=file.name, fpath=file.path: download_button_handler(fname, fpath))
            download_button.pack(side="right", padx=5)

            file_rows.append(row)

    def download_button_handler(fname, fpath):
        download_file_wraper(fname, fpath)
        update_file_list(get_all_files_request())

    def ask_password_and_delete(f_id):
        def toggle_password_visibility():
            current_state = password_entry.cget("show")
            if current_state == "":
                password_entry.configure(show="*")
                toggle_button.configure(text="Show")  # приховано
            else:
                password_entry.configure(show="")
                toggle_button.configure(text="Hide")  # видно

        password_window = ctk.CTkToplevel(tab_frame)
        password_window.title("Підтвердження паролем")
        password_window.geometry("300x200")
        password_window.grab_set()

        label = ctk.CTkLabel(password_window, text="Введіть пароль для підтвердження:")
        label.pack(pady=10)

        password_frame = ctk.CTkFrame(password_window, fg_color="transparent")
        password_frame.pack(pady=5, padx=20, fill="x")

        password_var = ctk.StringVar()
        password_entry = ctk.CTkEntry(password_frame, textvariable=password_var, show="*")
        password_entry.pack(side="left", fill="x", expand=True)

        toggle_button = ctk.CTkButton(password_frame, text="Show", width=30, command=toggle_password_visibility)
        toggle_button.pack(side="right", padx=(5, 0))

        error_label = ctk.CTkLabel(password_window, text="", text_color="red")
        error_label.pack(pady=(10, 0))

        def confirm():
            password = password_var.get()
            result = delete_pdf(f_id, password)
            if result:
                password_window.destroy()
                show_popup(f"Файл з ID={f_id} успішно видалено!", color="#90EE90")
                update_file_list(get_all_files_request())
            else:
                error_label.configure(text="❌ Невірний пароль або файл не знайдено")
                show_popup("Невірний пароль або файл не знайдено!", title="⚠ Warning", color="yellow")

        confirm_button = ctk.CTkButton(password_window, text="Підтвердити", command=confirm)
        confirm_button.pack(pady=0)

    update_file_list(get_all_files_request())
    return update_file_list
