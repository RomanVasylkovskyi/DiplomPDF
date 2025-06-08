import customtkinter as ctk

def create_participants_tab(tab_frame):
    users = ["Іван Петренко", "Олена Сидорова", "Максим Іванов", "Наталія Коваль",
             "Олег Бондар", "Світлана Павленко", "Андрій Мельник", "Юлія Кравець"]

    added_users = []

    def on_user_selected(user):
        if user not in added_users:
            added_users.append(user)
            refresh_added_users()

    selected_user = ctk.StringVar(value=users[0])
    user_option_menu = ctk.CTkOptionMenu(tab_frame, variable=selected_user, values=users, command=on_user_selected)
    user_option_menu.pack(pady=5, padx=10, anchor="w")

    scrollable_users_frame = ctk.CTkScrollableFrame(tab_frame, height=150)
    scrollable_users_frame.pack(pady=5, padx=10, fill="both", expand=False)

    def refresh_added_users():
        for widget in scrollable_users_frame.winfo_children():
            widget.destroy()

        for user in added_users:
            row = ctk.CTkFrame(scrollable_users_frame)
            row.pack(fill="x", pady=2, padx=5)

            label = ctk.CTkLabel(row, text=user, anchor="w")
            label.pack(side="left", padx=(5, 10), expand=True)

            def make_remove_callback(u=user):
                return lambda: remove_user(u)

            remove_button = ctk.CTkButton(row, text="Видалити", width=80, command=make_remove_callback())
            remove_button.pack(side="right", padx=5)

    def remove_user(user):
        if user in added_users:
            added_users.remove(user)
            refresh_added_users()

    # Роздільник
    separator = ctk.CTkLabel(tab_frame, text="─" * 60)
    separator.pack(pady=10)

    # Кнопка додавання теми обговорення
    add_topic_button = ctk.CTkButton(tab_frame, text="Додати тему обговорення", command=lambda: add_topic_fields())
    add_topic_button.pack(pady=(5, 10))

    # Список тем
    topics_frame = ctk.CTkScrollableFrame(tab_frame, height=250)
    topics_frame.pack(padx=10, pady=(0, 10), fill="both", expand=True)

    def add_topic_fields():
        row = ctk.CTkFrame(topics_frame)
        row.pack(fill="x", pady=5, padx=5)

        topic_entry = ctk.CTkEntry(row, placeholder_text="Тема обговорення")
        topic_entry.pack(side="left", padx=5, expand=True, fill="x")

        result_entry = ctk.CTkEntry(row, placeholder_text="Результати")
        result_entry.pack(side="left", padx=5, expand=True, fill="x")

        def remove_row():
            row.destroy()

        remove_button = ctk.CTkButton(row, text="Видалити", width=80, command=remove_row)
        remove_button.pack(side="right", padx=5)
