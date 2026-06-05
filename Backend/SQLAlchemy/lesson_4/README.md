# Lesson 4: Advanced Queries and Aggregate Functions

## Introduction
In this lesson, I learned how to optimize data retrieval in SQLAlchemy 2.0. Instead of pulling all records into Python memory, I implemented advanced SQL techniques to sort, filter, and calculate values directly inside the PostgreSQL database. This is a crucial skill for backend developers to keep applications fast and efficient when handling large amounts of AI log data.

## Key Skills Acquired

* **Advanced Filtering & Joins**: Mastered data sorting using `order_by`, limiting query results with `limit`/`offset`, and merging different tables using `.join()` to fetch related data in a single database request.
* **Database Calculations**: Learned how to use aggregate functions (`func.count`, `func.sum`, `func.avg`) to perform mathematical analysis.
