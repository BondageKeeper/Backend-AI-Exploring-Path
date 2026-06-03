# Lesson 1: Introduction to Async SQLAlchemy 2.0

## Introduction
In this lesson, I started learning SQLAlchemy 2.0, which is a powerful ORM (Object-Relational Mapping) library for Python. It allows developers to work with databases using standard Python classes and objects instead of writing raw SQL queries manually. For Backend and AI development, this is very important because it helps to easily save user profiles, AI prompts, and response history directly from Python code. In this project, I configured it to work asynchronously with a PostgreSQL database.

## Key Skills Acquired

* **Database Connection**: Configured an asynchronous database engine using `create_async_engine` and set up an `async_sessionmaker` factory to safely handle database connections.
* **Declarative Models**: Created database tables using modern SQLAlchemy 2.0 style with `DeclarativeBase`, `Mapped`, and `mapped_column` to define strict field types and rules like primary keys and unique values.
* **Async Table Creation**: Learned how to bridge synchronous and asynchronous code using `conn.run_sync(Base.metadata.create_all)` to automatically build tables inside PostgreSQL.
* **Data Operations (CRU - without DELETE)**: Mastered adding data to the database using `session.add_all()` and safely reading and filtering records using `select()` and `.where()` methods.
