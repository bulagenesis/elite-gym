from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del cliente")
    apellido: str = Field(..., min_length=1, max_length=100, description="Apellido del cliente")
    cedula: str = Field(..., min_length=1, max_length=20, description="Cédula de identidad")
    telefono: Optional[str] = Field(None, max_length=20, description="Número de teléfono")
    email: Optional[EmailStr] = Field(None, max_length=100, description="Correo electrónico")

class ClienteCreate(ClienteBase):
    fecha_registro: date = Field(..., description="Fecha de registro del cliente")

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre del cliente")
    apellido: Optional[str] = Field(None, min_length=1, max_length=100, description="Apellido del cliente")
    telefono: Optional[str] = Field(None, max_length=20, description="Número de teléfono")
    email: Optional[EmailStr] = Field(None, max_length=100, description="Correo electrónico")
    fecha_registro: Optional[date] = Field(None, description="Fecha de registro del cliente")

class ClienteResponse(ClienteBase):
    id: int = Field(..., description="ID único del cliente")
    fecha_registro: date = Field(..., description="Fecha de registro del cliente")

    model_config = {"from_attributes": True}