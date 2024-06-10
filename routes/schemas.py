from pydantic import BaseModel, EmailStr, constr, conint, validator
from typing import Optional
from datetime import datetime

# Project schema
class ProjectSchema(BaseModel):
    id: Optional[int]
    name: constr(min_length=1, max_length=255)
    description: Optional[str]
    manager: constr(min_length=1, max_length=255)
    start_date: datetime

# Task schema
class TaskSchema(BaseModel):
    id: Optional[int]
    name: constr(min_length=1, max_length=255)
    description: Optional[str]
    project_id: conint(gt=0)
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status_id: conint(gt=0)
    worker_id: conint(gt=0)

# Worker schema
class WorkerSchema(BaseModel):
    id: Optional[int]
    name: constr(min_length=1, max_length=255)
    title: Optional[str]
    login: constr(min_length=1, max_length=100)
    email: EmailStr
    password: constr(min_length=6)

    @validator('password')
    def password_strength(cls, v):
        # Add custom password validation logic here if needed
        return v

# File schema
class FileSchema(BaseModel):
    id: Optional[int]
    path: constr(min_length=1, max_length=255)
    type: Optional[constr(max_length=10)]
    description: Optional[str]
    task_id: conint(gt=0)

# Comment schema
class CommentSchema(BaseModel):
    id: Optional[int]
    text: constr(min_length=1)
    task_id: conint(gt=0)

# Status schema
class StatusSchema(BaseModel):
    id: Optional[int]
    status: constr(min_length=1, max_length=255)
