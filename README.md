# Python Collection Tool
## Project Overview
This project is a simple collection management tool built in Python with an SQLite database.

---
## Features
- A basic collection tool built with Python and Tkinter. 
- You can group things into categories, have collections inside those categories, and add items to each one. 
- It also keeps track of sources (people who own the items). 
- Everything is saved in a SQLite database, and you can add or remove categories, collections, items, and sources.

## Setup
### Requirements
- Python 3.10+
- Pillow (pip install pillow)
### Run with VS Code
- Open the project root in VS Code
- Press F5 (launch config)
### Run from Terminal
- From the project root
  - **Windows PowerShell:** $env:PYTHONPATH="src"; python -m collectors_tool.app
  - **macOS/Linux:** PYTHONPATH=src python -m collectors_tool.app

## Notes
This was my first Python project, built as a learning exercise.
It is not polished, and the structure could be improved significantly (imports, path handling, UI design, database logic, etc.).
If I were to revisit it, I would likely rebuild it from scratch, possibly in Java or another language.
