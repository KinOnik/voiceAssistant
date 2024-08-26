import tkinter as tk
from tkinter import filedialog, messagebox

class ApplicationManager:
    def __init__(self, parent, app):
        self.app = app
        self.window = tk.Toplevel(parent)
        self.window.title("Управление приложениями")

        self.listbox = tk.Listbox(self.window)
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=10)

        self.populate_listbox()

        tk.Button(self.window, text="Редактировать", command=self.edit_application).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.window, text="Удалить", command=self.delete_application).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.window, text="Добавить новое", command=self.add_new_application).pack(side=tk.RIGHT, padx=5, pady=5)

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for name in self.app.applications.keys():
            self.listbox.insert(tk.END, name)

    def add_new_application(self):
        self.edit_application(new=True)

    def edit_application(self, new=False):
        if not new:
            selected_index = self.listbox.curselection()
            if not selected_index:
                messagebox.showwarning("Выбор приложения", "Пожалуйста, выберите приложение для редактирования.")
                return
            old_name = self.listbox.get(selected_index)
            old_path = self.app.applications[old_name]
        else:
            old_name = ""
            old_path = ""

        self.edit_window = tk.Toplevel(self.window)
        self.edit_window.title("Редактирование приложения" if not new else "Добавление нового приложения")

        tk.Label(self.edit_window, text="Название:").pack(anchor="w")
        self.name_var = tk.StringVar(self.edit_window, value=old_name)
        tk.Entry(self.edit_window, textvariable=self.name_var).pack(anchor="w", pady=5)

        tk.Label(self.edit_window, text="Путь к приложению:").pack(anchor="w")
        self.path_var = tk.StringVar(self.edit_window, value=old_path)
        tk.Entry(self.edit_window, textvariable=self.path_var).pack(anchor="w", pady=5)

        tk.Button(self.edit_window, text="Выбрать файл", command=self.select_app_path).pack(anchor="w", pady=5)

        save_button_text = "Сохранить изменения" if not new else "Добавить приложение"
        tk.Button(self.edit_window, text=save_button_text, command=lambda: self.save_application(old_name)).pack(anchor="w", pady=5)

    def select_app_path(self):
        path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        if path:
            self.path_var.set(path)

    def save_application(self, old_name):
        new_name = self.name_var.get()
        new_path = self.path_var.get()

        if new_name and new_path:
            if old_name:
                del self.app.applications[old_name]
            self.app.applications[new_name] = new_path
            self.app.save_settings()
            self.populate_listbox()
            self.edit_window.destroy()
            print(f"Приложение {new_name} сохранено с путём {new_path}")
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите название и путь к приложению.")

    def delete_application(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Выбор приложения", "Пожалуйста, выберите приложение для удаления.")
            return

        app_name = self.listbox.get(selected_index)
        del self.app.applications[app_name]
        self.app.save_settings()
        self.populate_listbox()
        print(f"Приложение {app_name} удалено")

def open_application_manager(parent, app):
    ApplicationManager(parent, app)
