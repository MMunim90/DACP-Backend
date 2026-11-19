# Developer Assessment and Coding Platform (DACP) — Backend

A backend application built with **Python, FastAPI, SQLAlchemy, and Supabase PostgreSQL** for the Developer Assessment and Coding Platform (DACP).

DACP is a platform designed to help developers practice coding challenges, participate in programming contests, complete technical assessments, and track their problem-solving progress.

This repository contains the backend services, RESTful APIs, database models, and authentication system that power the DACP platform.

- Frontend: [Developer Assessment and Coding Platform]\([https://github.com/MMunim90/Developer-Assessment-and-Coding-Platform](https://github.com/MMunim90/Developer-Assessment-and-Coding-Platform))

## 🚀 Tech Stack

### Backend
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- RESTful API

### Database
- Supabase
- PostgreSQL

### Authentication & Security
- JWT Authentication
- Password Hashing
- Role-Based Access Control
- Environment Variable Configuration

### Tools
- Git & GitHub
- VS Code
- Postman
- Swagger UI

## ✨ Features

- RESTful API development using FastAPI
- User registration and authentication
- JWT-based authentication and authorization
- Role-based access control
- User profile management
- Coding challenge management
- Programming contest management
- Technical assessment management
- Code submission management
- Submission evaluation and result tracking
- Leaderboard and developer progress tracking
- PostgreSQL database integration using Supabase
- Data validation using Pydantic
- Database operations using SQLAlchemy
- CRUD operations (Create, Read, Update, Delete)
- Separation of backend services and frontend application

*Note: Keep only the features that are implemented in your current backend. Mark unfinished features as planned.*

## 🏗️ Architecture

```text
                 DACP Frontend
                  (React)
                      |
                      |
              HTTP Requests (REST API)
                      |
                      v
                FastAPI Backend
                      |
          ┌───────────┼───────────┐
          |           |           |
          v           v           v
       Routers     Services    Authentication
          |           |           |
          └───────────┼───────────┘
                      |
                      v
                SQLAlchemy ORM
                      |
                      |
                      v
              Supabase PostgreSQL
                      |
          ┌───────────┼───────────┐
          |           |           |
          v           v           v
        Users     Challenges   Submissions
                      |
               Contests & Assessments
```

## 📁 Project Structure

```text
DACP---Backend/
│
├── router/
│   ├── user.py
│   ├── admin.py
│   ├── challenge.py
│   ├── contest.py
│   └── assessment.py
│
├── .env
├── .gitignore
├── database.py
├── main.py
├── models.py
├── schemas.py
├── requirements.txt
│
└── README.md
```

*The structure above is a suggested example. Adjust the folders and filenames to match your actual backend project.*

## ⚙️ Installation and Setup

### Prerequisites

Make sure you have installed:

- Python 3.10+
- pip
- A Supabase account
- Git
- VS Code or another code editor

### 1. Clone the Repository

```bash
git clone <your-dacp-backend-repository-url>
cd DACP---Backend
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the backend root directory.

```env
DATABASE_URL=your_supabase_postgresql_connection_string
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace the placeholder values with your actual configuration.

Never expose your database credentials or secret keys publicly.

### 5. Run the Backend Server

```bash
uvicorn main:app --reload
```

The backend server will run at:

```text
http://127.0.0.1:8000
```

## 🗄️ Database Setup

DACP uses **Supabase PostgreSQL** as its database.

Follow these steps:

1. Create a project in [Supabase](https://supabase.com/).
2. Set up the required PostgreSQL database.
3. Copy your PostgreSQL connection string.
4. Add the connection string to your backend `.env` file.
5. Configure SQLAlchemy to connect to the database.
6. Ensure your database credentials remain private.

## 🔐 Environment Variables

Never commit sensitive information such as:

- Database connection strings
- JWT secret keys
- Passwords
- API keys
- Private credentials

Add the following entries to your `.gitignore` file:

```gitignore
.env
venv/
__pycache__/
*.py[cod]
.pytest_cache/
.idea/
.vscode/
```

## 📡 API Documentation

FastAPI automatically generates interactive API documentation.

After starting the backend server, access:

| Documentation | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

Use these interfaces to explore, test, and understand the available API endpoints.

## 🛠️ Development Workflow

1. Design and create database models using SQLAlchemy.
2. Define request and response schemas using Pydantic.
3. Develop API endpoints using FastAPI routers.
4. Implement authentication and authorization.
5. Connect the backend to Supabase PostgreSQL.
6. Integrate the frontend with backend REST APIs.
7. Test API endpoints using Swagger UI and Postman.
8. Test database operations and application functionality.

## 🚧 Project Status

**Currently under development.**

The backend is being developed to support the core functionalities of the Developer Assessment and Coding Platform.

## 👨‍💻 Author

**Munim**

- GitHub: [@MMunim90](https://github.com/MMunim90)
- LinkedIn: [MD. Shahan Al Munim](https://www.linkedin.com/in/m-munim)

## 📄 License

This project is licensed under the MIT License.

Add a `LICENSE` file to the repository if you intend to distribute it under the MIT License.