import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

# Предопределённые задачи с категориями
TASKS = [
    {"task": "Прочитать статью", "category": "учёба"},
    {"task": "Сделать зарядку", "category": "спорт"},
    {"task": "Написать отчёт", "category": "работа"},
    {"task": "Изучить новую тему", "category": "учёба"},
    {"task": "Пробежать 3 км", "category": "спорт"},
    {"task": "Проверить почту", "category": "работа"}
]

# Файл для сохранения истории
HISTORY_FILE = "history.json"

def load_history():
    """Загружает историю из JSON-файла, если он существует."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    """Сохраняет историю в JSON-файл."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x500")

        # Загрузка истории
        self.history = load_history()

        self.setup_ui()
        self.update_history_display()

    def setup_ui(self):
        # Фрейм для генерации задачи
        generate_frame = ttk.Frame(self.root)
        generate_frame.pack(pady=10)

        ttk.Button(generate_frame, text="Сгенерировать задачу",
                   command=self.generate_task).pack()

        # Фрейм для фильтрации
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=5)

        ttk.Label(filter_frame, text="Фильтр по категории:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="все")
        categories = ["все", "учёба", "спорт", "работа"]
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                   values=categories, state="readonly", width=15)
        filter_combo.pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Применить фильтр",
                   command=self.update_history_display).pack(side=tk.LEFT)

        # Фрейм для отображения истории
        history_frame = ttk.LabelFrame(self.root, text="История задач")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Список для отображения истории
        self.history_list = tk.Listbox(history_frame, height=15, width=70)
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL,
                               command=self.history_list.yview)
        self.history_list.configure(yscrollcommand=scrollbar.set)

        self.history_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Фрейм для добавления новых задач
        add_frame = ttk.LabelFrame(self.root, text="Добавить новую задачу")
        add_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(add_frame, text="Задача:").grid(row=0, column=0, padx=5, pady=2)
        self.task_entry = ttk.Entry(add_frame, width=40)
        self.task_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(add_frame, text="Категория:").grid(row=1, column=0, padx=5, pady=2)
        self.category_var = tk.StringVar(value="учёба")
        category_combo = ttk.Combobox(add_frame, textvariable=self.category_var,
                           values=["учёба", "спорт", "работа"], state="readonly")
        category_combo.grid(row=1, column=1, padx=5, pady=2)

        ttk.Button(add_frame, text="Добавить задачу",
               command=self.add_task).grid(row=2, column=0, columnspan=2, pady=5)

    def generate_task(self):
        """Генерирует случайную задачу и добавляет её в историю."""
        task = random.choice(TASKS)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry = {
            "task": task["task"],
            "category": task["category"],
            "timestamp": timestamp
        }
        self.history.append(history_entry)
        save_history(self.history)
        self.update_history_display()
        messagebox.showinfo("Новая задача", f"Ваша задача:\n{task['task']}\nКатегория: {task['category']}")

    def add_task(self):
        """Добавляет новую задачу в список предопределённых задач."""
        new_task = self.task_entry.get().strip()
        category = self.category_var.get()

        if not new_task:
            messagebox.showerror("Ошибка", "Задача не может быть пустой!")
            return

        TASKS.append({"task": new_task, "category": category})
        self.task_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Задача добавлена!")

    def update_history_display(self):
        """Обновляет отображение истории с учётом фильтра."""
        self.history_list.delete(0, tk.END)
        selected_category = self.filter_var.get()

        for entry in self.history:
            if selected_category == "все" or entry["category"] == selected_category:
                display_text = f"[{entry['timestamp']}] {entry['task']} ({entry['category']})"
                self.history_list.insert(tk.END, display_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
