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
    except IntegrityError:
        db.rollback()
        raise ValueError("Error de integridad en la base de datos")
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error inesperado al crear producto: {str(e)}")


def obtener_productos(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(Producto).offset(skip).limit(limit).all()
    except Exception as e:
        raise ValueError(f"Error inesperado al obtener productos: {str(e)}")


def obtener_producto_por_id(db: Session, producto_id: int):
    try:
        return db.query(Producto).filter(Producto.id == producto_id).first()
    except Exception as e:
        raise ValueError(f"Error inesperado al obtener producto: {str(e)}")


def obtener_productos_por_categoria(db: Session, categoria: str):
    try:
        return db.query(Producto).filter(Producto.categoria == categoria).all()
    except Exception as e:
        raise ValueError(f"Error inesperado al obtener productos por categoría: {str(e)}")


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
    except IntegrityError:
        db.rollback()
        raise ValueError("Error de integridad en la base de datos")
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error inesperado al actualizar producto: {str(e)}")


def eliminar_producto(db: Session, producto_id: int):
    try:
        db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if not db_producto:
            return False

        db.delete(db_producto)
        db.commit()
        return True

    except IntegrityError:
        db.rollback()
        raise ValueError("No se puede eliminar el producto por restricciones de integridad")
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error inesperado al eliminar producto: {str(e)}")
