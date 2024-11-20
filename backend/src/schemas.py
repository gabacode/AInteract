from datetime import datetime
from typing import Optional, List, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


# Personalities Schemas
class PersonalityBase(BaseModel):
    id: int
    hobbies: List[str] = Field(default_factory=list, description="List of hobbies")
    directives: List[dict] = Field(default_factory=list, description="Directives for behavior")
    core_memories: List[dict] = Field(default_factory=list, description="Core memories")

    class Config:
        from_attributes = True


class PersonalityCreate(BaseModel):
    hobbies: List[str] = Field(default_factory=list, description="List of hobbies")
    directives: List[dict] = Field(default_factory=list, description="Directives for behavior")
    core_memories: List[dict] = Field(default_factory=list, description="Core memories")


# Author Schemas
class AuthorBase(BaseModel):
    id: int
    username: str = Field(..., max_length=50)
    email: str = Field(..., pattern=r"[^@]+@[^@]+\.[^@]+")
    is_ai: bool
    avatar: Optional[str] = Field(default=None)
    personality: Optional[PersonalityBase] = None

    class Config:
        from_attributes = True


class Personality(PersonalityBase):
    author: AuthorBase


class AuthorCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: str = Field(..., pattern=r"[^@]+@[^@]+\.[^@]+")
    is_ai: bool
    avatar: Optional[str] = Field(default=None)


# Post Schemas
class PostBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=2048)


class PostCreate(PostBase):
    author_id: int = Field(..., description="ID of the author creating the post")


class Post(PostBase):
    id: int
    timestamp: datetime
    author: AuthorBase

    class Config:
        from_attributes = True


# Comment Schemas
class CommentCreate(BaseModel):
    author_id: int
    content: str = Field(..., min_length=1, max_length=1024)


class CommentSchema(CommentCreate):
    id: int
    timestamp: datetime
    author: AuthorBase
    post_id: int

    class Config:
        from_attributes = True


# Paginated Response Schema
class PaginatedResponse(BaseModel, Generic[T]):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[T]
