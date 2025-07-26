from pydantic import Field
from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, EmailStr


class UsuarioCrate(BaseModel):
    nombre: str
    correo_electronico: EmailStr
    usuario_nombre: str
    negocio_id:int

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    usuario_nombre:str
    correo_electronico: EmailStr
    estado: Literal['AC', 'IN', 'PE']
    fecha_creacion: Optional[datetime]
    negocio_id: int

class UsuarioResponseService(BaseModel):
    nombre: str
    usuario_nombre:str
    correo_electronico: EmailStr
    estado: Literal['AC', 'IN', 'PE']

class PasswordUpdateRequest(BaseModel):
    nueva_password: str = Field(..., min_length=8, max_length=100, description="Debe tener al menos 8 caracteres")



