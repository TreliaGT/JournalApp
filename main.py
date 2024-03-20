import tkinter as tk
from tkinter import ttk
from journal import Journal
from tasks import TasksTab
from tkinter import ttk  # Normal Tkinter.* widgets are not themed!
from ttkthemes import ThemedTk


def main():
    root = ThemedTk(theme="arc")
    app = Journal(root)
    tasks_tab = TasksTab(app.notebook)  # Add the tasks tab
 
    root.mainloop()

if __name__ == "__main__":
    main()