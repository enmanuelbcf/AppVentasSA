from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr


class UsuarioModel(BaseModel):
    id: int
    nombre:str
    correo: EmailStr
    estado: Literal['AC', 'IN']
    fecha_creacion: Optional[datetime]