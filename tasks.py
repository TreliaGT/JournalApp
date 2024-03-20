import tkinter as tk
from tkinter import ttk
import json

class TasksTab:
    def __init__(self, notebook):
        self.notebook = notebook
        self.tasks = []
        self.load_tasks_from_json()
        self.create_tab()

    def create_tab(self):
        tasks_frame = tk.Frame(self.notebook)
        self.notebook.add(tasks_frame, text="Tasks")

        self.task_entry = tk.Entry(tasks_frame)
        self.task_entry.pack(fill="x", padx=5, pady=5)

        button_frame = tk.Frame(tasks_frame)  # Frame to contain the buttons
        button_frame.pack(fill="x", padx=5, pady=5)

        add_button = tk.Button(button_frame, text="Add Task", command=self.add_task)
        add_button.pack(side="left")

        remove_button = tk.Button(button_frame, text="Remove Task", command=self.remove_task)
        remove_button.pack(side="left", padx=5)

        self.task_listbox = tk.Listbox(tasks_frame)
        self.task_listbox.pack(fill="both", expand=True)

        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    def load_tasks_from_json(self):
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            pass  # If the file doesn't exist, just continue with an empty list

    def save_tasks_to_json(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.save_tasks_to_json()  # Save tasks to JSON file
        else:
            messagebox.showwarning("Empty Task", "Please enter a task.")

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            task = self.task_listbox.get(task_index)
            self.task_listbox.delete(task_index)
            self.tasks.remove(task)
            self.save_tasks_to_json()  # Save tasks to JSON file

