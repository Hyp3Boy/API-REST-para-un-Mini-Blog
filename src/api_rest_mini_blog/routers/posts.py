from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api_rest_mini_blog import models, schemas, services
from api_rest_mini_blog.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

async def get_post_or_404(post_id: int, db: AsyncSession = Depends(get_db)) -> models.Post:
    """
    Dependencia que obtiene un post por su ID. Si no lo encuentra,
    lanza una excepción HTTPException 404.
    """
    post = await services.get_post(db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    return post


@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.PostCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea una nueva publicación. Requiere el id del autor.
    """
    if not await services.user_exists(db, user_id=post.user_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"User with id {post.user_id} not found. Cannot create post."
        )
    
    return await services.create_post(db=db, post=post)

@router.get("/", response_model=List[schemas.Post])
async def read_posts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
    Obtiene las últimas N publicaciones.
    """
    posts = await services.get_posts(db, skip=skip, limit=limit)
    return posts

@router.get("/{post_id}", response_model=schemas.Post)
async def read_post(post: models.Post = Depends(get_post_or_404)):
    """
    Obtiene una publicación específica junto con sus comentarios.
    La lógica de buscar y validar si existe se maneja en la dependencia `get_post_or_404`.
    """
    return post

@router.post("/{post_id}/comments", response_model=schemas.Comment, status_code=status.HTTP_201_CREATED)
async def create_comment_for_post(
    comment: schemas.CommentCreate,
    post: models.Post = Depends(get_post_or_404), 
    db: AsyncSession = Depends(get_db)
):
    """
    Añade un nuevo comentario a una publicación. Requiere el id del autor.
    La validación de la existencia del post se delega a la dependencia.
    """
    if not await services.user_exists(db, user_id=comment.user_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"User with id {comment.user_id} not found. Cannot create comment."
        )

    return await services.create_comment(db=db, comment=comment, post_id=post.id)