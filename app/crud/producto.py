from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate

def crear_producto(db: Session, producto: ProductoCreate):
    try:
        db_producto = Producto(**producto.model_dump())
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        return db_producto
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Error de integridad en la base de datos")
    except Exception as e:
        db.rollback()
        raise e

def obtener_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Producto).offset(skip).limit(limit).all()

def obtener_producto_por_id(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id == producto_id).first()

def obtener_producto_por_nombre(db: Session, nombre: str):
    return db.query(Producto).filter(Producto.nombre == nombre).first()

def actualizar_producto(db: Session, producto_id: int, producto_data: ProductoUpdate):
    try:
        db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if not db_producto:
            return None
        
        update_data = producto_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_producto, field, value)
        
        db.commit()
        db.refresh(db_producto)
        return db_producto
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Error de integridad en la base de datos")
    except Exception as e:
        db.rollback()
        raise e

def eliminar_producto(db: Session, producto_id: int):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if db_producto:
        db.delete(db_producto)
        db.commit()
        return True
    return False