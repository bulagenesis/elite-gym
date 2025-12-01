from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    cedula = Column(String(20), unique=True, index=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    email = Column(String(100), unique=True, index=True, nullable=True)
    fecha_registro = Column(Date, nullable=False)

    # ✅ AGREGAR ESTA RELACIÓN
    pagos = relationship("Pago", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente {self.nombre} {self.apellido} - {self.cedula}>"