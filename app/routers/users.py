from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.user import crear_user, obtener_users
from app.schemas.user import UserCreate, UserResponse
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=UserResponse)
def api_crear_user(user: UserCreate, db: Session = Depends(get_db)):
    return crear_user(db, user)

@router.get("/", response_model=list[UserResponse])
def api_obtener_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return obtener_users(db, skip, limit)
