import tkinter as tk
from tkinter import filedialog, messagebox

class SitesManager:
    def __init__(self, parent, app):
        self.app = app
        self.window = tk.Toplevel(parent)
        self.window.title("Управление сайтами")
     
        self.window_width = 400
        self.window_height = 250
        self.window.minsize(self.window_width, self.window_height)
        self.window.geometry(f"{self.window_width}x{self.window_height}")
        self.center_window(self.window)

        self.listbox = tk.Listbox(self.window)
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=10)

        self.populate_listbox()

        tk.Button(self.window, text="Редактировать", command=self.edit_site).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.window, text="Удалить", command=self.delete_site).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.window, text="Добавить новый", command=self.add_new_site).pack(side=tk.RIGHT, padx=10, pady=10)

    def center_window(self, window):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = (screen_width / 2) - (self.window_width / 2)
        y = (screen_height / 2) - (self.window_height / 2)
        
        self.window.geometry(f"{self.window_width}x{self.window_height}+{int(x)}+{int(y)}")

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for name in self.app.sites.keys():
            self.listbox.insert(tk.END, name)

    def add_new_site(self):
        self.edit_site(new=True)

    def edit_site(self, new=False):
        if not new:
            selected_index = self.listbox.curselection()
            if not selected_index:
                messagebox.showwarning("Выбор сайта", "Пожалуйста, выберите сайт для редактирования.")
                return
            old_name = self.listbox.get(selected_index)
            old_url = self.app.sites[old_name]
        else:
            old_name = ""
            old_url = ""

        self.edit_window = tk.Toplevel(self.window)
        self.edit_window.title("Редактирование сайта" if not new else "Добавление нового сайта")
        
        self.window_edit_width = 320
        self.window_edit_height = 110
        self.edit_window.minsize(self.window_edit_width, self.window_edit_height)
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = (screen_width / 2) - (self.window_edit_width / 2)
        y = (screen_height / 2) - (self.window_edit_height / 2)
        
        self.edit_window.geometry(f"{self.window_edit_width}x{self.window_edit_height}+{int(x)}+{int(y)}")
        
        tk.Label(self.edit_window, text="Название:", anchor="e").grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.name_var = tk.StringVar(self.edit_window, value=old_name)
        tk.Entry(self.edit_window, textvariable=self.name_var).grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        tk.Label(self.edit_window, text="Адрес:", anchor="e").grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.url_var = tk.StringVar(self.edit_window, value=old_url)
        tk.Entry(self.edit_window, textvariable=self.url_var).grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        save_button_text = "Сохранить изменения" if not new else "Добавить сайт"
        tk.Button(self.edit_window, text=save_button_text, command=lambda: self.save_site(old_name)).grid(row=2, column=0, columnspan=2, pady=10)

        self.edit_window.grid_columnconfigure(1, weight=1)
        

    def save_site(self, old_name):
        new_name = self.name_var.get()
        new_url = self.url_var.get()
        
        if not new_url.startswith(("http://", "https://")):
            new_url = "https://" + new_url

        if new_name and new_url:
            if old_name:
                del self.app.sites[old_name]
            self.app.sites[new_name] = new_url
            self.app.save_settings()
            self.populate_listbox()
            self.edit_window.destroy()
            print(f"Сайт {new_name} сохранен с Адресомн {new_url}")
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите название сайта и его Адрес в сети.")

    def delete_site(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Выбор сайт", "Пожалуйста, выберите сайт для удаления.")
            return

        site_name = self.listbox.get(selected_index)
        del self.app.sites[site_name]
        self.app.save_settings()
        self.populate_listbox()
        print(f"Сайт {site_name} удален")

def open_sites_manager(parent, app):
    SitesManager(parent, app)
