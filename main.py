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
    custom_font = ('Lato', 12)  # Change the font size as desired

    # Set the default font for the entire application
    root.option_add("*Font", custom_font)
    app = Journal(root)
    tasks_tab = TasksTab(app.notebook)  # Add the tasks tab
    
    root.mainloop()

if __name__ == "__main__":
    main()