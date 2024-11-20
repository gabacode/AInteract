import logging
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .crud import (
    get_posts,
    create_post,
    get_authors,
    create_author,
    delete_post,
    create_comment,
    get_comments_by_post,
    delete_comment,
)
from .database import SessionLocal, engine
from .models import Base, Author
from .schemas import (
    Post,
    PostCreate,
    PaginatedResponse,
    AuthorBase,
    AuthorCreate,
    CommentCreate,
    CommentSchema,
)
from .subscriptions import publish_new_post

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan event handler for startup and shutdown.
    """
    try:
        logging.info("Dropping and creating database schema...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        ensure_default_author()
        logging.info("Application started.")
        yield
    finally:
        logging.info("Application shutdown.")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def ensure_default_author():
    logging.info("Ensuring default author exists.")
    try:
        db = SessionLocal()
        if not db.query(Author).first():
            default_author = Author(
                username="Default Author",
                email="author@example.com",
                is_ai=False,
                avatar="https://i.pravatar.cc/150?img=12",
            )
            db.add(default_author)
            db.commit()
            logging.info("Default author created.")
        else:
            logging.info("Default author already exists.")
    except Exception as e:
        logging.error(f"An error occurred while ensuring default author: {str(e)}")
    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/posts", response_model=PaginatedResponse[Post], tags=["posts"])
def list_posts(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
):
    total_posts = get_posts(db, count_only=True)
    posts = get_posts(db, skip=skip, limit=limit)
    next_url = f"/posts?skip={skip + limit}&limit={limit}" if skip + limit < total_posts else None
    previous_url = f"/posts?skip={max(skip - limit, 0)}&limit={limit}" if skip > 0 else None

    return PaginatedResponse(
        count=total_posts,
        next=next_url,
        previous=previous_url,
        results=posts,
    )


@app.post("/posts", response_model=Post, tags=["posts"])
def add_post(post: PostCreate, db: Session = Depends(get_db)):
    try:
        new_post = create_post(db, post)
        publish_new_post(new_post.id)
        return new_post
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@app.delete("/posts/{post_id}", status_code=204, tags=["posts"])
def remove_post(post_id: int, db: Session = Depends(get_db)):
    """
    Remove a post by its ID.
    Returns a 204 No Content status if successful.
    """
    try:
        success = delete_post(db, post_id)
        if success:
            return
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@app.get("/authors", response_model=PaginatedResponse[AuthorBase], tags=["authors"])
def list_authors(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
):
    try:
        total_authors = db.query(Author).count()
        authors = get_authors(db, skip=skip, limit=limit)
        next_url = f"/authors?skip={skip + limit}&limit={limit}" if skip + limit < total_authors else None
        previous_url = f"/authors?skip={max(skip - limit, 0)}&limit={limit}" if skip > 0 else None

        return PaginatedResponse(
            count=total_authors,
            next=next_url,
            previous=previous_url,
            results=authors,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@app.post("/authors", response_model=AuthorBase, tags=["authors"])
def add_author(author: AuthorCreate, db: Session = Depends(get_db)):
    try:
        return create_author(db, author)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@app.post("/posts/{post_id}/comments", response_model=CommentSchema, tags=["comments"])
def add_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    """
    Add a comment to a specific post.
    """
    try:
        return create_comment(db, post_id, comment.author_id, comment.content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@app.get("/posts/{post_id}/comments", response_model=List[CommentSchema], tags=["comments"])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all comments for a specific post.
    """
    try:
        return get_comments_by_post(db, post_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@app.delete("/posts/{post_id}/comments/{comment_id}", status_code=204, tags=["comments"])
def remove_comment(post_id: int, comment_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific comment associated with a specific post.
    """
    try:
        success = delete_comment(db, post_id, comment_id)
        if success:
            return
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}",
        )
