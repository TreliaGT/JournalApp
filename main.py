import tkinter as tk
from tkinter import ttk
from journal import Journal
from tasks import TasksTab


def main():
    root = tk.Tk()
    app = Journal(root)
    tasks_tab = TasksTab(app.notebook)  # Add the tasks tab
    root.mainloop()

if __name__ == "__main__":
    main()