import logging
import traceback
from datetime import datetime

from dns.e164 import query

from app.constants.general import plataformas
from core.Databases import db
from schema.Dispositivo_schema import CrearDispositivoUsuario
from schema.Message_schema import CrearMensaje


async def insertar_dispositivo_usuario(dispositivo: CrearDispositivoUsuario, usuarioId:int):
    try:
        query = '''
            INSERT INTO dispositivos_usuario
                (usuario_id, player_id, plataforma, fecha_actualizacion)
            VALUES 
                ($1, $2, $3, $4)
        '''
        await db.execute(
            query,
            usuarioId,
            dispositivo.player_id,
            plataformas.ANDROID,
            datetime.now()
        )
    except Exception as e:
        logging.error("Ocurrió un error:\n" + traceback.format_exc())
        raise e


async def RegistrarMensaje(dispostitvos:list, texto_mensaje:str, id_notificacion_push:str):
    try:
        query = """
        insert into mensajes_usuario (usuario_id, dispositivo_id, texto_mensaje, id_notificacion_push,fecha_envio)
        values($1,$2,$3,$4, $5)
        """

        for dispositivo in dispostitvos:
            await db.execute(
                query,
                dispositivo['usuario_id'],
                dispositivo['dispositivos_usuario_id'],
                texto_mensaje,
                id_notificacion_push,
                datetime.now()
            )

    except Exception as e:
        logging.error("Ocurrió un error:\n" + traceback.format_exc())
        raise e


