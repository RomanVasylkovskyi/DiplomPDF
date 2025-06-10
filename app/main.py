import customtkinter as ctk

from tabs.participants_tab import create_participants_tab
from tabs.files_tab import create_files_tab
from tabs.admin_menu_tab import create_admin_menu_tab

from backend import get_all_files_request

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("900x900")
app.title("Discussion Protocol")

tabview = ctk.CTkTabview(app, width=880, height=660)
tabview.pack(padx=10, pady=1)


tabview.add("Participants")
tabview.add("Files")
tabview.add("Admin Menu")


create_participants_tab(tabview.tab("Participants"))
files_tab_update_file_list_func = create_files_tab(tabview.tab("Files"))
admin_tab_update_file_list_func = create_admin_menu_tab(tabview.tab("Admin Menu"))

current_tab_name = None  # глобальна змінна для збереження попередньої активної вкладки

def handle_tab_change():
    global current_tab_name
    selected_tab = tabview.get()
    if selected_tab != current_tab_name:
        current_tab_name = selected_tab
        print(f"🔄 Tab changed to: {selected_tab}")
        
        if selected_tab == "Files":
            on_files_tab_open()
        elif selected_tab == "Participants":
            on_participants_tab_open()
        elif selected_tab == "Admin Menu":
            on_admin_menu_tab_open()

    tabview.after(50, handle_tab_change)

def on_files_tab_open():
    files_tab_update_file_list_func(get_all_files_request())

def on_participants_tab_open():
    pass

def on_admin_menu_tab_open():
    admin_tab_update_file_list_func(get_all_files_request())

handle_tab_change()


app.mainloop()