from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.crud.membresia import (
    crear_membresia, 
    obtener_membresias, 
    obtener_membresia_por_id,
    actualizar_membresia, 
    eliminar_membresia,
    obtener_membresia_por_nombre
)
from app.schemas.membresia import MembresiaCreate, MembresiaUpdate, MembresiaResponse
from app.database import get_db

router = APIRouter(tags=["membresias"])

@router.post("/", response_model=MembresiaResponse, status_code=status.HTTP_201_CREATED)
def api_crear_membresia(membresia: MembresiaCreate, db: Session = Depends(get_db)):
    try:
        return crear_membresia(db, membresia)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/", response_model=List[MembresiaResponse])
def api_obtener_membresias(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_db)
):
    try:
        return obtener_membresias(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener membresías: {str(e)}"
        )

@router.get("/{membresia_id}", response_model=MembresiaResponse)
def api_obtener_membresia(membresia_id: int, db: Session = Depends(get_db)):
    membresia = obtener_membresia_por_id(db, membresia_id)
    if not membresia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membresía no encontrada"
        )
    return membresia

@router.put("/{membresia_id}", response_model=MembresiaResponse)
def api_actualizar_membresia(
    membresia_id: int, 
    membresia: MembresiaUpdate, 
    db: Session = Depends(get_db)
):
    try:
        db_membresia = actualizar_membresia(db, membresia_id, membresia)
        if not db_membresia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Membresía no encontrada"
            )
        return db_membresia
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar membresía: {str(e)}"
        )

@router.delete("/{membresia_id}", status_code=status.HTTP_200_OK)
def api_eliminar_membresia(membresia_id: int, db: Session = Depends(get_db)):
    success = eliminar_membresia(db, membresia_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membresía no encontrada"
        )
    return {"message": "Membresía eliminada exitosamente"}

@router.get("/nombre/{nombre}", response_model=MembresiaResponse)
def api_obtener_membresia_por_nombre(nombre: str, db: Session = Depends(get_db)):
    membresia = obtener_membresia_por_nombre(db, nombre)
    if not membresia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membresía no encontrada"
        )
    return membresia