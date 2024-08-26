import tkinter as tk
import speech_recognition as sr
from application_manager import open_application_manager

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
        self.mic_menu.pack(anchor="w", pady=5)

        self.listen_var = tk.BooleanVar(self.window, value=app.listen_enabled)
        tk.Checkbutton(self.window, text="Включить фоновое прослушивание", variable=self.listen_var).pack(anchor="w", pady=5)
        
        # Тема
        tk.Label(self.window, text="Тема:").pack(anchor="w")
        self.theme_var = tk.StringVar(self.window)
        self.theme_var.set("Светлая" if app.light_theme else "Тёмная")
        self.theme_menu = tk.OptionMenu(self.window, self.theme_var, "Светлая", "Тёмная")
        self.theme_menu.pack(anchor="w", pady=5)

        # Управление приложениями
        tk.Button(self.window, text="Управление приложениями", command=lambda: open_application_manager(self.window, app)).pack(anchor="w", pady=10)

        tk.Button(self.window, text="Сохранить", command=self.save_settings).pack(anchor="w", pady=5)

    def save_settings(self):
        # Сохранение микрофона
        selected_mic = self.mic_var.get()
        self.app.selected_mic_index = self.app.mic_list.index(selected_mic)
        self.app.microphone = sr.Microphone(device_index=self.app.selected_mic_index)

        # состояние прослушивания
        self.app.listen_enabled = self.listen_var.get()
        if self.app.listen_enabled:
            self.app.start_background_listening()

        # Сохранение темы
        selected_theme = self.theme_var.get()
        self.app.light_theme = (selected_theme == "Светлая")
        self.app.apply_theme()

        # Сохранение настроек
        self.app.save_settings()
        self.window.destroy()

def open_settings(parent, app):
    SettingsWindow(parent, app)
