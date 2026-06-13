# Lesson 3: Advanced FastAPI & Async SQLAlchemy Relationships

This section covers building a real-world backend database system for a Car Service using relational tables, Pydantic nesting, and automatic documentation.

## What I Learned & Implemented

* **Database Relationships:** Created a One-to-Many relational structure in SQLAlchemy using foreign keys and `relationship()` to tie repair orders to multiple spare parts.
* **Nested Validation:** Used Pydantic schemas to validate complex nested JSON payloads containing lists of objects dynamically.
* **Async Session Flow:** Mastered `AsyncSession` for handling non-blocking database transactions using `commit()`, `refresh()`, and custom dependency injection.
* **Custom Field Validators:** Implemented advanced data filtering using Python's `re` (Regular Expressions) to block illegal entries (like "nitro") and check email shapes.
* **Debugging with 500 Errors:** Learned how asynchronous database engines block implicit lazy-loading operations under the hood, throwing `Internal Server Error`.

## How to Run & Open Swagger UI

FastAPI automatically generates an interactive Swagger UI panel, which allows testing endpoints and checking payload delivery directly from the browser without a frontend.

1. Open your terminal and run the server using this exact command:
   ```bash
   python -m uvicorn exp_FastAPI_tasks:app --reload
   ```

2. Once the terminal displays `Application startup complete`, open your browser and navigate to:
   ```text
   http://127.0.0
   ```
