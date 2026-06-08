import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

try:
    from .models import TaskStatus, ProjectStatus
except ImportError:
    from models import TaskStatus, ProjectStatus


# --- Auth ---
class AdminRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6, max_length=72)


class LoginRequest(BaseModel):
    username: str
    password: str = Field(..., min_length=6, max_length=72)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


# --- Project ---
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    status: ProjectStatus = ProjectStatus.PLANNING


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None


class ProjectResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# --- Developer ---
class DeveloperCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


class DeveloperUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=72)


class DeveloperResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Task ---
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    project_id: uuid.UUID
    developer_id: uuid.UUID


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    project_id: Optional[uuid.UUID] = None
    developer_id: Optional[uuid.UUID] = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    status: TaskStatus
    project_id: uuid.UUID
    developer_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskDetailResponse(TaskResponse):
    project: Optional[ProjectResponse] = None
    developer: Optional[DeveloperResponse] = None
