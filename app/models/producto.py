from sqlalchemy import Column, Integer, String, Float, Text
from app.database import Base

class Producto(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    categoria = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Producto {self.nombre} - ${self.precio}>"