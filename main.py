from gui import start_gui
from database import init_db, save_command

def main():
    init_db()
    start_gui()

if __name__ == "__main__":
    main()
