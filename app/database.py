import os  # Necesario para leer variables de entorno

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ----------------------------------------------------------------------
# CORRECCIÓN: Lee la URL del entorno. Usa la URL local como respaldo.
# ----------------------------------------------------------------------
DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://postgres:313586@localhost:5432/elite_gym"
)
# ----------------------------------------------------------------------

# El resto del código permanece igual

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
