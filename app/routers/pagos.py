from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.crud.pago import (
    crear_pago, 
    obtener_pagos, 
    obtener_pago_por_id,
    actualizar_pago, 
    eliminar_pago,
    obtener_pagos_por_cliente,
    obtener_pagos_por_membresia
)
from app.schemas.pago import PagoCreate, PagoUpdate, PagoResponse
from app.database import get_db

router = APIRouter(tags=["pagos"])

@router.post("/", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def api_crear_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    try:
        return crear_pago(db, pago)
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

@router.get("/", response_model=List[PagoResponse])
def api_obtener_pagos(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_db)
):
    try:
        return obtener_pagos(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener pagos: {str(e)}"
        )

@router.get("/{pago_id}", response_model=PagoResponse)
def api_obtener_pago(pago_id: int, db: Session = Depends(get_db)):
    pago = obtener_pago_por_id(db, pago_id)
    if not pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado"
        )
    return pago

@router.put("/{pago_id}", response_model=PagoResponse)
def api_actualizar_pago(
    pago_id: int, 
    pago: PagoUpdate, 
    db: Session = Depends(get_db)
):
    try:
        db_pago = actualizar_pago(db, pago_id, pago)
        if not db_pago:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pago no encontrado"
            )
        return db_pago
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar pago: {str(e)}"
        )

@router.delete("/{pago_id}", status_code=status.HTTP_200_OK)
def api_eliminar_pago(pago_id: int, db: Session = Depends(get_db)):
    success = eliminar_pago(db, pago_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado"
        )
    return {"message": "Pago eliminado exitosamente"}

@router.get("/cliente/{cliente_id}", response_model=List[PagoResponse])
def api_obtener_pagos_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    try:
        return obtener_pagos_por_cliente(db, cliente_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener pagos del cliente: {str(e)}"
        )

@router.get("/membresia/{membresia_id}", response_model=List[PagoResponse])
def api_obtener_pagos_por_membresia(membresia_id: int, db: Session = Depends(get_db)):
    try:
        return obtener_pagos_por_membresia(db, membresia_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener pagos de la membresía: {str(e)}"
        )