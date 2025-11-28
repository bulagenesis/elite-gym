from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.crud.producto import (
    crear_producto, 
    obtener_productos, 
    obtener_producto_por_id,
    actualizar_producto, 
    eliminar_producto,
    obtener_producto_por_nombre
)
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from app.database import get_db

router = APIRouter(tags=["productos"])

@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def api_crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    try:
        return crear_producto(db, producto)
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

@router.get("/", response_model=List[ProductoResponse])
def api_obtener_productos(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_db)
):
    try:
        return obtener_productos(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos: {str(e)}"
        )

@router.get("/{producto_id}", response_model=ProductoResponse)
def api_obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = obtener_producto_por_id(db, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return producto

@router.put("/{producto_id}", response_model=ProductoResponse)
def api_actualizar_producto(
    producto_id: int, 
    producto: ProductoUpdate, 
    db: Session = Depends(get_db)
):
    try:
        db_producto = actualizar_producto(db, producto_id, producto)
        if not db_producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        return db_producto
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar producto: {str(e)}"
        )

@router.delete("/{producto_id}", status_code=status.HTTP_200_OK)
def api_eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    success = eliminar_producto(db, producto_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return {"message": "Producto eliminado exitosamente"}

@router.get("/nombre/{nombre}", response_model=ProductoResponse)
def api_obtener_producto_por_nombre(nombre: str, db: Session = Depends(get_db)):
    producto = obtener_producto_por_nombre(db, nombre)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return producto