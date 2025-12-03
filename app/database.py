# app/database.py
import os 

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ----------------------------------------------------------------------
# 🚨 CORRECCIÓN CLAVE: Adaptar la URL para Render
# ----------------------------------------------------------------------

# 1. Leer la URL del entorno (Render usará esta, o usará la local si está en desarrollo).
DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://postgres:313586@localhost:5432/elite_gym"
)

# 2. Reemplazo necesario para compatibilidad con el driver de Render/SQLAlchemy
# Render a veces proporciona la URL con 'postgres://', SQLAlchemy necesita 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1) 

# ----------------------------------------------------------------------

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para los routers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()