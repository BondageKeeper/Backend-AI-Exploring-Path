# Lesson 1: Full-Stack Integration, Database Alignment & CORS Bypass

## Key Skills Acquired

* **CORS Security Bypass:** Solved the strict browser security block (`Origin: allow_origin_regex = r".*"`) for local files by correctly configuring `allow_credentials=True` and wildcard settings in FastAPI.
* **SQLAlchemy Async Optimization:** Fixed critical `greenlet` and lazy-loading errors by replacing direct relationship appends with explicit, high-performance Foreign Key bindings (`user_id`).
* **Relational Data Flow:** Implemented an end-to-end data pipeline where a single frontend JSON payload successfully seeds three relational PostgreSQL tables concurrently (`users_info_registration`, `booking_info`, and `time_tables`)
