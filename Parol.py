# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 16:53:28 2026

@author: student
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

# Параметры по умолчанию
DEFAULT_MIN_LENGTH = 8
DEFAULT_MAX_LENGTH = 32

# Файл для хранения истории
HISTORY_FILE = 'history.json'

# Загрузка истории из файла
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Сохранение истории в файл
def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# Генерация пароля
def generate_password(length, use_digits, use_letters, use_special):
    chars = ''
    if use_letters:
        chars += string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_special:
        chars += string.punctuation

    if not chars:
        return ''
    return ''.join(random.choices(chars, k=length))

# Обработчик кнопки "Сгенерировать"
def on_generate():
    try:
        length = int(length_var.get())
        if length < DEFAULT_MIN_LENGTH or length > DEFAULT_MAX_LENGTH:
            messagebox.showwarning(
                "Ошибка", 
                f"Длина пароля должна быть от {DEFAULT_MIN_LENGTH} до {DEFAULT_MAX_LENGTH} символов."
            )
            return

        password = generate_password(
            length,
            digits_var.get(),
            letters_var.get(),
            special_var.get()
        )

        if not password:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов.")
            return

        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

        # Добавляем в историю (максимум 10 последних)
        history.append(password)
        if len(history) > 10:
            history.pop(0)
        save_history(history)
        update_history_table()

    except ValueError:
        messagebox.showerror("Ошибка", "Некорректная длина пароля.")

# Обновление таблицы истории
def update_history_table():
    for i in history_table.get_children():
        history_table.delete(i)
    for pwd in history:
        history_table.insert('', tk.END, values=(pwd,))

# Очистка истории
def clear_history():
    global history
    if messagebox.askyesno("Очистить историю", "Удалить всю историю?"):
        history = []
        save_history(history)
        update_history_table()

# Главное окно
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("500x450")
root.resizable(False, False)

# Переменные
length_var = tk.IntVar(value=12)
digits_var = tk.BooleanVar(value=True)
letters_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)
history = load_history()

# Фрейм настроек
settings_frame = ttk.LabelFrame(root, text="Настройки")
settings_frame.pack(pady=10, padx=10, fill=tk.X)

# Длина пароля
ttk.Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
length_slider = ttk.Scale(
    settings_frame,
    from_=DEFAULT_MIN_LENGTH,
    to=DEFAULT_MAX_LENGTH,
    orient=tk.HORIZONTAL,
    variable=length_var,
    length=250
)
length_slider.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
ttk.Label(settings_frame, textvariable=length_var).grid(row=0, column=3, padx=5)

# Чекбоксы символов
ttk.Checkbutton(settings_frame, text="Цифры", variable=digits_var).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
ttk.Checkbutton(settings_frame, text="Буквы", variable=letters_var).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
ttk.Checkbutton(settings_frame, text="Спецсимволы", variable=special_var).grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)

# Кнопка генерации и поле результата
ttk.Button(root, text="Сгенерировать", command=on_generate).pack(pady=5)
password_entry = ttk.Entry(root, width=40)
password_entry.pack(pady=5)

# Фрейм истории
history_frame = ttk.LabelFrame(root, text="История")
history_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

history_table = ttk.Treeview(history_frame, columns=("password",), show="headings", height=5)
history_table.heading("password", text="Пароль")
history_table.column("password", width=400)
history_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=history_table.yview)
history_table.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

ttk.Button(root, text="Очистить историю", command=clear_history).pack(pady=5)

# Заполнение таблицы истории при запуске
update_history_table()

root.mainloop()