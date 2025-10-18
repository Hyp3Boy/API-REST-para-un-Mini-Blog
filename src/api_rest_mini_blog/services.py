# app/services.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api_rest_mini_blog import models, schemas

# Funciones de servicio para Users

async def user_exists(db: AsyncSession, user_id: int) -> bool:
    """
    Verifica de forma eficiente si un usuario existe.
    """
    result = await db.execute(select(models.User.id).where(models.User.id == user_id))
    return result.scalar_one_or_none() is not None

async def get_user(db: AsyncSession, user_id: int):
    """
    Obtiene un usuario por su ID, incluyendo sus publicaciones y comentarios.
    """
    query = (
        select(models.User)
        .where(models.User.id == user_id)
        .options(
            selectinload(models.User.posts),    
            selectinload(models.User.comments)  
        )
    )
    
    result = await db.execute(query)
    
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    """
    Obtiene un usuario por su email.
    """
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    """
    Crea un nuevo usuario en la base de datos.
    """
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# Funciones de servicio para Posts
async def create_post(db: AsyncSession, post: schemas.PostCreate):
    """
    Crea una nueva publicación.
    """
    db_post = models.Post(title=post.title, content=post.content, user_id=post.user_id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 10):
    """
    Obtiene una lista de las últimas N publicaciones.
    """
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .order_by(models.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_post(db: AsyncSession, post_id: int):
    """
    Obtiene una publicación específica junto con sus comentarios.
    """
    result = await db.execute(
        select(models.Post)
        .where(models.Post.id == post_id)
        .options(selectinload(models.Post.comments)) # Carga eficiente de comentarios
    )
    return result.scalar_one_or_none()


# Funciones de servicio para Comments
async def create_comment(db: AsyncSession, comment: schemas.CommentCreate, post_id: int):
    """
    Crea un nuevo comentario para una publicación.
    """
    db_comment = models.Comment(**comment.model_dump(), post_id=post_id)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment