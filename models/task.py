from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    user_id: int
    title: str
    description: Optional[str] = None
    status: Optional[str] = "To Do"  # Kanban: 'To Do', 'In Progress', 'Done'
    priority: Optional[int] = 1       # 1: baja, 2: media, 3: alta

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None

class Task(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    status: str
    priority: int
    created_at: datetime
    updated_at: datetime
