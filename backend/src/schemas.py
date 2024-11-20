from datetime import datetime
from typing import Optional, List, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


# Author Schemas
class AuthorBase(BaseModel):
    id: int
    username: str = Field(..., max_length=50)
    email: str = Field(..., pattern=r"[^@]+@[^@]+\.[^@]+")
    is_ai: bool
    avatar: Optional[str] = Field(default=None)

    class Config:
        from_attributes = True


class AuthorCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: str = Field(..., pattern=r"[^@]+@[^@]+\.[^@]+")
    is_ai: bool
    avatar: Optional[str] = Field(default=None)


# Post Schemas
class PostBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)


class PostCreate(PostBase):
    author_id: int = Field(..., description="ID of the author creating the post")


class Post(PostBase):
    id: int
    timestamp: datetime
    author: AuthorBase

    class Config:
        from_attributes = True


# Paginated Response Schema
class PaginatedResponse(BaseModel, Generic[T]):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[T]


# Comment Schemas
class CommentCreate(BaseModel):
    author_id: int
    content: str = Field(..., min_length=1, max_length=300)


class CommentSchema(CommentCreate):
    id: int
    timestamp: datetime
    author: AuthorBase
    post_id: int

    class Config:
        from_attributes = True
