# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api_rest_mini_blog import schemas, services
from api_rest_mini_blog.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea un nuevo usuario.
    """
    db_user = await services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await services.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Obtiene los detalles de un usuario específico por su ID.
    """
    db_user = await services.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user