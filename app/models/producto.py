from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Producto(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)  # ✅ Agregado stock

    def __repr__(self):
        return f"<Producto {self.nombre} - ${self.precio} (Stock: {self.stock})>"