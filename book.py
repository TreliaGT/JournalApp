import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import defaultdict

class JournalApp:
    year_emotion = {}
    month_emotion = {}
    
    #Init the program
    def __init__(self, master):
        self.master = master
        self.master.title("Journal App")
        self.master.geometry("600x600")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.create_tab()
        self.calendar_tab()
        self.graph_tab()

    # Create entry Tab
    def create_tab(self):
        create_frame = tk.Frame(self.notebook)
        self.notebook.add(create_frame, text="Create Entry")

        self.text_entry = tk.Text(create_frame)
        self.text_entry.pack(fill=tk.BOTH, expand=True)

        emotions_frame = tk.Frame(create_frame)
        emotions_frame.pack()

        emotions = ["Happy", "Sad", "Angry", "Excited", "Calm"]
        self.emotion_var = tk.StringVar(create_frame)
        self.emotion_var.set(emotions[0])
        emotion_label = tk.Label(emotions_frame, text="Select Emotion:")
        emotion_label.pack(side=tk.LEFT)
        emotion_dropdown = tk.OptionMenu(emotions_frame, self.emotion_var, *emotions)
        emotion_dropdown.pack(side=tk.LEFT)

        create_button = tk.Button(create_frame, text="Create Entry", command=self.save_entry)
        create_button.pack()

    # Saves the entry to json file
    def save_entry(self):
        entry_text = self.text_entry.get("1.0", "end-1c")
        selected_emotion = self.emotion_var.get()
        entry = {
            "date": str(datetime.now().date()),  # Use the current date
            "emotion": selected_emotion,
            "entry": entry_text
        }

        # Load existing entries
        try:
            with open("journal_entries.json", "r") as file:
                entries = json.load(file)
        except FileNotFoundError:
            entries = []

        # Check if an entry already exists for the current date
        for existing_entry in entries:
            if existing_entry["date"] == entry["date"]:
                messagebox.showwarning("Duplicate Entry", "An entry already exists for today.")
                return  # Exit the method if an entry already exists

        # If no entry exists for the current date, append the new entry
        entries.append(entry)

        # Save the updated entries to the JSON file
        with open("journal_entries.json", "w") as file:
            json.dump(entries, file, indent=4)  # Pretty-print for better readability

        messagebox.showinfo("Entry Saved", f"Entry saved with emotion: {selected_emotion}")

    #Create the calendar Tab
    def calendar_tab(self):
        calendar_frame = tk.Frame(self.notebook)
        self.notebook.add(calendar_frame, text="Calendar")

        self.cal = Calendar(calendar_frame, selectmode="day")
        self.cal.pack(fill="both", expand=True)

        # Display emotions and their corresponding colors
        emotions = [
            ("Happy", "Green"),
            ("Sad", "Blue"),
            ("Angry", "Red"),
            ("Excited", "Orange"),
            ("Calm", "Yellow")
        ]

        for emotion, color in emotions:
            emotion_label = tk.Label(calendar_frame, text=f"{emotion}: {color}", fg="black")
            emotion_label.pack(anchor="w", padx=10, pady=5)

        self.load_entries_from_json()

        self.cal.bind("<<CalendarSelected>>", self.on_calendar_click)

    #Function to load Json file Data
    def load_entries_from_json(self):
        try:
            with open("journal_entries.json", "r") as file:
                entries = json.load(file)
                #print(entries)  # Add this line to print loaded entries
                for entry in entries:
                    date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
                    #For the Graph Tab
                    if self.is_current_month(entry["date"]):
                        emotion = entry["emotion"]
                        self.month_emotion[emotion] = self.month_emotion.get(emotion, 0) + 1
                    if self.is_current_year(entry["date"]):
                        emotion = entry["emotion"]
                        self.year_emotion[emotion] = self.year_emotion.get(emotion, 0) + 1
                    #For the calendar Tab
                    self.cal.calevent_create(date, entry["entry"], tags=(entry["emotion"],))
                    self.cal.tag_config(entry["emotion"], background=self.get_emotion_color(entry["emotion"]))
        except FileNotFoundError:
            messagebox.showwarning("File Not Found", "No journal entries found.")

    # Action to click on calendar to show entry         
    def on_calendar_click(self, event=None):
        date = self.cal.selection_get()
        event_ids = self.cal.get_calevents(date)
        if event_ids:
            event_id = event_ids[0]  # Assuming there's only one event per date
            emotion = self.cal.calevent_cget(event_id, "tags")[0]
            entry_text = self.cal.calevent_cget(event_id, "text")
            messagebox.showinfo("Journal Entry", f"Date: {date}\nEmotion: {emotion}\nEntry: {entry_text}")

    #Create Graph tab to display emotions
    def graph_tab(self):
        graph_frame = tk.Frame(self.notebook)
        self.notebook.add(graph_frame, text="Graph")

        # Create a dropdown
        options = ["Month", "Year"]  # Add your options here
        self.selected_option = tk.StringVar()
        dropdown = ttk.Combobox(graph_frame, textvariable=self.selected_option, values=options)
        dropdown.pack()

        # Create the graph canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        dropdown.bind("<<ComboboxSelected>>", self.update_graph)

    #Update the graph depending on month or year selection
    def update_graph(self, event):
        selected_option = self.selected_option.get()
        # Example if statement based on selected option
        if selected_option == "Month":
           self.plot_emotions(self.month_emotion)
  
        elif selected_option == "Year":
            self.plot_emotions(self.year_emotion)

        # Redraw canvas after updating
        self.canvas.draw()

    #added the data into the graph tab
    def plot_emotions(self, emotions):
        self.ax.clear()
        if not emotions:
            return  # No emotions for the selected date

        emotion_names = list(emotions.keys())
        emotion_counts = list(emotions.values())

        self.ax.bar(emotion_names, emotion_counts)
        self.ax.set_xlabel('Emotions')
        self.ax.set_ylabel('Counts')
        self.ax.set_title('Emotions for Selected Date')
        self.canvas.draw()

    #Calendar tab colours 
    def get_emotion_color(self, emotion):
        # Function to map emotions to colors
        color_map = {
            "Happy": "green",
            "Sad": "blue",
            "Angry": "red",
            "Excited": "orange",
            "Calm": "yellow"
        }
        return color_map.get(emotion, "white")

    #checks if the current month    
    def is_current_month(self, date_str):
        # Convert string to datetime object
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        # Get current date
        current_date = datetime.now().date()
        # Check if the year and month of the date match the current year and month
        return date_obj.year == current_date.year and date_obj.month == current_date.month

    #checks if the current year
    def is_current_year(self, date_str):
        # Convert string to datetime object
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        # Get current date
        current_date = datetime.now().date()
        # Check if the year of the date matches the current year
        return date_obj.year == current_date.year


# Main Function
def main():
    root = tk.Tk()
    app = JournalApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
