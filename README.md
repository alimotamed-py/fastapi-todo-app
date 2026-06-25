<div align="center">
  <img src="todo app.png" alt="Todo API Logo" width="700">


A secure and modern Todo API built with FastAPI

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-red)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

## ✨ About

Todo API is a modern RESTful API built with FastAPI for managing tasks and todos. The project provides secure authentication using JWT and uses SQLAlchemy ORM for database management.

---

## 🚀 Features

* User registration and authentication
* JWT Authentication
* Create, update and delete todos
* Mark tasks as completed
* Protected endpoints
* SQLAlchemy ORM
* Automatic API documentation
* Fast and lightweight architecture
* Docker support (Coming Soon)

---

## 🛠 Tech Stack

* Python
* FastAPI
* SQLAlchemy
* JWT Authentication
* Pydantic
* Uvicorn
* Docker (Planned)

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/alimotamed-py/todo-api.git
cd todo-api
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

```bash
# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

---

## 🔐 Authentication

Authentication is implemented using JSON Web Tokens (JWT).

Protected routes require a valid access token.

---

## 📚 API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## 👨‍💻 Author

Ali Motamed

GitHub: https://github.com/alimotamed-py

---

## 📄 License

This project is licensed under the MIT License.
