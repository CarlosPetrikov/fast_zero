from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from fast_zero.models import TodoState


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class TodoPublic(BaseModel):
    id: int
    title: str
    description: str
    state: TodoState
    created_at: datetime
    updated_at: datetime


class TodoList(BaseModel):
    todos: list[TodoPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)  # fix: bug conversão SQLAlchemy -> Pydantic


class UserList(BaseModel):
    users: list[UserPublic]
