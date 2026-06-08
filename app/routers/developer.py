from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

try:
    from ..database import get_db
    from ..models import Task
    from ..schemas import TaskStatusUpdate, TaskDetailResponse
    from ..dependencies import get_current_developer
except ImportError:
    from database import get_db
    from models import Task
    from schemas import TaskStatusUpdate, TaskDetailResponse
    from dependencies import get_current_developer

router = APIRouter(prefix="/api/developer", tags=["Developer"], dependencies=[Depends(get_current_developer)])


@router.get("/tasks", response_model=List[TaskDetailResponse])
def list_my_tasks(
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_dev=Depends(get_current_developer),
):
    q = db.query(Task).filter(Task.developer_id == current_dev.id)
    if status_filter:
        q = q.filter(Task.status == status_filter)
    return q.order_by(Task.created_at.desc()).all()


@router.get("/tasks/{task_id}", response_model=TaskDetailResponse)
def get_my_task(task_id: str, db: Session = Depends(get_db), current_dev=Depends(get_current_developer)):
    task = db.query(Task).filter(Task.id == task_id, Task.developer_id == current_dev.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or not assigned to you")
    return task


@router.put("/tasks/{task_id}/status", response_model=TaskDetailResponse)
def update_task_status(
    task_id: str,
    body: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_dev=Depends(get_current_developer),
):
    task = db.query(Task).filter(Task.id == task_id, Task.developer_id == current_dev.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found or not assigned to you")
    task.status = body.status
    db.commit()
    db.refresh(task)
    return task
