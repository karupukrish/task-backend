from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

try:
    from ..database import get_db
    from ..models import Project, Developer, Task
    from ..schemas import (
        ProjectCreate, ProjectUpdate, ProjectResponse,
        DeveloperCreate, DeveloperUpdate, DeveloperResponse,
        TaskCreate, TaskUpdate, TaskResponse, TaskDetailResponse,
    )
    from ..auth import hash_password
    from ..dependencies import get_current_admin
except ImportError:
    from database import get_db
    from models import Project, Developer, Task
    from schemas import (
        ProjectCreate, ProjectUpdate, ProjectResponse,
        DeveloperCreate, DeveloperUpdate, DeveloperResponse,
        TaskCreate, TaskUpdate, TaskResponse, TaskDetailResponse,
    )
    from auth import hash_password
    from dependencies import get_current_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"], dependencies=[Depends(get_current_admin)])


# ──────────────────────── Projects ────────────────────────

@router.get("/projects", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.created_at.desc()).all()


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(body: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(name=body.name, description=body.description, status=body.status)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: str, body: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if body.name is not None:
        project.name = body.name
    if body.description is not None:
        project.description = body.description
    if body.status is not None:
        project.status = body.status
    db.commit()
    db.refresh(project)
    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    db.delete(project)
    db.commit()


# ──────────────────────── Developers ────────────────────────

@router.get("/developers", response_model=List[DeveloperResponse])
def list_developers(db: Session = Depends(get_db)):
    return db.query(Developer).order_by(Developer.created_at.desc()).all()


@router.post("/developers", response_model=DeveloperResponse, status_code=status.HTTP_201_CREATED)
def create_developer(body: DeveloperCreate, db: Session = Depends(get_db)):
    existing = db.query(Developer).filter(Developer.email == body.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    dev = Developer(name=body.name, email=body.email, password_hash=hash_password(body.password))
    db.add(dev)
    db.commit()
    db.refresh(dev)
    return dev


@router.get("/developers/{developer_id}", response_model=DeveloperResponse)
def get_developer(developer_id: str, db: Session = Depends(get_db)):
    dev = db.query(Developer).filter(Developer.id == developer_id).first()
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Developer not found")
    return dev


@router.put("/developers/{developer_id}", response_model=DeveloperResponse)
def update_developer(developer_id: str, body: DeveloperUpdate, db: Session = Depends(get_db)):
    dev = db.query(Developer).filter(Developer.id == developer_id).first()
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Developer not found")
    if body.name is not None:
        dev.name = body.name
    if body.email is not None:
        existing = db.query(Developer).filter(Developer.email == body.email, Developer.id != developer_id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        dev.email = body.email
    if body.password is not None:
        dev.password_hash = hash_password(body.password)
    db.commit()
    db.refresh(dev)
    return dev


@router.delete("/developers/{developer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_developer(developer_id: str, db: Session = Depends(get_db)):
    dev = db.query(Developer).filter(Developer.id == developer_id).first()
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Developer not found")
    db.delete(dev)
    db.commit()


# ──────────────────────── Tasks ────────────────────────

@router.get("/tasks", response_model=List[TaskDetailResponse])
def list_tasks(
    project_id: str = None,
    developer_id: str = None,
    db: Session = Depends(get_db),
):
    q = db.query(Task)
    if project_id:
        q = q.filter(Task.project_id == project_id)
    if developer_id:
        q = q.filter(Task.developer_id == developer_id)
    return q.order_by(Task.created_at.desc()).all()


@router.post("/tasks", response_model=TaskDetailResponse, status_code=status.HTTP_201_CREATED)
def create_task(body: TaskCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == body.project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    dev = db.query(Developer).filter(Developer.id == body.developer_id).first()
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Developer not found")
    task = Task(
        title=body.title,
        description=body.description,
        status=body.status,
        project_id=body.project_id,
        developer_id=body.developer_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/tasks/{task_id}", response_model=TaskDetailResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskDetailResponse)
def update_task(task_id: str, body: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if body.title is not None:
        task.title = body.title
    if body.description is not None:
        task.description = body.description
    if body.status is not None:
        task.status = body.status
    if body.project_id is not None:
        project = db.query(Project).filter(Project.id == body.project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        task.project_id = body.project_id
    if body.developer_id is not None:
        dev = db.query(Developer).filter(Developer.id == body.developer_id).first()
        if not dev:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Developer not found")
        task.developer_id = body.developer_id
    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(task)
    db.commit()
