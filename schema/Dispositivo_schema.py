
from pydantic import BaseModel


class CrearDispositivoUsuario(BaseModel):
    player_id: str
    modelo_movil:str
    marca_movil:str