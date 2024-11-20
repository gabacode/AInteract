import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_ai = Column(Boolean, default=False, server_default="false")
    avatar = Column(String, nullable=True)

    # Relationship to posts and comments
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"))
    author = relationship("Author", back_populates="posts")

    # Relationship to comments
    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"))

    # Relationships
    post = relationship("Post", back_populates="comments")
    author = relationship("Author", back_populates="comments")
