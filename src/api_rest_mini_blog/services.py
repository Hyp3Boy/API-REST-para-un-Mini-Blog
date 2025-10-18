from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api_rest_mini_blog import models, schemas

# --- User Services ---
async def user_exists(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(select(models.User.id).where(models.User.id == user_id))
    return result.scalar_one_or_none() is not None

async def get_user(db: AsyncSession, user_id: int):
    query = (
        select(models.User)
        .where(models.User.id == user_id)
        .options(
            selectinload(models.User.posts).selectinload(models.Post.author),
            selectinload(models.User.posts).selectinload(models.Post.comments).selectinload(models.Comment.author),
            selectinload(models.User.comments).selectinload(models.Comment.author)
        )
    )
    result = await db.execute(query)
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# --- Post Services ---
async def create_post(db: AsyncSession, post: schemas.PostCreate):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post, attribute_names=['author'])
    return await get_post(db, post_id=db_post.id)

async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 10):
    """
    Obtiene una lista de las últimas N publicaciones.
    """
    result = await db.execute(
        select(models.Post)
        .options(
            selectinload(models.Post.author),
            selectinload(models.Post.comments).selectinload(models.Comment.author)
        )
        .order_by(models.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_post(db: AsyncSession, post_id: int):
    result = await db.execute(
        select(models.Post)
        .where(models.Post.id == post_id)
        .options(
            selectinload(models.Post.author), 
            selectinload(models.Post.comments).selectinload(models.Comment.author)
        )
    )
    return result.scalar_one_or_none()

# --- Comment Services ---
async def create_comment(db: AsyncSession, comment: schemas.CommentCreate, post_id: int):
    db_comment = models.Comment(**comment.model_dump(), post_id=post_id)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    await db.refresh(db_comment, attribute_names=['author'])
    return db_comment