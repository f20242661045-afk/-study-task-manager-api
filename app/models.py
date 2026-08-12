from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    priority: int = Field(ge=1, le=5)
    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    description: str | None = None
    priority: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )
    due_date: date | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    completed: bool
    due_date: date | None
    created_at: datetime


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
    )
    email: EmailStr
    password: str = Field(
        min_length=6,
        max_length=100,
    )


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str