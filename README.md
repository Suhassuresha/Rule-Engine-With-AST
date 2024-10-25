<<<<<<< HEAD
# Rule-Engine-With-AST
=======
# Simple Rule Engine Application

## Description
This project is a simple rule engine that allows users to create and evaluate rules based on user attributes such as age, department, income, and spend. The application features a web interface for creating rules, evaluating them, and viewing results.

## Features
- **Create Rule**: Input rule strings and generate an Abstract Syntax Tree (AST).
- **Evaluate Rule**: Evaluate rules against user data (age, department, income, and spend).

## Technology Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask, SQLite
- **AST Parsing**: Custom rule parsing and AST generation in Python
- **Database**: SQLite for storing rules and their ASTs

## Directory Structure
```bash
├── backend
│   ├── app.py               # Flask backend application
│   ├── ast_processor.py      # AST logic for rule creation and evaluation
│   ├── config.py             # Configuration file for the Flask app
│   └── database.py           # SQLite database initialization
├── frontend
│   ├── static
│   │   ├── styles.css        # CSS file for styling
│   │   └── scripts.js        # JavaScript for frontend logic
│   └── templates
│       └── index.html        # HTML template for the frontend
└── README.md                 # Documentation
```
Build Instructions
Prerequisites
1.Docker: Make sure you have Docker installed on your machine.
2.Docker Compose (optional): For orchestrating multiple containers.

Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/simple-rule-engine.git
cd simple-rule-engine
```
Step 2: Build and Run the Docker Containers
To build and run the application using Docker, create a Dockerfile and a docker-compose.yml file in your project root.

Dockerfile:

dockerfile
Copy code
# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY ./backend ./backend
COPY ./frontend ./frontend

# Expose the Flask port
EXPOSE 5000

# Set the command to run the Flask app
CMD ["python", "backend/app.py"]
docker-compose.yml:

```yaml

version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app/backend
      - ./frontend:/app/frontend
```

Step 3: Run Docker Compose
```bash
docker-compose up
This will build the application and start the Flask server, which can be accessed at http://127.0.0.1:5000.
```

Dependencies
Backend
Flask: Web framework for Python
SQLite: Database for storing rules and their ASTs
Other dependencies listed in requirements.txt (to be created)

Frontend
No external dependencies; standard HTML, CSS, and JavaScript are used.
Design Choices
Modular Structure: The application is divided into frontend and backend components for better maintainability.
AST Representation: Rules are parsed into an Abstract Syntax Tree (AST) for easy evaluation and manipulation.
Database Use: SQLite is used for its simplicity and ease of use during development.
Running the Application
Open your web browser and navigate to http://127.0.0.1:5000.
Use the provided web interface to create rules and evaluate them against user data.
Contributing
If you wish to contribute to this project, please fork the repository and submit a pull request with your changes.

License
This project is licensed under the MIT License - see the LICENSE file for details.

```markdown


### Customizing the README
- Replace `your-username` in the clone command with your actual GitHub username.
- Add your `requirements.txt` file with necessary dependencies for the backend.
- Adjust any sections as needed to better fit your project specifics. 

Let me know if you need further modifications!
```
>>>>>>> 3945d1c (Initial commit of the Simple Rule Engine application)
