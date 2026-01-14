This project is a FastAPI-based URL shortener with authentication, analytics, and a clean, versioned API structure. It is designed to be simple, async-first, and production-oriented while keeping analytics accurate and extensible.

---

## High-Level Approach

- The system exposes a versioned REST API (`/api/v1`) for authentication, link management, and analytics.
- Shortened URLs are generated using hashed public IDs to avoid predictability.
- All database operations are asynchronous using SQLAlchemy + asyncpg.
- Analytics are collected at redirect time and aggregated later.
- Authentication is handled using JWT access and refresh tokens.
- Analytics are made in the background. Enhancing User Experience by increasing speed

---

## Assumptions

- Analytics accuracy is prioritized over browser caching.
- Redirects are the main trigger for analytics.
- A visit is defined as each redirect request, not a unique user.
- Users and links are exposed externally using hashed IDs, not database primary keys.

---

## Redirect Strategy and Status Codes

- HTTP 302 (Temporary Redirect) is used by default to track all visits accurately.
- HTTP 301 (Permanent Redirect) can be used for truly permanent links but may reduce analytics accuracy due to caching.

The current design favors 302 redirects.

---

## Security Design

### Password Handling
- Passwords are hashed using bcrypt with per-password salts.
- Plain-text passwords are never stored.

### JWT Authentication
- Stateless JWT-based authentication.
- Access tokens are short-lived.
- Refresh tokens are long-lived.

### Token Validation
- Expired or invalid tokens return 401 Unauthorized.

---

## Project Structure

    api/
      v1/
        routes/
    core/
      config.py
      database.py
      security.py
    models/
    schemas/
    services/
    migrations/
    main.py

The structure separates routing, business logic, data models, and configuration. API versioning allows safe iteration.

---

## Tech Stack

- FastAPI
- PostgreSQL (async via asyncpg)
- SQLAlchemy (Async)
- Pydantic
- JWT (python-jose)
- bcrypt
- Gemini API (optional)
- Uvicorn

---

## Prerequisites

- Python 3.10+
- PostgreSQL
- Git

---

## Project Setup

    git clone https://github.com/boluwatife-py/URL-Shortener.git
    cd URL-Shortener

---

## Environment Variables

Create a `.env` file:

    DATABASE_URL=postgresql+asyncpg://postgres:password@host:port/db_name
    JWT_SECRET=super-secret-key
    HOST_URL=http://localhost:8000
    GEMINI_API_KEY=your-gemini-api-key

---

## Install Dependencies

### Using uv

    pip install uv
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt

### Using pip

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

---

## Run the Application

    uvicorn main:app --reload

---

## API Docs

Visit:

    http://localhost:8000/docs

---

## Trade-offs

- 302 redirects chosen for accurate analytics.
- Hashed IDs improve security but add minor computation.
- JWT provides stateless auth but requires expiration handling.