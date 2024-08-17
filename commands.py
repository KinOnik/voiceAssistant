import re
import os
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

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
    "увеличь громкость": lambda: change_volume(10),
    "уменьши громкость": lambda: change_volume(-10),
}

def execute_command(command, app):
    if command in commands:
        print(f"Выполняется команда: {command}")
        commands[command]()
    else:
        match = re.search(r'установи громкость (\d+)', command)
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
        else:
            print("Неизвестная команда.")