import logging
import traceback
from datetime import datetime
from core.Databases import db



async def insertar_bicatora_errores(servicio_id, descripcion_error, datosRelacionados,usuario_id):

    try:
        query = '''
           INSERT INTO public.bitacora_errores
            (servicio_id, descripcion_error, datos_relacionados, usuario_id, fecha_ocurrencia)
             VALUES($1, $2, $3, $4, $5);
        '''
        await db.execute(
            query,
            servicio_id,
            descripcion_error,
            datosRelacionados,
            usuario_id,
            datetime.now()

        )

    except Exception as e:
        logging.error("Ocurrió un error:\n" + traceback.format_exc())
        raise e


