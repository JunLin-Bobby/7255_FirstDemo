# 7255_FirstDemo

## Project Overview
This project is built using **FastAPI** (Python framework) and **Uvicorn** as the ASGI server. It provides RESTful APIs for managing plans and integrates with MongoDB for database operations.

---

## Prerequisites
Before running the project, ensure you have the following installed:

- Python 3.10 or higher
- MongoDB (running locally or accessible remotely)
- Git (for cloning the repository)

---

## How to Build

1. **Clone the Repository**
   ```bash
   git clone git@github.com:JunLin-Bobby/7255_FirstDemo.git
   cd 7255_FirstDemo
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install fastapi uvicorn motor pydantic
   ```

---

## How to Run

1. **Start MongoDB**
   Ensure MongoDB is running locally or update the connection string in `backend/db/connection.py` to point to your MongoDB instance.

2. **Run the Application**
   ```bash
   uvicorn backend.main:app --reload
   ```

3. **Access the API**
   Open your browser and navigate to:
   - API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Framework and Library Versions
- **FastAPI**: 0.100.0+
- **Uvicorn**: 0.22.0+
- **Motor**: 3.1.0+
- **Pydantic**: 2.0.0+

---

## Notes
- Ensure the `MONGO_URI` in `backend/db/connection.py` is correctly configured for your MongoDB instance.
- Use `pip freeze > requirements.txt` to update dependencies if new packages are added.

---

## Troubleshooting
- If you encounter issues with MongoDB, ensure it is running and accessible.
- For Python-related issues, ensure you are using the correct virtual environment.

---

Enjoy using the project!