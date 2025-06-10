import customtkinter as ctk

def show_popup(message: str, title: str = "Повідомлення", color: str = "white"):
    popup = ctk.CTkToplevel()
    popup.title(title)
    popup.geometry("360x100")
    popup.resizable(False, False)
    popup.attributes("-topmost", True)
    label = ctk.CTkLabel(
        popup,
        text=message,
        text_color=color,
        wraplength=340,
        justify="center"
    )
    label.pack(pady=20)

    ok_button = ctk.CTkButton(popup, text="OK", command=popup.destroy)
    ok_button.pack()

    popup.grab_set()