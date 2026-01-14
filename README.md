# FastAPI URL Shortener

This is a FastAPI-based URL shortener service with analytics support, async PostgreSQL, and automatic API documentation via Swagger UI.

---

## Tech Stack

- FastAPI
- PostgreSQL (async via asyncpg)
- SQLAlchemy (Async)
- Pydantic
- JWT Authentication
- Gemini API (optional, for AI-generated analytics insights)
- Uvicorn

---

## Prerequisites

Make sure you have the following installed:

- Python 3.10 or higher
- PostgreSQL
- Git

---

## Project Setup

Clone the repository:

    git clone https://github.com/boluwatife-py/URL-Shortener.git
    cd URL-Shortener

---

## Environment Variables

Create a `.env` file in the root of the project and add the following values:

    DATABASE_URL=postgresql+asyncpg://postgres:password@host:port/db_name
    JWT_SECRET=super-secret-key
    HOST_URL=http://localhost:8000
    GEMINI_API_KEY=your-gemini-api-key

Notes:
- Ensure the database `url_shortener` already exists.
- Update database credentials if necessary.
- `GEMINI_API_KEY` is optional unless AI analytics features are enabled.

---

## Dependency Installation

### Option 1: Using uv (recommended)

Install uv if you do not already have it:

    pip install uv

Create and activate a virtual environment:

    uv venv
    source .venv/bin/activate

Install dependencies:

    uv pip install -r requirements.txt

---

### Option 2: Using pip

Create and activate a virtual environment:

    python -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

---

## Running the Application

Start the FastAPI server using Uvicorn:

    uvicorn main:app --reload

---

## API Documentation

Once the server is running, open your browser and visit:

    http://localhost:8000/docs

This will open the Swagger UI where you can explore and test all available APIs.

---

## Redirect Configuration (Important)

When redirecting shortened URLs:

- Use HTTP 301 (Permanent Redirect) for links that are permanently redirected.
- Use HTTP 302 (Temporary Redirect) when you want to collect accurate analytics such as click counts, referrers, or timestamps.

Using 302 ensures that browsers and proxies do not aggressively cache redirects, which is important for analytics accuracy.