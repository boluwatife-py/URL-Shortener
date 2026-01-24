# URL Shortener

A high-performance, analytics-focused URL shortening service built with FastAPI, designed for accurate click tracking and user insights. This is a side project exploring modern web development practices.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Key Features](#key-features)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Security Design](#security-design)
- [Analytics Strategy](#analytics-strategy)
- [Setup & Installation](#setup--installation)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Good Parts & Bad Parts](#good-parts--bad-parts)
- [Contributing](#contributing)

## Overview

This is a modern URL shortening platform built as a side project to explore analytics accuracy and user experience. The system provides secure link management with comprehensive click tracking, AI-powered insights, and a clean REST API.

### Core Principles

- **Analytics Accuracy**: Uses HTTP 302 redirects to ensure every click is tracked
- **Security First**: JWT-based authentication with bcrypt password hashing
- **Async by Design**: Built with async SQLAlchemy for high performance
- **Clean Architecture**: Separated concerns with services, schemas, and routes

## Architecture

The application follows a modular architecture with clear separation of concerns:

```
api/v1/
├── routes/          # API endpoint definitions
│   ├── auth.py      # Authentication endpoints
│   ├── links.py     # Link CRUD operations
│   ├── analytics.py # Analytics data retrieval
│   └── ai_insight.py # AI-powered insights
└── __init__.py

core/
├── config.py        # Application configuration
├── database.py      # Database connection and session management
├── security.py      # JWT token handling and password security
└── utils/
    ├── hashid.py    # Public ID encoding/decoding
    └── validators/  # Input validation

models/              # SQLAlchemy ORM models
├── base.py
├── user.py
├── link.py
└── link_event.py

schemas/             # Pydantic data models
├── auth.py
├── link.py
├── analytics.py
└── ai_insight.py

services/            # Business logic layer
├── auth.py          # User authentication
├── link.py          # Link management
├── link_redirect.py # URL redirection with analytics
├── analytics.py     # Data aggregation and reporting
└── ai_insight.py    # Gemini AI integration
```

## Tech Stack

### Backend

- **FastAPI**: High-performance async web framework
- **SQLAlchemy 2.0**: Async ORM for PostgreSQL
- **asyncpg**: High-performance PostgreSQL driver
- **Pydantic**: Data validation and serialization
- **JWT**: Stateless authentication with jose
- **bcrypt**: Secure password hashing
- **Google Gemini AI**: AI-powered analytics insights

### Infrastructure

- **PostgreSQL**: Primary database
- **Redis**: Caching (configured but not fully utilized)
- **Alembic**: Database migrations
- **Uvicorn**: ASGI server

### Development Tools

- **Python 3.13+**: Core runtime
- **uv**: Fast Python package manager
- **Hashids**: Obfuscated public IDs

## Key Features

### 🔗 Link Management

- Create, read, update, delete shortened links
- Custom link titles
- Public ID obfuscation using Hashids
- URL validation and normalization

### 📊 Analytics & Insights

- Real-time click tracking
- Daily click aggregation
- Source-based click analysis (UTM parameters)
- IP address and user agent logging
- AI-powered insights using Google Gemini

### 🔐 Security

- JWT-based authentication (access + refresh tokens)
- Secure password hashing with bcrypt
- Username validation and sanitization
- CORS configuration for frontend integration
- Hashid-based public ID obfuscation

### 🚀 Performance

- Async database operations
- Background task processing for analytics
- Connection pooling with asyncpg
- Efficient query optimization

## API Documentation

### Authentication Endpoints

#### POST `/api/v1/auth/register`

Register a new user account.

**Request Body:**

```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Response:**

```json
{
  "access_token": "eyJ...",
  "username": "johndoe",
  "id": "abc123def",
  "token_type": "bearer"
}
```

#### POST `/api/v1/auth/login`

Authenticate and receive JWT tokens.

**Request Body:**

```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

### Link Management Endpoints

#### POST `/api/v1/links/`

Create a new shortened link.

**Request Body:**

```json
{
  "title": "My Awesome Link",
  "url": "https://example.com"
}
```

**Response:**

```json
{
  "id": "abc123def",
  "title": "My Awesome Link",
  "url": "https://example.com",
  "shortened_url": "http://localhost:8000/abc123def",
  "created_at": "2026-01-24T10:00:00Z"
}
```

#### GET `/api/v1/links/`

List all user links.

#### GET `/api/v1/links/{link_id}`

Get specific link details.

#### PUT `/api/v1/links/{link_id}`

Update link title or URL.

#### DELETE `/api/v1/links/{link_id}`

Delete a link.

### Analytics Endpoints

#### GET `/api/v1/analytics/link/{public_id}`

Get analytics for a specific link.

**Response:**

```json
{
  "url": "https://example.com",
  "shortended_url": "http://localhost:8000/abc123def",
  "total_clicks": 42,
  "clicks_per_day": [
    { "day": "2026-01-20", "clicks": 5 },
    { "day": "2026-01-21", "clicks": 12 }
  ],
  "clicks_by_source": [
    { "source": "twitter", "clicks": 15 },
    { "source": "facebook", "clicks": 8 }
  ]
}
```

#### GET `/api/v1/analytics/all`

Get analytics for all user links.

### AI Insights Endpoint

#### POST `/api/v1/ai/insights`

Generate AI-powered insights from analytics data.

**Request Body:**

```json
{
  "prompt": "What are the best performing links and why?"
}
```

### URL Redirection

#### GET `/{public_id}`

Redirect to the original URL while tracking analytics.

- **Status Code**: 302 (Temporary Redirect)
- **Analytics**: Background task records click data
- **Tracking**: IP address, user agent, UTM source parameters

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Links Table

```sql
CREATE TABLE links (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR NOT NULL,
    url VARCHAR(2048) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Link Events Table

```sql
CREATE TABLE link_events (
    id SERIAL PRIMARY KEY,
    link_id INTEGER REFERENCES links(id) ON DELETE CASCADE,
    clicked_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source VARCHAR(512),
    ip_address VARCHAR(45),
    user_agent TEXT
);
```

## Security Design

### Password Security

- **Hashing**: bcrypt with per-password salts
- **Validation**: Minimum 8 characters, complexity requirements
- **Common Password Check**: Against known weak passwords list

### Authentication

- **JWT Tokens**: Short-lived access tokens (15 minutes) + long-lived refresh tokens (30 days)
- **Token Storage**: HTTP-only cookies for refresh tokens
- **Public IDs**: Hashid-encoded database IDs to prevent enumeration

### Input Validation

- **Username**: 3-20 characters, alphanumeric + underscores
- **URLs**: Pydantic HttpUrl validation
- **Passwords**: Complexity rules enforced

### HTTPS Considerations

- CORS configured for frontend integration
- Secure cookie settings (configurable for development/production)

## Analytics Strategy

### 302 vs 301 Redirects

The system uses **HTTP 302 (Temporary Redirect)** instead of **HTTP 301 (Permanent Redirect)** for critical analytics accuracy:

#### Why 302?

- **Browser Behavior**: Browsers don't cache 302 redirects, ensuring every click goes through the server
- **Analytics Accuracy**: Each redirect triggers analytics recording
- **Real-time Tracking**: No risk of cached redirects bypassing tracking

#### Trade-offs

- **Performance**: Slightly slower due to no caching
- **SEO Impact**: Search engines may not pass link equity as effectively
- **Use Case**: Prioritizes analytics over SEO for link sharing platforms

#### When to Use 301

- Static, permanent links where analytics accuracy is less critical
- High-traffic scenarios where caching provides performance benefits
- SEO-focused campaigns

### Analytics Data Collection

**Synchronous Redirect + Asynchronous Analytics:**

```python
@app.get("/{public_id}")
async def redirect_link(
    public_id: str,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    # Fast redirect
    service = LinkRedirectService(db)
    link = await service.get_link_by_public_id(public_id)

    # Background analytics recording
    background_tasks.add_task(
        record_click_background,
        public_id=public_id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        source=request.query_params.get("utm_source"),
        db=db
    )

    return RedirectResponse(url=link.url, status_code=302)
```

### Data Points Tracked

- **Timestamp**: Click time with timezone
- **IP Address**: Client IP (IPv4/IPv6 support)
- **User Agent**: Browser/client information
- **UTM Source**: Campaign tracking parameters
- **Geographic Data**: Inferred from IP (future enhancement)

## Setup & Installation

### Prerequisites

- Python 3.13+
- PostgreSQL 12+
- Git

### Installation

1. **Clone the repository:**

```bash
git clone <repository-url>
```

2. **Create virtual environment:**

```bash
# Using uv (recommended)
pip install uv
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Or using pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. **Environment Configuration:**
   Create a `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/url_shortener
JWT_SECRET=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
HOST_URL=http://localhost:8000
HASHID_SALT=your-unique-hashid-salt
REDIRECT_STATUS_CODE=302
GEMINI_API_KEY=your-gemini-api-key
```

4. **Database Setup:**

```bash
# Run migrations
alembic upgrade head
```

5. **Start the server:**

```bash
uvicorn main:app --reload
```

### API Documentation Access

Visit `http://localhost:8000/docs` for interactive API documentation.

## Configuration

### Environment Variables

| Variable                      | Description                  | Default                 | Required |
| ----------------------------- | ---------------------------- | ----------------------- | -------- |
| `DATABASE_URL`                | PostgreSQL connection string | -                       | Yes      |
| `JWT_SECRET`                  | Secret key for JWT signing   | -                       | Yes      |
| `JWT_ALGORITHM`               | JWT algorithm                | `HS256`                 | No       |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime        | `15`                    | No       |
| `REFRESH_TOKEN_EXPIRE_DAYS`   | Refresh token lifetime       | `30`                    | No       |
| `HOST_URL`                    | Base URL for shortened links | `http://localhost:8000` | No       |
| `HASHID_SALT`                 | Salt for ID obfuscation      | -                       | Yes      |
| `REDIRECT_STATUS_CODE`        | HTTP redirect status         | `302`                   | No       |
| `GEMINI_API_KEY`              | Google Gemini API key        | -                       | No\*     |

\*Required for AI insights feature

## Deployment

### Production Considerations

1. **Database**: Use connection pooling and read replicas for high traffic
2. **Caching**: Implement Redis for analytics aggregation
3. **Security**: Use HTTPS, secure JWT secrets, environment variable management
4. **Monitoring**: Add logging, metrics, and health checks
5. **Scaling**: Consider async workers for background analytics processing

### Docker Deployment (Future Enhancement)

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Good Parts & Bad Parts

### Strengths

#### ✅ Excellent Analytics Design

- **302 redirects** ensure 100% click tracking accuracy
- Background task processing prevents redirect delays
- Comprehensive data collection (IP, UA, UTM, timestamps)
- AI-powered insights add significant value

#### ✅ Clean Architecture

- Clear separation of concerns (routes → services → models)
- Async-first design for scalability
- Pydantic schemas ensure data validation
- Modular service layer for business logic

#### ✅ Security Best Practices

- bcrypt password hashing with salts
- JWT with short-lived access tokens
- Input validation and sanitization
- Hashid obfuscation prevents ID enumeration

#### ✅ Developer Experience

- FastAPI auto-generated documentation
- Type hints throughout codebase
- Alembic migrations for schema evolution
- Comprehensive error handling

#### ✅ Performance Optimizations

- Async database operations
- Connection pooling with asyncpg
- Efficient query patterns
- Background task processing

### Areas for Improvement

#### ⚠️ Missing Features

- **Rate Limiting**: No protection against abuse
- **Link Expiration**: No TTL for shortened links
- **Custom Domains**: Only supports single domain
- **Bulk Operations**: No batch link creation/deletion
- **Export Functionality**: No analytics data export

#### ⚠️ Scalability Concerns

- **Analytics Storage**: Link events table grows rapidly
- **No Caching**: Redis configured but not utilized
- **Database Load**: Analytics queries could be expensive at scale
- **Background Tasks**: No queue system for high-volume analytics

#### ⚠️ Code Quality Issues

- **Error Handling**: Inconsistent error responses
- **Validation**: Some endpoints lack proper validation
- **Logging**: Minimal logging for debugging/monitoring
- **Testing**: No test suite visible
- **Documentation**: API docs could be more detailed

#### ⚠️ Security Gaps

- **HTTPS**: No forced HTTPS configuration
- **CORS**: Overly permissive CORS settings
- **Token Refresh**: No automatic token refresh mechanism
- **Audit Logging**: No security event logging

#### ⚠️ Operational Concerns

- **Monitoring**: No health checks or metrics
- **Backup**: No database backup strategy mentioned
- **Migration**: No zero-downtime deployment strategy
- **Configuration**: Environment validation could be improved

### Recommendations

#### High Priority

1. **Add Rate Limiting** (nginx, redis, or middleware)
2. **Implement Analytics Aggregation** (daily summaries, data archival)
3. **Add Comprehensive Testing** (unit, integration, e2e)
4. **Improve Error Handling** (consistent error schemas)
5. **Add Monitoring/Logging** (structured logging, metrics)

#### Medium Priority

1. **Custom Link Expiration** (TTL, scheduled cleanup)
2. **Bulk Operations** (CSV import/export)
3. **Advanced Analytics** (geographic data, device detection)
4. **API Versioning Strategy** (proper versioning for breaking changes)
5. **Caching Layer** (Redis for frequently accessed data)

#### Low Priority

1. **Multi-domain Support** (custom domains per user)
2. **Link Tags/Categories** (organization features)
3. **Team Collaboration** (shared workspaces)
4. **Advanced UTM Builder** (campaign management)
5. **Integration APIs** (webhooks, Zapier)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Guidelines

- Follow async/await patterns consistently
- Use type hints for all function parameters
- Write descriptive commit messages
- Update documentation for API changes
- Test analytics accuracy for redirect changes

---

**Built with ❤️ using FastAPI, SQLAlchemy, and Google Gemini**
