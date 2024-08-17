import tkinter as tk
import speech_recognition as sr
import threading
from commands import execute_command
from database import save_command, init_db, load_history
import json
import os
from settings import open_settings

class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")

        self.settings_file = "settings.json"
        self.load_settings()

        self.history = tk.Text(root, state="disabled")
        self.history.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.mic_var = tk.StringVar(root)
        self.mic_list = self.list_microphones()
        self.mic_var.set(self.mic_list[self.selected_mic_index])

        self.mic_menu = tk.OptionMenu(root, self.mic_var, *self.mic_list, command=self.update_microphone)
        self.mic_menu.pack()

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=self.selected_mic_index)

        self.recognize_button = tk.Button(root, text="Распознать речь", command=self.start_recognition_thread)
        self.recognize_button.pack()

        self.settings_button = tk.Button(root, text="Настройки", command=lambda: open_settings(root, self))
        self.settings_button.pack()

        self.apply_theme()

        if self.listen_enabled:
            self.start_wake_word_thread()

    def start_wake_word_thread(self):
        threading.Thread(target=self.listen_for_wake_word).start()

    def listen_for_wake_word(self):
        try:
            while self.listen_enabled:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    print("Жду ключевую фразу...")
                    audio = self.recognizer.listen(source)
                    try:
                        command = self.recognizer.recognize_google(audio, language="ru-RU").lower()
                        if "привет, помощник" in command:
                            self.log("Активирован по ключевой фразе")
                            self.root.after(0, self.start_recognition_thread)  # Используем after для вызова в основном потоке
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        self.log(f"Ошибка при обращении к сервису: {e}")
        except Exception as e:
            self.log(f"Произошла ошибка: {e}")



    def update_microphone(self, selection):
        self.selected_mic_index = self.mic_list.index(selection)
        self.microphone = sr.Microphone(device_index=self.selected_mic_index)
        self.save_settings()
        self.log(f"Микрофон изменен на: {selection}")

    def start_recognition_thread(self):
        threading.Thread(target=self.recognize_speech).start()

    def recognize_speech(self):
        self.log("Слушаю...")
        self.root.update()

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source)
                command = self.recognizer.recognize_google(audio, language="ru-RU").lower()
                self.log(f"Вы сказали: {command}")
                self.process_command(command)
            except sr.UnknownValueError:
                self.log("Не удалось распознать речь.")
            except sr.RequestError as e:
                self.log(f"Ошибка при обращении к сервису: {e}")

    def process_command(self, command):
        if command in commands:
            execute_command(command)
            save_command(command, "OK")
        else:
            self.log("Неизвестная команда.")

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
                self.listen_enabled = settings.get('listen_enabled', True)
        else:
            self.selected_mic_index = 0
            self.light_theme = True
            self.listen_enabled = True

    def save_settings(self):
        settings = {
            'selected_mic_index': self.selected_mic_index,
            'light_theme': self.light_theme,
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

def start_gui():
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
