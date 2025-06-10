import customtkinter as ctk
from datetime import datetime
import requests
from backend import get_all_files_request
from tabs.menu_utils import download_file_wraper

def create_files_tab(tab_frame):
    search_frame = ctk.CTkFrame(tab_frame)
    search_frame.pack(pady=10, padx=10, fill="x")

    search_var = ctk.StringVar()

    def on_search_var_change(*args):
        query = search_var.get().lower()
        all_files = get_all_files_request()
        print("allfiles", all_files)
        if query:
            filtered_files = []
            for f in all_files:
                fields = [
                    f.name.lower() if f.name else "",
                    str(f.id).lower(),
                    str(f.datetime) if f.datetime else "",
                    f.description.lower() if f.description else ""
                ]
                if any(query in field for field in fields):
                    filtered_files.append(f)
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
            row = ctk.CTkFrame(
                results_frame,
                border_width=1,
                corner_radius=8,
                fg_color="transparent"
            )
            row.pack(fill="x", padx=10, pady=5)

            id_label = ctk.CTkLabel(row, text=file.id, anchor="w", width=40)
            id_label.pack(side="left", padx=5, pady=10, expand=True)

            name_label = ctk.CTkLabel(row, text=file.name, anchor="w", width=300)
            name_label.pack(side="left", padx=5, pady=10, expand=True)

            date_label = ctk.CTkLabel(row, text=file.datetime.strftime("%Y-%m-%d %H:%M"), anchor="w", width=140)
            date_label.pack(side="left", padx=5, pady=10, expand=True)

            download_button = ctk.CTkButton(
                row, text="Скачати", width=100, 
                command=lambda fname=file.name, fpath=file.path: download_button_handler(fname, fpath))
            download_button.pack(side="right", padx=5)

            file_rows.append(row)

    def download_button_handler(fname, fpath):
        download_file_wraper(fname, fpath)
        update_file_list(get_all_files_request())

    update_file_list(get_all_files_request())
    return update_file_list
