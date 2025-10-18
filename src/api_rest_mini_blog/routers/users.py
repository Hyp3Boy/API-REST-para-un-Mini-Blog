from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api_rest_mini_blog import models, schemas, services
from api_rest_mini_blog.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

async def get_user_or_404(user_id: int, db: AsyncSession = Depends(get_db)) -> models.User:
    """
    Dependencia que obtiene un usuario por su ID. Si no lo encuentra,
    lanza una excepción HTTPException 404.
    """
    user = await services.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


@router.post("/", response_model=schemas.UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea un nuevo usuario.
    Verifica que tanto el email como el username no estén ya en uso.
    """
    db_user = await services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{user.email}' is already registered."
        )
    
    return await services.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user: models.User = Depends(get_user_or_404)):
    """
    Obtiene los detalles de un usuario específico por su ID.
    La lógica de buscar y validar si el usuario existe se delega a la dependencia.
    """
    return user