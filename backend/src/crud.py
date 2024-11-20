import logging
from typing import Type

from sqlalchemy import func, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from .models import Post, Author, Comment, Personalities
from .schemas import PostCreate, AuthorCreate, PersonalityCreate


# Posts
def get_posts(db: Session, count_only: bool = False, skip: int = 0, limit: int = 10) -> list[Type[Post]]:
    """Retrieve a list of posts with pagination."""
    try:
        if count_only:
            return db.query(func.count(Post.id)).scalar()
        return (
            db.query(Post)
            .order_by(desc(Post.timestamp))
            .offset(skip)
            .limit(limit)
            .all()
        )
    except SQLAlchemyError as e:
        raise ValueError(f"Database error: {str(e)}")


def create_post(db: Session, post: PostCreate):
    """Create a new post."""
    try:
        get_author_by_id(db, post.author_id)
        db_post = Post(content=post.content, author_id=post.author_id)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error: {str(e)}")
        raise ValueError(f"Database error: {str(e)}")


def delete_post(db: Session, post_id: int):
    """Delete a post by its ID along with related comments."""
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise ValueError(f"Post with ID {post_id} does not exist.")
        db.delete(post)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Database error: {str(e)}")


# Authors
def get_authors(db: Session, skip: int = 0, limit: int = 10) -> list[Type[Author]]:
    """Retrieve a list of authors with pagination."""
    try:
        return db.query(Author).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        raise ValueError(f"Database error: {str(e)}")


def create_author(db: Session, author: AuthorCreate):
    """Create a new author with auto-generated ID and handle duplicate emails."""
    try:
        existing_author = db.query(Author).filter(Author.email == author.email).first()
        if existing_author:
            raise ValueError(f"An author with the email {author.email} already exists.")

        db_author = Author(
            username=author.username,
            email=author.email,
            is_ai=author.is_ai,
            avatar=author.avatar,
        )
        db.add(db_author)
        db.flush()

        if author.personality:
            directives = [
                directive.to_dict() for directive in author.personality.directives
            ]
            core_memories = [
                memory.to_dict() for memory in author.personality.core_memories
            ]

            personality = Personalities(
                id=db_author.id,
                hobbies=author.personality.hobbies,
                directives=directives,
                core_memories=core_memories,
            )
            db.add(personality)

        db.commit()
        db.refresh(db_author)
        return db_author
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Database error: {str(e)}")


def get_author_by_id(db: Session, author_id: int):
    """Retrieve an author by ID."""
    try:
        author = db.query(Author).filter(Author.id == author_id).first()
        if not author:
            raise ValueError(f"Author with ID {author_id} does not exist")
        return author
    except SQLAlchemyError as e:
        raise ValueError(f"Database error: {str(e)}")


# Personalities
def get_personality_by_author_id(db: Session, author_id: int):
    """Retrieve a personality by the associated author ID."""
    try:
        personality = db.query(Personalities).filter(Personalities.id == author_id).first()
        if not personality:
            raise ValueError(f"Personality for Author ID {author_id} does not exist.")
        return personality
    except SQLAlchemyError as e:
        raise ValueError(f"Database error: {str(e)}")


def create_personality(db: Session, author_id: int, personality: PersonalityCreate):
    """Create or update a personality for an author."""
    try:
        author = db.query(Author).filter(Author.id == author_id).first()
        if not author:
            raise ValueError(f"Author with ID {author_id} does not exist.")

        existing_personality = db.query(Personalities).filter(Personalities.id == author_id).first()
        if existing_personality:
            raise ValueError(f"Personality for Author ID {author_id} already exists.")

        # Create a new personality
        new_personality = Personalities(
            id=author_id,
            hobbies=personality.hobbies,
            directives=personality.directives,
            core_memories=personality.core_memories,
        )
        db.add(new_personality)
        db.commit()
        db.refresh(new_personality)
        return new_personality
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Database error: {str(e)}")


def update_personality(db: Session, author_id: int, personality: PersonalityCreate):
    """Update an existing personality."""
    try:
        existing_personality = db.query(Personalities).filter(Personalities.id == author_id).first()
        if not existing_personality:
            raise ValueError(f"Personality for Author ID {author_id} does not exist.")

        existing_personality.hobbies = personality.hobbies
        existing_personality.directives = personality.directives
        existing_personality.core_memories = personality.core_memories

        db.commit()
        db.refresh(existing_personality)
        return existing_personality
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Database error: {str(e)}")


def delete_personality(db: Session, author_id: int) -> bool:
    """Delete a personality by the associated author ID."""
    try:
        personality = db.query(Personalities).filter(Personalities.id == author_id).first()
        if not personality:
            raise ValueError(f"Personality for Author ID {author_id} does not exist.")

        db.delete(personality)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Database error: {str(e)}")


# Comments
def create_comment(db: Session, post_id: int, author_id: int, content: str) -> Comment:
    """Create a new comment."""
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise ValueError(f"Post with ID {post_id} does not exist.")

        author = db.query(Author).filter(Author.id == author_id).first()
        if not author:
            raise ValueError(f"Author with ID {author_id} does not exist.")

        comment = Comment(content=content, post_id=post_id, author_id=author_id)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Database error: {str(e)}")


def get_comments_by_post(db: Session, post_id: int):
    """Retrieve all comments for a specific post, including author information."""
    try:
        return (
            db.query(Comment)
            .filter(Comment.post_id == post_id)
            .options(joinedload(Comment.author))
            .order_by(Comment.timestamp.asc())
            .all()
        )
    except SQLAlchemyError as e:
        raise ValueError(f"Database error: {str(e)}")


def delete_comment(db: Session, post_id: int, comment_id: int) -> bool:
    """Delete a comment by its ID and post ID."""
    try:
        comment = (
            db.query(Comment)
            .filter(Comment.id == comment_id, Comment.post_id == post_id)
            .first()
        )
        if not comment:
            raise ValueError(f"Comment with ID {comment_id} on Post {post_id} does not exist.")
        db.delete(comment)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Database error: {str(e)}")
