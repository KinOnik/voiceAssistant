import tkinter as tk
import speech_recognition as sr
import threading
from commands import execute_command
import json
import os
from settings import open_settings
import time

class VoiceAssistantApp:
    def __init__(self, root):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.root = root
        self.root.title("Voice Assistant")

        self.settings_file = "settings.json"
        self.load_settings()

        self.history = tk.Text(root, state="disabled")
        self.history.pack(pady=10)

        self.entry = tk.Entry(root)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.on_enter)

        self.mic_var = tk.StringVar(root)
        self.mic_list = self.list_microphones()
        self.mic_var.set(self.mic_list[self.selected_mic_index])

        self.microphone = sr.Microphone(device_index=self.selected_mic_index)

        self.recognize_button = tk.Button(root, text="Распознать речь", command=self.start_recognition_thread)
        self.recognize_button.pack(pady=5)

        self.settings_button = tk.Button(root, text="Настройки", command=lambda: open_settings(root, self))
        self.settings_button.pack(pady=5)

        self.status_label = tk.Label(root, text="Ожидание команды...")
        self.status_label.pack(pady=5)

        self.apply_theme()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        if self.listen_enabled:
            self.start_background_listening()

        self.microphone_lock = threading.Lock()

    def start_background_listening(self):
        if self.listen_enabled:  # Проверка включения
            self.background_thread = threading.Thread(target=self.background_listening)
            self.background_thread.daemon = True
            self.background_thread.start()

    def background_listening(self):
        while self.listen_enabled:  # Используйте listen_enabled для проверки
            try:
                mic = sr.Microphone(device_index=self.selected_mic_index)
                with mic as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source)
                    wake_word = self.recognizer.recognize_google(audio, language="ru-RU").lower()
                    if "ассистент привет" in wake_word:
                        self.log("Ключевая фраза распознана!")
                        self.start_recognition_thread()  # Запуск распознавания команд
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                self.log(f"Ошибка при обращении к сервису: {e}")
                break
            except AssertionError as e:
                self.log(f"Ошибка контекстного менеджера микрофона: {e}")
                break

    def start_recognition_thread(self):
        threading.Thread(target=self.recognize_speech).start()

    def recognize_speech(self):
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                command = self.recognizer.recognize_google(audio, language="ru-RU").lower()
                self.log(f"Вы сказали: {command}")
                self.process_command(command)
        except sr.UnknownValueError:
            self.log("Не удалось распознать речь.")
        except sr.RequestError as e:
            self.log(f"Ошибка при обращении к сервису: {e}")

    def process_command(self, command):
        self.status_label.config(text="Обработка команды...")
        execute_command(command, self)
        self.status_label.config(text="Ожидание команды...")

    def on_enter(self, event):
        command = self.entry.get().lower()
        self.log(f"Вы ввели: {command}")
        self.process_command(command)
        self.entry.delete(0, tk.END)

    def log(self, message):
        self.history.config(state="normal")
        self.history.insert(tk.END, f"{message}\n")
        self.history.config(state="disabled")
        self.history.see(tk.END)

    def list_microphones(self):
        mic_names = sr.Microphone.list_microphone_names()
        return [name.encode('utf-8').decode('utf-8') for name in mic_names]

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as file:
                settings = json.load(file)
                self.selected_mic_index = settings.get('selected_mic_index', 0)
                self.light_theme = settings.get('light_theme', True)
                self.applications = settings.get('applications', {})
                self.listen_enabled = settings.get('listen_enabled', True)
        else:
            self.selected_mic_index = 0
            self.light_theme = True
            self.applications = {}
            self.listen_enabled = True

    def save_settings(self):
        settings = {
            'selected_mic_index': self.selected_mic_index,
            'light_theme': self.light_theme,
            'applications': self.applications,
            'listen_enabled': self.listen_enabled
        }
        with open(self.settings_file, 'w') as file:
            json.dump(settings, file)

    def apply_theme(self):
        if self.light_theme:
            self.root.config(bg="white")
            self.history.config(bg="white", fg="black")
            self.entry.config(bg="white", fg="black")
        else:
            self.root.config(bg="black")
            self.history.config(bg="black", fg="white")
            self.entry.config(bg="black", fg="white")

    def on_closing(self):
        self.listen_enabled = False
        self.root.destroy()
        os._exit(0)

def start_gui():
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
