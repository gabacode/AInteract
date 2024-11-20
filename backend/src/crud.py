from sqlalchemy import func, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from .models import Post, Author, Comment
from .schemas import PostCreate, AuthorCreate


# Posts
def get_posts(db: Session, count_only: bool = False, skip: int = 0, limit: int = 10):
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
def get_authors(db: Session, skip: int = 0, limit: int = 10):
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

        db_author = Author(**author.model_dump())
        db.add(db_author)
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


def delete_comment(db: Session, comment_id: int) -> bool:
    """Delete a comment by its ID."""
    try:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise ValueError(f"Comment with ID {comment_id} does not exist.")
        db.delete(comment)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Database error: {str(e)}")
