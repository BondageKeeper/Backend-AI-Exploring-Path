# 🚀 Advanced B2B AI Infrastructure Monitoring Pipeline

## 📝 Introduction
This little project training code is important. Over the last two weeks, I mastered four core pillars of modern Python backend development: **Pydantic**, **SQLAlchemy 2.0 (Async ORM)**, **PostgreSQL**, and **Alembic**. 

To prove my skills, I designed and built a highly resilient, asynchronous data pipeline . The system ingests a complex, multi-level nested JSON payload from an enterprise infrastructure node, runs it through a strict validation(Using REGEX as one of my favourite tool to check the sample) and security layer, dynamically normalizes the data, and establishes clean relational storage inside a PostgreSQL cluster with automated version control.

---

## 🛠️ Architecture & Core Components

1. 🛡️ **Validation Layer (Pydantic)**: Acts as an enterprise-grade firewall. It parses heavily nested dictionaries, validates data types, and utilizes advanced Regex to strictly filter corporate emails, network proxy addresses (`socks5`/`http`), and secure endpoints (`https`/`wss`).
2. 🗄️ **Database Layer (SQLAlchemy 2.0 Async)**: A completely asynchronous database interface managing a parallel "Star Schema" architecture across 3 distinct, interconnected tables (`Operators`, `Agents`, and `Configs`).
3. 🧬 **Migration Layer (Alembic)**: Serves as version control for the database schema, handling zero-downtime structural modifications through code blueprints.
4. 🪵 **Observability Layer (Loguru)**: Provides rich asynchronous logging, tracking every state of the pipeline and exporting structured metrics to file-streams via `logger.add()`.

---

## 💎 Key Skills Acquired

* **Deep Nested JSON Engineering**: Developed multi-tier validation schemas using `list[BaseModel]` structures capable of handling complex parent-child input objects safely.
* **Asynchronous Connection Mastery**: Resolved complex async lifecycles, race conditions, and python garbage collection faults by enforcing explicit token check-ins via `await session.close()` and graceful pool termination with `await engine.dispose()`.
* **Parallel Query Optimization**: Implemented advanced `selectinload` mechanics to load multiple independent relationships parallelly in a single database hit, completely eliminating the dangerous N+1 query problem.
* **Advanced Server-Side Aggregations**: Processed complex statistical data directly inside the PostgreSQL memory loop using `func.sum`, `func.count`, and conditional `.join().group_by()` filters.
* **Database Version Control (CI/CD Basics)**: Mastered live database schema refactoring. Learned how to manually rewrite automated Alembic version scripts using safe structural commands like `op.alter_column` with explicit `existing_type` guards to avoid live data loss.
* **Advanced Python Idioms**: Leveraged Python's built-in `zip()` function within the ORM loop to cleanly synchronize and bind decoupled parallel datasets on the fly.

---

## 🎯 Conclusion
This project marks my transition from writing isolated scripts to developing production-grade backend data pipelines. By unifying **validation**, **async database streaming**, and **safe schema migrations**, I have built a rock-solid foundation for engineering high-scale, reliable systems that interact with complex database structures.
