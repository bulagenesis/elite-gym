from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class ProductoVendidoCreate(BaseModel):
    producto_id: int = Field(..., description="ID del producto")
    cantidad: int = Field(..., gt=0, description="Cantidad vendida")
    precio_unitario: float = Field(..., gt=0, description="Precio unitario")

class VentaCreate(BaseModel):
    productos: List[ProductoVendidoCreate] = Field(..., description="Lista de productos")
    metodo_pago: str = Field(..., description="efectivo, tarjeta o transferencia")
    cliente_id: Optional[int] = Field(None, description="ID del cliente")

class ProductoInfo(BaseModel):
    id: int
    nombre: str
    precio: float
    
    model_config = {"from_attributes": True}

class ProductoVendidoResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float
    producto: ProductoInfo  # 🔥 CAMBIO IMPORTANTE: producto en lugar de producto_nombre
    
    model_config = {"from_attributes": True}

class VentaResponse(BaseModel):
    id: int
    fecha_venta: datetime
    total: float
    metodo_pago: str
    cliente_id: Optional[int]
    productos: List[ProductoVendidoResponse]
    
    model_config = {"from_attributes": True}