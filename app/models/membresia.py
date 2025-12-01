from sqlalchemy import Column, Integer, String, Float, Date, Text  # ← Agrega Text
from app.database import Base

class Membresia(Base):
    __tablename__ = "membresias"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    duracion_meses = Column(Integer, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    descripcion = Column(Text, nullable=True)  # ← NUEVA COLUMNA AGREGADA

    def __repr__(self):
        return f"<Membresia {self.nombre} - ${self.precio}>"