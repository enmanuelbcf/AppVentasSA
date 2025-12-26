from typing import Dict

from pydantic import BaseModel


class CrearBitacoraErrores(BaseModel):
    servicioId: int
    descripcionError: str
    datosRelacionados: Dict[str, any]
    usuario_id:int

