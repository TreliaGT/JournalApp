import tkinter as tk
from tkinter import ttk
from journal import Journal
from tasks import TasksTab
from ttkthemes import ThemedStyle

def main():
    root = tk.Tk()
    style = ThemedStyle(root)
    style.theme_use("arc")# Style configuration for Button widgets
    root.configure(bg="#038387")

    app = Journal(root)
    tasks_tab = TasksTab(app.notebook)  # Add the tasks tab
    
    root.mainloop()

if __name__ == "__main__":
    main()