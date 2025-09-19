# CCCS 106 Projects 
Application Development and Emerging Technologies 
Academic Year 2025-2026 
ECHO is on.

## Student Information
- **Name:** Renna Martinez Israel
- **Student ID:** 231002318
- **Program:** Computer Science
- **Section:** A

## Repository Structure 
- week1_labs/ - Environment setup and Python basics 
- week2_labs/ - Git and Flet GUI development
- week3_labs/ - Flet User Login Application
- week4_labs/ - Contact Book App
- module1_final/ - Module 1 final project

### Week 1 Labs – Python Basics
- `week1_labs/hello_world.py` – Python program, prints "Hello World".
- `week1_labs/basic_calculator.py` – A simple calculator that performs basic arithmetic operations.
- `week1_labs/screenshots/` – Contains screenshots related to Week 1 outputs.

### Week 2 Labs - Git and Flet GUI Development
- `week2_labs/hello_flet.py` - First Flet GUI application
- `week2_labs/personal_info_gui.py` - Enhanced personal information manager
- `week2_labs/enhanced_calculator.py` - GUI calculator

### Week 3 Labs – Database & Flet Integration
- `week3_labs/src/main.py` – Main entry point of the Flet app.
- `week3_labs/src/db_connection.py` – Handles database connections for the project.
- `week3_labs/src/assets/` – Stores additional resources for the app.
- `week3_labs/pyproject.toml` – Project dependencies and configuration.
- `week3_labs/.gitignore` – Ignore file for Python cache and unnecessary files.

### Week 4 Labs – Contact Book App
- `week4_labs/contact_book_app/src/` – Source code of the Contact Book application (main app logic, database handling, UI).
- `week4_labs/contact_book_app/pyproject.toml` – Dependencies and project setup for the app.
- `week4_labs/contact_book_app/.gitignore` – Ignore file for DB/cache.
- `week4_labs/contact_book_app/contacts.db` – SQLite database storing contact information.
- `week4_labs/contacts.db` – Duplicate SQLite database (can be ignored if not needed).

### Module 1 Final Project
- `module1_final/` - Final integrated project (TBD)

## Technologies Used
- **Python 3.8+** - Main programming language
- **Flet 0.28.3** - GUI framework for cross-platform applications
- **Git & GitHub** - Version control and collaboration
- **VS Code** - Integrated development environment
- **SQLite3** – Lightweight database used in Week 3 & Week 4 apps

## Development Environment
- **Virtual Environment:** cccs106_env
- **Python Packages:** flet==0.28.3, sqlite3
- **Platform:** Windows 10/11

## How to Run Applications

### Prerequisites
1. Python 3.8+ installed
2. Virtual environment activated: `cccs106_env\Scripts\activate`
3. Flet installed: `pip install flet==0.28.3`
4. Git installed and configured for version control
5. SQLite (built-in with Python, used for database in Week 4)
6. Visual Studio Code
   
### Running GUI Applications
```cmd
# Navigate to project directory
cd week2_labs

# Run applications
python hello_flet.py
python personal_info_gui.py

Commit and push README.md

# Add the updated README.md file to the staging area
# This stages the modified README.md file so it will be included in the next commit
# Git tracks changes to this file and prepares it for version control
git add README.md

# Commit the staged changes with a descriptive message
# Creates a permanent snapshot of the README.md updates in the repository history
# The commit message should clearly describe what was changed for future reference
git commit -m "Update README.md with new application information"

# Push the committed changes to the remote GitHub repository
# Synchronizes your local main branch with the remote repository on GitHub
# This makes your updated README.md visible to others and backs up your changes
git push origin main
