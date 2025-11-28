from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Pago(Base):
    __tablename__ = "pagos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    membresia_id = Column(Integer, ForeignKey("membresias.id"), nullable=False)
    valor = Column(Float, nullable=False)
    fecha_pago = Column(Date, nullable=False)

    def __repr__(self):
        return f"<Pago Cliente:{self.cliente_id} - ${self.valor}>"