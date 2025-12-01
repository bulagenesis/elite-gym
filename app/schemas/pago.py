from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class PagoBase(BaseModel):
    cliente_id: int = Field(..., description="ID del cliente")
    valor: float = Field(..., gt=0, description="Valor del pago")
    fecha_pago: date = Field(..., description="Fecha del pago")
    tipo_pago: str = Field("completo", description="Tipo de pago: 'completo' o 'fraccionado'")
    es_abono_inicial: Optional[bool] = Field(False, description="Si es abono inicial en pago fraccionado")
    pago_relacionado_id: Optional[int] = Field(None, description="ID del pago relacionado")

class PagoCreate(PagoBase):
    pass

class PagoUpdate(BaseModel):
    cliente_id: Optional[int] = Field(None, description="ID del cliente")
    valor: Optional[float] = Field(None, gt=0, description="Valor del pago")
    fecha_pago: Optional[date] = Field(None, description="Fecha del pago")
    tipo_pago: Optional[str] = Field(None, description="Tipo de pago")
    es_abono_inicial: Optional[bool] = Field(None, description="Si es abono inicial")
    pago_relacionado_id: Optional[int] = Field(None, description="ID del pago relacionado")

class PagoResponse(PagoBase):
    id: int = Field(..., description="ID único del pago")

    model_config = {"from_attributes": True}