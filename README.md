# My Full-stack Project

This repository contains both the backend (Python) and frontend (Angular) components of the project.

## Structure

- `/backend`: Contains the Python backend project
- `/frontend`: Contains the Angular frontend project
- `/PLC Project`: Contains the binary file for a PLC controller.

## Setup

### Backend (Python)

1. Navigate to the `backend` directory
2. Create a virtual environment: `python -m venv env`
3. Activate the virtual environment:
   - On Windows: `env\Scripts\activate`
   - On macOS and Linux: `source env/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the backend server: `python manage.py runserver`

### Frontend (Angular)

1. Navigate to the `frontend` directory
2. Install dependencies: `npm install`
3. Run the development server: `ng serve`

### PLC Project(Sysmac)

1. The binary can be imported using Sysmac Studio

## Development

- Backend development is done in the `backend` directory, preferably using PyCharm
- Frontend development is done in the `frontend` directory, preferably using VS Code

Always make sure you're in the correct directory when running commands or starting your development servers.