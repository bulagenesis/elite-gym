from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.crud.producto import (
    crear_producto, 
    obtener_productos, 
    obtener_producto_por_id,
    obtener_productos_por_categoria,
    actualizar_producto, 
    eliminar_producto
)
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from app.database import get_db

router = APIRouter(tags=["productos"])


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def api_crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    try:
        return crear_producto(db, producto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[ProductoResponse])
def api_obtener_productos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    try:
        return obtener_productos(db, skip=skip, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{producto_id}", response_model=ProductoResponse)
def api_obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    try:
        producto = obtener_producto_por_id(db, producto_id)
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return producto
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/categoria/{categoria}", response_model=List[ProductoResponse])
def api_obtener_productos_por_categoria(categoria: str, db: Session = Depends(get_db)):
    try:
        return obtener_productos_por_categoria(db, categoria)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{producto_id}", response_model=ProductoResponse)
def api_actualizar_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    try:
        db_producto = actualizar_producto(db, producto_id, producto)
        if not db_producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return db_producto
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{producto_id}", status_code=status.HTTP_200_OK)
def api_eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    try:
        success = eliminar_producto(db, producto_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return {"message": "Producto eliminado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
