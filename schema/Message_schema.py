from pydantic import BaseModel


class CrearMensaje(BaseModel):
    texto_mensaje:str
    id_notification_push:str