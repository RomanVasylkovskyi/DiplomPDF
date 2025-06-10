
from backend import download_pdf
from tabs.message_popup import show_popup
import os
import re

def download_file_wraper(fname, fpath):
    result, save_path = download_pdf(fname, fpath)
    filename = os.path.basename(save_path)
    if result:
        show_popup(f'Файл "{filename}" успішно завантажено!', color="#90EE90")
    else:
        show_popup("Файл не вдалось завантажити!", title="⚠ Warning", color="yellow")

def is_valid_filename(filename: str) -> bool:
    # 1. Порожній рядок або лише пробіли
    if not filename or filename.strip() == "":
        return False

    # 2. Заборонені символи для Windows / Linux / macOS
    invalid_chars = r'<>:"/\\|?*\n\r\t'
    if any(char in filename for char in invalid_chars):
        return False

    # 3. Максимальна довжина (255 символів — стандарт для більшості файлових систем)
    if len(filename) > 255:
        return False

    return True
