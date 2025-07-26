
from pydantic import Field


from pydantic import BaseModel


class negociosRespose(BaseModel):
    id: int
    descripcion:str

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





