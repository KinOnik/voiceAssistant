from voice_recognition import recognize_speech
from commands import execute_command
from gui import start_gui
from database import init_db, save_command

def main():
    init_db()
    start_gui()

    while True:
        command = recognize_speech()
        if command:
            execute_command(command)
            save_command(command, "OK")

if __name__ == "__main__":
    main()
