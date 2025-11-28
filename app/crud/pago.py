from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.pago import Pago
from app.schemas.pago import PagoCreate, PagoUpdate

def crear_pago(db: Session, pago: PagoCreate):
    try:
        db_pago = Pago(**pago.model_dump())
        db.add(db_pago)
        db.commit()
        db.refresh(db_pago)
        return db_pago
    except IntegrityError as e:
        db.rollback()
        if "cliente_id" in str(e.orig):
            raise ValueError("El cliente no existe")
        elif "membresia_id" in str(e.orig):
            raise ValueError("La membresía no existe")
        raise ValueError("Error de integridad en la base de datos")
    except Exception as e:
        db.rollback()
        raise e

def obtener_pagos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pago).offset(skip).limit(limit).all()

def obtener_pago_por_id(db: Session, pago_id: int):
    return db.query(Pago).filter(Pago.id == pago_id).first()

def obtener_pagos_por_cliente(db: Session, cliente_id: int):
    return db.query(Pago).filter(Pago.cliente_id == cliente_id).all()

def obtener_pagos_por_membresia(db: Session, membresia_id: int):
    return db.query(Pago).filter(Pago.membresia_id == membresia_id).all()

def actualizar_pago(db: Session, pago_id: int, pago_data: PagoUpdate):
    try:
        db_pago = db.query(Pago).filter(Pago.id == pago_id).first()
        if not db_pago:
            return None
        
        update_data = pago_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_pago, field, value)
        
        db.commit()
        db.refresh(db_pago)
        return db_pago
    except IntegrityError as e:
        db.rollback()
        if "cliente_id" in str(e.orig):
            raise ValueError("El cliente no existe")
        elif "membresia_id" in str(e.orig):
            raise ValueError("La membresía no existe")
        raise ValueError("Error de integridad en la base de datos")
    except Exception as e:
        db.rollback()
        raise e

def eliminar_pago(db: Session, pago_id: int):
    db_pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if db_pago:
        db.delete(db_pago)
        db.commit()
        return True
    return False