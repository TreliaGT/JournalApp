# Journal App

## Overview

This is a Python program that serves as a journaling application, allowing users to track their daily experiences, emotions, and tasks. The program utilizes JSON files to store journal entries and tasks.

## Features

- **Journaling**: Users can record their daily experiences, emotions, and thoughts.
- **Emotion Tracking**: Each journal entry includes an emotion tag, allowing users to track their mood over time.
- **Task Management**: Users can create, remove, and list tasks, which are stored in a JSON file.

## JSON Data Examples

### Journal Entries

```json
[
    {
        "date": "2024-03-19",
        "emotion": "Happy",
        "entry": "Today was a great day!"
    },
    {
        "date": "2024-03-18",
        "emotion": "Sad",
        "entry": "Feeling a bit down today."
    },
    {
        "date": "2024-03-20",
        "emotion": "Happy",
        "entry": "This is a test"
    }
]
```
### Tasks 
```json
[
    "test",
    "A list of tasks"
]
```

## Dependencies
- Python 3.x
- Tkinter
- MatplotLib

## Usage
- Clone the repository to your local machine.
- Install Dependencies
- Run the main.py file using Python.
- The application will open, allowing you to record journal entries and manage tasks.

## Contributors
- TreliaGT
