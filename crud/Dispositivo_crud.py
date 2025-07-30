import logging
import traceback
from datetime import datetime

from app.constants.general import plataformas
from core.Databases import db
from schema.Dispositivo_schema import CrearDispositivoUsuario


async def insertar_dispositivo_usuario(dispositivo: CrearDispositivoUsuario, usuarioId:int):
    try:
        query = '''
            INSERT INTO dispositivos_usuario
                (usuario_id, player_id, plataforma, fecha_actualizacion, marca_movil, modelo_movil)
            VALUES 
                ($1, $2, $3, $4, $5, $6)
        '''
        await db.execute(
            query,
            usuarioId,
            dispositivo.player_id,
            plataformas.ANDROID,
            datetime.now(),
            dispositivo.marca_movil,
            dispositivo.modelo_movil
        )
    except Exception as e:
        logging.error("Ocurrió un error:\n" + traceback.format_exc())
        raise e