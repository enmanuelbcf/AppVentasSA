from pydantic import BaseModel, conint, constr, condecimal


class PreventaBase(BaseModel):
    clienteid:int
    descripcion: constr(strip_whitespace=True, min_length=1, max_length=200)
    cantidad: conint(strict=True, ge=1)
    precio: condecimal(max_digits=14, decimal_places=2, ge=0)
    codigoproducto: str


class Preventaout(BaseModel):
    descripcion: constr(strip_whitespace=True, min_length=1, max_length=200)
    cantidad: conint(strict=True, ge=1)
    precio: condecimal(max_digits=14, decimal_places=2, ge=0)
    codigoproducto: str