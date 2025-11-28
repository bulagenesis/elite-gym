from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.crud.cliente import (
    crear_cliente, 
    obtener_clientes, 
    obtener_cliente_por_id,
    actualizar_cliente, 
    eliminar_cliente,
    obtener_cliente_por_cedula
)
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.database import get_db

router = APIRouter(tags=["clientes"])

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def api_crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    try:
        return crear_cliente(db, cliente)
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

@router.get("/", response_model=List[ClienteResponse])
def api_obtener_clientes(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_db)
):
    try:
        return obtener_clientes(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener clientes: {str(e)}"
        )

@router.get("/{cliente_id}", response_model=ClienteResponse)
def api_obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = obtener_cliente_por_id(db, cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    return cliente

@router.put("/{cliente_id}", response_model=ClienteResponse)
def api_actualizar_cliente(
    cliente_id: int, 
    cliente: ClienteUpdate, 
    db: Session = Depends(get_db)
):
    try:
        db_cliente = actualizar_cliente(db, cliente_id, cliente)
        if not db_cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        return db_cliente
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cliente: {str(e)}"
        )

@router.delete("/{cliente_id}", status_code=status.HTTP_200_OK)
def api_eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    success = eliminar_cliente(db, cliente_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    return {"message": "Cliente eliminado exitosamente"}

@router.get("/cedula/{cedula}", response_model=ClienteResponse)
def api_obtener_cliente_por_cedula(cedula: str, db: Session = Depends(get_db)):
    cliente = obtener_cliente_por_cedula(db, cedula)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    return cliente