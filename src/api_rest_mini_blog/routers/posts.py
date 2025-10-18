from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api_rest_mini_blog import schemas, services
from api_rest_mini_blog.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.PostCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea una nueva publicación. Requiere el id del autor.
    """
    if not await services.user_exists(db, user_id=post.user_id):
        raise HTTPException(status_code=404, detail=f"User with id {post.user_id} not found")
    
    return await services.create_post(db=db, post=post)

@router.get("/", response_model=List[schemas.Post])
async def read_posts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
    Obtiene las últimas N publicaciones.
    """
    posts = await services.get_posts(db, skip=skip, limit=limit)
    return posts

@router.get("/{post_id}", response_model=schemas.Post)
async def read_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """
    Obtiene una publicación específica junto con sus comentarios.
    """
    db_post = await services.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.post("/{post_id}/comments", response_model=schemas.Comment, status_code=status.HTTP_201_CREATED)
async def create_comment_for_post(
    post_id: int, comment: schemas.CommentCreate, db: AsyncSession = Depends(get_db)
):
    """
    Añade un nuevo comentario a una publicación. Requiere el id del autor.
    """
    if not await services.user_exists(db, user_id=comment.user_id):
         raise HTTPException(status_code=404, detail=f"User with id {comment.user_id} not found")

    
    post = await services.get_post(db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")

    return await services.create_comment(db=db, comment=comment, post_id=post_id)