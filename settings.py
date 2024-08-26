import tkinter as tk
import speech_recognition as sr
from application_manager import open_application_manager
from sites_manager import open_sites_manager

class SettingsWindow:
    def __init__(self, parent, app):
        self.app = app
        self.window = tk.Toplevel(parent)
        self.window.title("Настройки")
        
        self.window_width = 400
        self.window_height = 270
        self.window.minsize(self.window_width, self.window_height)
        self.window.geometry(f"{self.window_width}x{self.window_height}")
        self.center_window()

        self.main_frame = tk.Frame(self.window, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Выбор микрофона
        tk.Label(self.main_frame, text="Выбор микрофона:").grid(row=0, column=0, sticky="w")
        self.mic_var = tk.StringVar(self.main_frame)
        self.mic_var.set(app.mic_list[app.selected_mic_index])
        self.mic_menu = tk.OptionMenu(self.main_frame, self.mic_var, *app.mic_list)
        self.mic_menu.grid(row=0, column=1, sticky="ew", pady=5)

        self.listen_var = tk.BooleanVar(self.main_frame, value=app.listen_enabled)
        tk.Checkbutton(self.main_frame, text="Включить фоновое прослушивание", variable=self.listen_var).grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

        # Фраза активации
        tk.Label(self.main_frame, text="Фраза активации:").grid(row=2, column=0, sticky="w")
        self.wake_word_entry = tk.Entry(self.main_frame)
        self.wake_word_entry.insert(0, app.wake_word)  
        self.wake_word_entry.grid(row=2, column=1, sticky="ew", pady=5)

        # Тема
        tk.Label(self.main_frame, text="Тема:").grid(row=3, column=0, sticky="w")
        self.theme_var = tk.StringVar(self.main_frame)
        self.theme_var.set("Светлая" if app.light_theme else "Тёмная")
        self.theme_menu = tk.OptionMenu(self.main_frame, self.theme_var, "Светлая", "Тёмная")
        self.theme_menu.grid(row=3, column=1, sticky="ew", pady=5)

        # Управление приложениями и сайтами
        button_frame = tk.Frame(self.main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
        tk.Button(button_frame, text="Управление приложениями", command=lambda: open_application_manager(self.window, app)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Управление сайтами", command=lambda: open_sites_manager(self.window, app)).pack(side=tk.RIGHT, padx=5)

        tk.Button(self.main_frame, text="Сохранить", command=self.save_settings).grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")

        
    def center_window(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = (screen_width / 2) - (self.window_width / 2)
        y = (screen_height / 2) - (self.window_height / 2)

        self.window.geometry(f"{self.window_width}x{self.window_height}+{int(x)}+{int(y)}")

    def save_settings(self):
        # микрофон
        selected_mic = self.mic_var.get()
        self.app.selected_mic_index = self.app.mic_list.index(selected_mic)
        self.app.microphone = sr.Microphone(device_index=self.app.selected_mic_index)
        
        # фраза активации
        self.app.wake_word = self.wake_word_entry.get()
        
        # состояние прослушивания
        self.app.listen_enabled = self.listen_var.get()
        if self.app.listen_enabled:
            self.app.start_background_listening()

        # тема
        selected_theme = self.theme_var.get()
        self.app.light_theme = (selected_theme == "Светлая")
        self.app.apply_theme()

        self.app.save_settings()
        self.window.destroy()

def open_settings(parent, app):
    SettingsWindow(parent, app)
