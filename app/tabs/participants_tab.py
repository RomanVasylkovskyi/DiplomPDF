import customtkinter as ctk
from database.worker import get_all_worker


def create_participants_tab(tab_frame):
    users = get_all_worker()
    user_map = {f"{u.surname} {u.name} — {u.position}": u for u in users}
    user_names = list(user_map.keys())

    added_users = []

    def on_user_selected(user_str):
        user = user_map[user_str]
        if user not in added_users:
            added_users.append(user)
            refresh_added_users()

    selected_user = ctk.StringVar(value=user_names[0])
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

        remove_button = ctk.CTkButton(inner, text="Видалити", width=80, command=lambda: wrapper.destroy())
        remove_button.pack(pady=(5, 0))
