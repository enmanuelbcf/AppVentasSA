import re
from typing import Optional
from pydantic import BaseModel, Field, validator

# ========== MODELOS ==========

class ClienteCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    rnc: Optional[str] = None          # RNC (9) o Cédula (11), sin guiones
    telefono: Optional[str] = None     # Teléfono RD sin guiones (10 dígitos preferido)

    @validator('nombre', pre=True)
    def _strip_nombre(cls, v):
        v = (v or '').strip()
        if not v:
            raise ValueError('El nombre es requerido')
        return v

    @validator('rnc', pre=True, always=True)
    def _digits_rnc(cls, v):
        if v is None:
            return None
        d = re.sub(r'\D', '', str(v))
        if not d:
            return None
        # Acepta 9 (RNC) o 11 (Cédula). Si quieres permitir otros largos, elimina el if.
        if len(d) not in (9, 11):
            raise ValueError('El RNC/Cédula debe tener 9 o 11 dígitos')
        return d

    @validator('telefono', pre=True, always=True)
    def _normalize_phone_do(cls, v):
        if v is None:
            return None
        d = re.sub(r'\D', '', str(v))
        if not d:
            return None
        # Si viene 11 y empieza con 1 (formato NANP), recorta prefijo
        if len(d) == 11 and d.startswith('1'):
            d = d[1:]
        # Preferimos guardar 10 dígitos; si hay más, quedarse con los últimos 10
        if len(d) >= 10:
            d = d[-10:]
        return d or None


class ClienteOut(BaseModel):
    clienteid: int
    nombre: str
    rnc: Optional[str] = None
    telefono: Optional[str] = None
