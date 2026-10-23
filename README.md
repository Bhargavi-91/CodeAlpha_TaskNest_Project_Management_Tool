# TaskNest — CodeAlpha Project Management Tool

A beginner-friendly full-stack project management app using Python, Django, SQLite, HTML, and CSS.

## Features
- User registration and login
- Create personal projects
- Add, edit, and delete tasks
- Task priority, status, and due date
- Dashboard summary and status filtering
- Django admin
- SQLite database
- Responsive layout

## Windows setup
Open this folder in VS Code, then choose Terminal → New Terminal.

Create and activate a virtual environment:
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, switch the VS Code terminal profile to Command Prompt and run:
```bat
.venv\Scripts\activate.bat
```

Install dependencies:
```bash
python -m pip install -r requirements.txt
```

Create the database:
```bash
python manage.py makemigrations tasks
python manage.py migrate
```

Run the site:
```bash
python manage.py runserver
```
Open http://127.0.0.1:8000/ and create an account.

## Optional admin account
```bash
python manage.py createsuperuser
```
Then visit http://127.0.0.1:8000/admin/.

## Before submitting
- Register a user and log in.
- Create at least two projects.
- Add tasks with different priorities, statuses, and due dates.
- Test edit/delete and status filtering.
- Take screenshots and record a short demo.
- Upload code to GitHub and follow the exact CodeAlpha submission instructions.
- Do not upload passwords, private user data, or production secrets.
