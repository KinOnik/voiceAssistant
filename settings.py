import tkinter as tk
from tkinter import filedialog
import json
import os
import speech_recognition as sr
from database import load_history, save_command

class SettingsWindow:
    def __init__(self, parent, app):
        self.app = app
        self.window = tk.Toplevel(parent)
        self.window.title("Настройки")

        # Выбор микрофона
        tk.Label(self.window, text="Выбор микрофона:").pack(anchor="w")
        self.mic_var = tk.StringVar(self.window)
        self.mic_var.set(app.mic_list[app.selected_mic_index])
        self.mic_menu = tk.OptionMenu(self.window, self.mic_var, *app.mic_list)
        self.mic_menu.pack(anchor="w",pady=5)

        # Импорт/Экспорт истории
        tk.Button(self.window, text="Экспорт истории", command=self.export_history).pack(anchor="w",pady=5)
        tk.Button(self.window, text="Импорт истории", command=self.import_history).pack(anchor="w",pady=5)

        # Тема
        tk.Label(self.window, text="Тема:").pack(anchor="w")
        self.theme_var = tk.StringVar(self.window)
        self.theme_var.set("Светлая" if app.light_theme else "Тёмная")
        self.theme_menu = tk.OptionMenu(self.window, self.theme_var, "Светлая", "Тёмная")
        self.theme_menu.pack(anchor="w")

        # Прослушивание и активация по ключевой фразе
        self.listen_var = tk.BooleanVar(self.window, value=app.listen_enabled)
        tk.Checkbutton(self.window, text="Включить прослушивание", variable=self.listen_var).pack(anchor="w",pady=5)
        
        tk.Label(self.window, text="Добавить приложение:").pack(anchor="w",pady=5)
        self.app_name_var = tk.StringVar(self.window)
        self.app_path_var = tk.StringVar(self.window)
        
        tk.Label(self.window, text="Название:").pack(anchor="w",pady=5)
        tk.Entry(self.window, textvariable=self.app_name_var).pack(anchor="w",pady=5)
        
        tk.Label(self.window, text="Путь к приложению:").pack(anchor="w",pady=5)
        tk.Entry(self.window, textvariable=self.app_path_var).pack(anchor="w",pady=5)
        
        tk.Button(self.window, text="Выбрать файл", command=self.select_app_path).pack(anchor="w",pady=5)
        tk.Button(self.window, text="Добавить приложение", command=self.add_application).pack(anchor="w",pady=5)       
        

        tk.Button(self.window, text="Сохранить", command=self.save_settings).pack(anchor="w", pady=5)
        
    def save_settings(self):
        # Сохранение микрофона
        selected_mic = self.mic_var.get()
        self.app.selected_mic_index = self.app.mic_list.index(selected_mic)
        self.app.microphone = sr.Microphone(device_index=self.app.selected_mic_index)
        
        # Сохранение темы
        selected_theme = self.theme_var.get()
        self.app.light_theme = (selected_theme == "Светлая")
        self.app.apply_theme()

        # Сохранение прослушивания
        self.app.listen_enabled = self.listen_var.get()

        # Сохранение настроек
        self.app.save_settings()
        self.window.destroy()
        

    def export_history(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filepath:
            history = load_history()
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(history, file, ensure_ascii=False, indent=4)

    def import_history(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as file:
                history = json.load(file)
                for command, response in history:
                    save_command(command, response)

    def select_app_path(self):
        path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        if path:
            self.app_path_var.set(path)

    def add_application(self):
        app_name = self.app_name_var.get()
        app_path = self.app_path_var.get()
        if app_name and app_path:
            self.app.applications[app_name] = app_path
            self.save_settings()
            print(f"Приложение {app_name} добавлено с путём {app_path}")

          

def open_settings(parent, app):
    SettingsWindow(parent, app)
