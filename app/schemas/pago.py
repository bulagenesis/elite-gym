from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class PagoBase(BaseModel):
    cliente_id: int = Field(..., description="ID del cliente")
    membresia_id: int = Field(..., description="ID de la membresía")
    valor: float = Field(..., gt=0, description="Valor del pago")
    fecha_pago: date = Field(..., description="Fecha del pago")

class PagoCreate(PagoBase):
    pass

class PagoUpdate(BaseModel):
    cliente_id: Optional[int] = Field(None, description="ID del cliente")
    membresia_id: Optional[int] = Field(None, description="ID de la membresía")
    valor: Optional[float] = Field(None, gt=0, description="Valor del pago")
    fecha_pago: Optional[date] = Field(None, description="Fecha del pago")

class PagoResponse(PagoBase):
    id: int = Field(..., description="ID único del pago")

    model_config = {"from_attributes": True}