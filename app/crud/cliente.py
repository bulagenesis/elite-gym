from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate

def crear_cliente(db: Session, cliente: ClienteCreate):
    try:
        db_cliente = Cliente(**cliente.model_dump())
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    except IntegrityError as e:
        db.rollback()
        if "cedula" in str(e.orig):
            raise ValueError("La cédula ya existe en el sistema")
        elif "email" in str(e.orig):
            raise ValueError("El email ya existe en el sistema")
        raise ValueError("Error de integridad en la base de datos")
    except Exception as e:
        db.rollback()
        raise e

def obtener_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cliente).offset(skip).limit(limit).all()

def obtener_cliente_por_id(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

def obtener_cliente_por_cedula(db: Session, cedula: str):
    return db.query(Cliente).filter(Cliente.cedula == cedula).first()

def actualizar_cliente(db: Session, cliente_id: int, cliente_data: ClienteUpdate):
    try:
        db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not db_cliente:
            return None
        
        update_data = cliente_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cliente, field, value)
        
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    except IntegrityError as e:
        db.rollback()
        if "cedula" in str(e.orig):
            raise ValueError("La cédula ya existe en el sistema")
        elif "email" in str(e.orig):
            raise ValueError("El email ya existe en el sistema")
        raise ValueError("Error de integridad en la base de datos")
    except Exception as e:
        db.rollback()
        raise e

def eliminar_cliente(db: Session, cliente_id: int):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
        return True
    return False