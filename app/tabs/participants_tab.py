import customtkinter as ctk
from tkcalendar import DateEntry
import datetime
import tkinter as tk
from backend import PDFRequest, Participant, Question, send_pdf_request, get_all_worker_request

def create_participants_tab(tab_frame):
    ### Doc name part ###
    label = ctk.CTkLabel(tab_frame, text="Генерація PDF", font=ctk.CTkFont(size=16))
    label.pack(pady=(20, 10))

    row_frame = ctk.CTkFrame(tab_frame)
    row_frame.pack(fill="x", padx=10, pady=5)

    filename_entry = ctk.CTkEntry(row_frame, placeholder_text="Назва файлу")
    filename_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

    today = datetime.date.today()
    date_entry = DateEntry(row_frame, width=12, background='darkblue',
                           foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    date_entry.set_date(today)
    date_entry.pack(side="left")


    ### Worker part ###
    users = get_all_worker_request()
    user_map = {f"{u.surname} {u.name} — {u.position}": u for u in users}
    user_names = list(user_map.keys())

    added_users = []

    def on_user_selected(user_str):
        user = user_map[user_str]
        if user not in added_users:
            added_users.append(user)
            refresh_added_users()

    selected_user = ctk.StringVar(value=user_names[0] if user_names else "")
    user_option_menu = ctk.CTkOptionMenu(
        tab_frame,
        variable=selected_user,
        values=user_names,
        command=on_user_selected
    )
    user_option_menu.pack(pady=5, padx=10, anchor="w")

    scrollable_users_frame = ctk.CTkScrollableFrame(tab_frame, height=150)
    scrollable_users_frame.pack(pady=5, padx=10, fill="both", expand=False)

    def refresh_added_users():
        for widget in scrollable_users_frame.winfo_children():
            widget.destroy()

        for user in added_users:
            row = ctk.CTkFrame(
                scrollable_users_frame,
                border_width=1,
                border_color="#666666",
                corner_radius=6,
                fg_color="transparent"
            )
            row.pack(fill="x", pady=5, padx=5)

            content = ctk.CTkFrame(row, fg_color="transparent")
            content.pack(fill="x", padx=10, pady=5)

            label = ctk.CTkLabel(
                content,
                text=f"{user.surname} {user.name} — {user.position}",
                anchor="w"
            )
            label.pack(side="left", padx=(5, 10), expand=True)

            def make_remove_callback(u=user):
                return lambda: remove_user(u)

            remove_button = ctk.CTkButton(content, text="Видалити", width=80, command=make_remove_callback())
            remove_button.pack(side="right", padx=5)

    def remove_user(user):
        if user in added_users:
            added_users.remove(user)
            refresh_added_users()

    separator = ctk.CTkLabel(tab_frame, text="─" * 60)
    separator.pack(pady=10)

    added_topics = []

    add_topic_button = ctk.CTkButton(tab_frame, text="Додати тему обговорення", command=lambda: add_topic_fields())
    add_topic_button.pack(pady=(5, 10))

    topics_frame = ctk.CTkScrollableFrame(tab_frame, height=250)
    topics_frame.pack(padx=10, pady=(0, 10), fill="both", expand=True)
    
    def add_topic_fields():
        wrapper = ctk.CTkFrame(
            topics_frame,
            border_width=1,
            border_color="#666666",
            corner_radius=6,
            fg_color="transparent"
        )
        wrapper.pack(fill="x", pady=5, padx=5)

        inner = ctk.CTkFrame(wrapper, fg_color="transparent")
        inner.pack(fill="x", padx=10, pady=10)

        topic_entry = ctk.CTkEntry(inner, placeholder_text="Тема обговорення")
        topic_entry.pack(fill="x", padx=5, pady=(0, 5))

        result_textbox = ctk.CTkTextbox(inner, height=120)
        result_textbox.insert("0.0", "Результати")
        result_textbox.pack(fill="x", padx=5, pady=(0, 5))

        remove_button = ctk.CTkButton(inner, text="Видалити", width=80, command=lambda: remove_topic_fields(wrapper))
        remove_button.pack(pady=(5, 0))
    
        added_topics.append((wrapper, topic_entry, result_textbox))
    
    def remove_topic_fields(wrapper):
        # Видаляємо відповідний елемент зі списку
        for item in added_topics:
            if item[0] == wrapper:
                added_topics.remove(item)
                break
        # Знищуємо вікно з інтерфейсу
        wrapper.destroy()


    generate_button = ctk.CTkButton(tab_frame, text="Згенерувати PDF", command=lambda: generate_pdf_callback())
    generate_button.pack(pady=(15, 10))

    def generate_pdf_callback():
        filename_text = filename_entry.get()
        selected_date_str = date_entry.get()
        participant_data = []
        for worker in added_users:
            participant_data.append(Participant(name=worker.surname +" "+ worker.name +" "+ worker.patronymic, role=worker.position))
        topic_data = []
        for topic in added_topics:
            topic_name = topic[1].get()
            topic_result = topic[2].get("0.0", "end").strip()
            topic_data.append(Question(question=topic_name, decision=topic_result))

        print(f"Генеруємо PDF з назвою: {filename_text}")
        print(f"users: {participant_data}")
        print(f"topics: {topic_data}")

        request_data = PDFRequest(
            filename=filename_text,
            datetime=selected_date_str,
            participants=participant_data,
            questions=topic_data
        )
        send_pdf_request(request_data)