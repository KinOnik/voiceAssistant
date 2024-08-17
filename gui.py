import tkinter as tk
import speech_recognition as sr
import threading

class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")

        # Поле для истории команд
        self.history = tk.Text(root, state="disabled")
        self.history.pack()

        # Поле для ввода команд
        self.entry = tk.Entry(root)
        self.entry.pack()

        # Список микрофонов
        self.mic_var = tk.StringVar(root)
        self.mic_list = list_microphones()
        self.mic_var.set(self.mic_list[0])  # Устанавливаем первый микрофон по умолчанию

        self.mic_menu = tk.OptionMenu(root, self.mic_var, *self.mic_list, command=self.update_microphone)
        self.mic_menu.pack()

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()  # По умолчанию первый микрофон

        # Кнопка для запуска распознавания речи
        self.recognize_button = tk.Button(root, text="Распознать речь", command=self.start_recognition_thread)
        self.recognize_button.pack()

    def update_microphone(self, selection):
        mic_index = self.mic_list.index(selection)
        self.microphone = sr.Microphone(device_index=mic_index)
        self.log(f"Микрофон изменен на: {selection}")

    def start_recognition_thread(self):
        # Запускаем распознавание речи в отдельном потоке
        threading.Thread(target=self.recognize_speech).start()

    def recognize_speech(self):
        self.log("Слушаю...")  # Выводим сообщение "Слушаю..."
        self.root.update()  # Обновляем интерфейс, чтобы текст отобразился сразу

        recognizer = sr.Recognizer()
        with self.microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio, language="ru-RU")
                self.log(f"Вы сказали: {command}")
                # Вызов метода для обработки команды
                self.process_command(command)
            except sr.UnknownValueError:
                self.log("Не удалось распознать речь.")
            except sr.RequestError as e:
                self.log(f"Ошибка при обращении к сервису: {e}")

    def process_command(self, command):
        # Метод для обработки команды, который можно переопределить в зависимости от логики
        pass

    def log(self, message):
        self.history.config(state="normal")
        self.history.insert(tk.END, f"{message}\n")
        self.history.config(state="disabled")
        self.history.see(tk.END)  # Прокручиваем текстовое поле до последней записи

def list_microphones():
    return sr.Microphone.list_microphone_names()

def start_gui():
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
