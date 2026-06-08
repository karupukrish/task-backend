# Project Management System

A backend API built with **FastAPI** for managing projects, developers, and tasks with role-based access control.

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL + SQLAlchemy ORM
- **Auth:** JWT (python-jose + passlib/bcrypt)
- **Validation:** Pydantic v2

## Features

- **Admin** — full CRUD for projects, developers, and tasks
- **Developer** — view and update tasks assigned to them
- **JWT authentication** with separate admin/developer roles
- **Auto-migrating schema** on startup

## Getting Started

### 1. Prerequisites

- Python 3.10+
- PostgreSQL running locally

### 2. Setup

```bash
# Clone the repo
git clone <repo-url>
cd project-management

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure

Edit `.env` in the project root:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/project_mgmt
JWT_SECRET=change-this-to-a-random-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=24
```

### 4. Run

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### 5. Seed Data (Optional)

```bash
python seed.py
```

Creates an admin user (`admin` / `admin123`) and sample projects, developers, and tasks.

## Project Structure

```
├── app/
│   ├── main.py          # FastAPI app setup & startup
│   ├── config.py        # Settings via pydantic-settings
│   ├── database.py      # SQLAlchemy engine & session
│   ├── models.py        # ORM models (Admin, Project, Developer, Task)
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── auth.py          # Password hashing & JWT utilities
│   ├── dependencies.py  # FastAPI dependency injection (auth guards)
│   └── routers/
│       ├── auth_router.py   # Register / Login endpoints
│       ├── admin.py         # Admin CRUD endpoints
│       └── developer.py     # Developer task endpoints
├── seed.py              # Database seed script
├── API.md               # Full API reference
└── requirements.txt
```

## API Overview

All endpoints are prefixed with `/api`. See [API.md](API.md) for the full reference.

| Endpoint Group | Prefix               | Auth   |
|----------------|----------------------|--------|
| Auth           | `/api/auth`          | Public |
| Admin          | `/api/admin`         | Admin  |
| Developer      | `/api/developer`     | Dev    |
| Health         | `GET /api/health`    | Public |

### Quick Examples

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# List projects (admin)
curl http://localhost:8000/api/admin/projects \
  -H "Authorization: Bearer <token>"

# List my tasks (developer)
curl http://localhost:8000/api/developer/tasks \
  -H "Authorization: Bearer <token>"
```
