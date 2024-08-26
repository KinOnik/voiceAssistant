import json
import re
import os
import webbrowser
import keyboard
import speech_recognition as sr
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def load_settings():
    settings_file = "settings.json"
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as file:
            settings = json.load(file)
            return settings.get('selected_mic_index', 0)
    return 0

def get_audio_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None)
    interface = cast(interface, POINTER(IAudioEndpointVolume))
    return interface

def change_volume(delta):
    interface = get_audio_interface()
    volume = interface.GetMasterVolumeLevelScalar()
    new_volume = min(max(volume + delta / 100.0, 0.0), 1.0)
    interface.SetMasterVolumeLevelScalar(new_volume, None)
    print(f"Установлена громкость: {new_volume * 100:.0f}%")

def set_volume(level):
    interface = get_audio_interface()
    new_volume = min(max(level / 100.0, 0.0), 1.0)
    interface.SetMasterVolumeLevelScalar(new_volume, None)
    print(f"Установлена громкость: {new_volume * 100:.0f}%")

commands = {
    "увеличь громкость": lambda: change_volume(5),
    "уменьши громкость": lambda: change_volume(-5),    
}

def execute_command(command, app):        
    if command in commands:
        print(f"Выполняется команда: {command}")
        commands[command]()
    elif "скриншот" in command:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        print("Скриншот сохранен.")
    elif command.startswith("введи текст"):
        print("Ожидание ввода текста...")
        text = listen_for_text()
        if text:
            keyboard.write(text)
    elif "отправь" in command:
        keyboard.press('enter')
    else:
        match = re.search(r'установи громкость (\d+)', command) #or re.search(r'громкость (\d+)', command)
        if match:
            level = int(match.group(1))
            set_volume(level)
        elif command.startswith("запусти "):
            app_name = command.split("запусти ")[-1].strip().lower()
            app_path = app.applications.get(app_name)
            if app_path:
                try:
                    os.startfile(app_path)
                    print(f"Запущено приложение: {app_name}")
                except Exception as e:
                    print(f"Не удалось запустить приложение '{app_name}': {e}")
            else:
                print(f"Приложение с названием '{app_name}' не найдено.")
        elif command.startswith("открой "):
            site_name = command.split("открой ")[-1].strip().lower()
            site_url = None
            for site_names, url in app.sites.items():
                if site_name in site_names:
                    site_url = url
                    break

            if site_url:
                webbrowser.open(site_url)
                print(f"Открыт сайт: {site_name}")
            else:
                print(f"Сайт с названием '{site_name}' не найден.")
        else:
            print("Неизвестная команда.")

def listen_for_text():
    mic_index = load_settings()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=mic_index)

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Говорите текст для ввода...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Распознанный текст: {text}")
            return text
        except sr.UnknownValueError:
            print("Не удалось распознать речь.")
            return ""
        except sr.RequestError as e:
            print(f"Ошибка при обращении к сервису: {e}")
            return ""