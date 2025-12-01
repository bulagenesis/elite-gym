from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class MembresiaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre de la membresía")
    precio: float = Field(..., gt=0, description="Precio de la membresía")
    duracion_meses: int = Field(..., gt=0, description="Duración en meses")
    descripcion: Optional[str] = Field(None, description="Descripción de la membresía")  # ← NUEVO CAMPO

class MembresiaCreate(MembresiaBase):
    fecha_inicio: date = Field(..., description="Fecha de inicio de la membresía")

class MembresiaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    precio: Optional[float] = Field(None, gt=0)
    duracion_meses: Optional[int] = Field(None, gt=0)
    fecha_inicio: Optional[date] = Field(None)
    descripcion: Optional[str] = Field(None)  # ← NUEVO CAMPO

class MembresiaResponse(MembresiaBase):
    id: int = Field(..., description="ID único de la membresía")
    fecha_inicio: date = Field(..., description="Fecha de inicio de la membresía")

    model_config = {"from_attributes": True}