from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.venta import crear_venta, obtener_ventas, obtener_venta_por_id
from app.schemas.venta import VentaCreate, VentaResponse
from app.database import get_db

router = APIRouter(tags=["ventas"])

@router.post("/", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def api_crear_venta(venta: VentaCreate, db: Session = Depends(get_db)):
    try:
        return crear_venta(db, venta)
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

@router.get("/", response_model=List[VentaResponse])
def api_obtener_ventas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        return obtener_ventas(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ventas: {str(e)}"
        )

@router.get("/{venta_id}", response_model=VentaResponse)
def api_obtener_venta(venta_id: int, db: Session = Depends(get_db)):
    venta = obtener_venta_por_id(db, venta_id)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada"
        )
    return venta