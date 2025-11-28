from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.membresia import Membresia
from app.schemas.membresia import MembresiaCreate, MembresiaUpdate

def crear_membresia(db: Session, membresia: MembresiaCreate):
    try:
        db_membresia = Membresia(**membresia.model_dump())
        db.add(db_membresia)
        db.commit()
        db.refresh(db_membresia)
        return db_membresia
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Error de integridad en la base de datos")
    except Exception as e:
        db.rollback()
        raise e

def obtener_membresias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Membresia).offset(skip).limit(limit).all()

def obtener_membresia_por_id(db: Session, membresia_id: int):
    return db.query(Membresia).filter(Membresia.id == membresia_id).first()

def obtener_membresia_por_nombre(db: Session, nombre: str):
    return db.query(Membresia).filter(Membresia.nombre == nombre).first()

def actualizar_membresia(db: Session, membresia_id: int, membresia_data: MembresiaUpdate):
    try:
        db_membresia = db.query(Membresia).filter(Membresia.id == membresia_id).first()
        if not db_membresia:
            return None
        
        update_data = membresia_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_membresia, field, value)
        
        db.commit()
        db.refresh(db_membresia)
        return db_membresia
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Error de integridad en la base de datos")
    except Exception as e:
        db.rollback()
        raise e

def eliminar_membresia(db: Session, membresia_id: int):
    db_membresia = db.query(Membresia).filter(Membresia.id == membresia_id).first()
    if db_membresia:
        db.delete(db_membresia)
        db.commit()
        return True
    return False