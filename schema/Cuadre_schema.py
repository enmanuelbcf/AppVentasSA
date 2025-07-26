from pydantic import BaseModel
from datetime import datetime

class CrearCuadreVenta(BaseModel):
    usuario_id: str
    nombre_completo: str
    numero_caja: int
    cuadre_id: str
    efectivo: float
    monto_cheque: float
    monto_tarjeta: float
    monto_credito: float
    monto_transferencia: float

