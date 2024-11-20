from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_ai = Column(Boolean, default=False, server_default="false")
    avatar = Column(String, nullable=True)

    # Relationships
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    personality = relationship(
        "Personalities",
        back_populates="author",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True
    )


class Personalities(Base):
    __tablename__ = "personalities"
    id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True)
    hobbies = Column(ARRAY(String), nullable=True)
    directives = Column(JSONB, nullable=True)
    core_memories = Column(JSONB, nullable=True)

    # Relationships
    author = relationship("Author", back_populates="personality", cascade="all")
    memories = relationship(
        "Memory", back_populates="personality", cascade="all, delete-orphan"
    )

    # Index for JSONB fields for efficient querying
    __table_args__ = (
        Index('ix_personalities_hobbies', hobbies, postgresql_using='gin'),
        Index('ix_personalities_directives', directives, postgresql_using='gin'),
    )

    @validates('directives')
    def validate_directives(self, key, value):
        if value:
            for directive in value:
                if not isinstance(directive, dict) or 'task' not in directive or 'priority' not in directive:
                    raise ValueError("Each directive must include 'task' and 'priority'.")
        return value


class Memory(Base):
    __tablename__ = "memories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    personality_id = Column(Integer, ForeignKey("personalities.id", ondelete="CASCADE"))
    description = Column(String, nullable=False)
    meta_data = Column(JSONB, nullable=True)  # Renamed from 'metadata' to 'meta_data'

    # Relationships
    personality = relationship("Personalities", back_populates="memories")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"))

    # Relationships
    author = relationship("Author", back_populates="posts")
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
