from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Pago(Base):
    __tablename__ = "pagos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    valor = Column(Float, nullable=False)
    fecha_pago = Column(Date, nullable=False)
    
    # NUEVAS COLUMNAS PARA PAGOS FRACCIONADOS
    tipo_pago = Column(String(20), nullable=False, default="completo")
    es_abono_inicial = Column(Boolean, default=False)
    pago_relacionado_id = Column(Integer, ForeignKey("pagos.id"), nullable=True)
    
    # RELACIONES
    cliente = relationship("Cliente", back_populates="pagos")
    pago_relacionado = relationship("Pago", remote_side=[id], backref="abonos_relacionados")

    def __repr__(self):
        tipo = "Abono" if self.es_abono_inicial else "Pago"
        return f"<{tipo} ${self.valor} - {self.tipo_pago} - Cliente {self.cliente_id}>"