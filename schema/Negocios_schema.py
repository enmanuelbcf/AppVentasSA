from typing import Optional

from pydantic import Field, validator

from pydantic import BaseModel


class negociosRespose(BaseModel):
    id: int
    descripcion: str
    preventa: bool
    sys_cuadre: bool
    rnc: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None


    class Config:
        from_attributes = True


class crearCuadreVenta(BaseModel):
    usuario: str
    nombre_completo: str
    numero_caja: int
    cuadre_id: int
    efectivo: float = Field(..., ge=0)
    monto_cheque: float = Field(..., ge=0)
    monto_tarjeta: float = Field(..., ge=0)
    monto_credito: float = Field(..., ge=0)
    monto_transferencia: float = Field(..., ge=0)





