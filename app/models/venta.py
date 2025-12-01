from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Venta(Base):
    __tablename__ = "ventas"
    
    id = Column(Integer, primary_key=True, index=True)
    fecha_venta = Column(DateTime, nullable=False)
    total = Column(Float, nullable=False)
    metodo_pago = Column(String(20), nullable=False)
    cliente_id = Column(Integer, nullable=True)
    
    productos = relationship("ProductoVendido", back_populates="venta")

class ProductoVendido(Base):
    __tablename__ = "productos_vendidos"
    
    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    venta = relationship("Venta", back_populates="productos")
    producto = relationship("Producto")