import sqlite3

def init_db():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history (command TEXT, response TEXT)''')
    conn.commit()
    conn.close()


def save_command(command, response):
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (command, response) VALUES (?, ?)", (command, response))
    conn.commit()
    conn.close()
