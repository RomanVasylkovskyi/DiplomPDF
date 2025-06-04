import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def clear_window(_app):
    for widget in _app.winfo_children():
        widget.destroy()
    print('clear')


# --- Функція для другого інтерфейсу ---
def load_second_view(app):
    label = ctk.CTkLabel(app, text="Другий інтерфейс")
    label.pack(pady=20)

    back_button = ctk.CTkButton(app, text="Повернутися назад", command=lambda: [clear_window(app), load_main_view(app)])
    back_button.pack(pady=10)

# --- Основний інтерфейс ---
def load_main_view(app):
    entry = ctk.CTkEntry(app, placeholder_text="Введіть текст")
    entry.pack(pady=10)

    output_label = ctk.CTkLabel(app, text="Результат з'явиться тут")
    output_label.pack(pady=10)

    def on_click():
        text = entry.get()
        output_label.configure(text=f"Ви ввели: {text}")

    button = ctk.CTkButton(app, text="Показати", command=on_click)
    button.pack(pady=10)

    switch_button = ctk.CTkButton(app, text="Очистити і показати інше", command=lambda: [clear_window(app), load_second_view(app)])
    switch_button.pack(pady=20)