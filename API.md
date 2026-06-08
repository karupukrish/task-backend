# Project Management System — API Documentation

**Base URL:** `http://localhost:8000`

**Auth:** All protected endpoints require an `Authorization: Bearer <token>` header.

---

## 1. Authentication

### Register Admin (first setup)
```
POST http://localhost:8000/api/auth/register-admin
```
Body:
```json
{ "username": "admin", "password": "admin123" }
```
Response: `{ "access_token": "...", "token_type": "bearer", "role": "admin" }`

### Login
```
POST /api/auth/login
```
Body:
```json
{ "username": "admin", "password": "admin123" }
```
Admin logs in with `username`, Developer logs in with `email` as the `username` field.
Response: `{ "access_token": "...", "token_type": "bearer", "role": "admin|developer" }`

---

## 2. Admin Endpoints (require admin JWT)

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/projects` | List all projects |
| POST | `/api/admin/projects` | Create project |
| GET | `/api/admin/projects/{id}` | Get project by ID |
| PUT | `/api/admin/projects/{id}` | Update project |
| DELETE | `/api/admin/projects/{id}` | Delete project |

**POST /api/admin/projects**
```json
{ "name": "E-Commerce App", "description": "...", "status": "Planning" }
```
Status options: `Planning`, `In Progress`, `Completed`, `On Hold`

### Developers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/developers` | List all developers |
| POST | `/api/admin/developers` | Create developer |
| GET | `/api/admin/developers/{id}` | Get developer by ID |
| PUT | `/api/admin/developers/{id}` | Update developer |
| DELETE | `/api/admin/developers/{id}` | Delete developer |

**POST /api/admin/developers**
```json
{ "name": "Alice", "email": "alice@example.com", "password": "pass123" }
```

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/tasks` | List all tasks (optional: `?project_id=&developer_id=`) |
| POST | `/api/admin/tasks` | Create task |
| GET | `/api/admin/tasks/{id}` | Get task by ID |
| PUT | `/api/admin/tasks/{id}` | Update task |
| DELETE | `/api/admin/tasks/{id}` | Delete task |

**POST /api/admin/tasks**
```json
{
  "title": "Build login page",
  "description": "Create the login UI and validation",
  "status": "Pending",
  "project_id": "<uuid>",
  "developer_id": "<uuid>"
}
```
Status options: `Pending`, `In Progress`, `Completed`

---

## 3. Developer Endpoints (require developer JWT)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/developer/tasks` | List my tasks (optional: `?status_filter=In Progress`) |
| GET | `/api/developer/tasks/{id}` | Get task detail (only if assigned to you) |
| PUT | `/api/developer/tasks/{id}/status` | Update task status |

**PUT /api/developer/tasks/{id}/status**
```json
{ "status": "In Progress" }
```

---

## Health Check
```
GET /api/health
```
Response: `{ "status": "ok", "version": "1.0.0" }`
