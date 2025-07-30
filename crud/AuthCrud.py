import logging
import traceback



from core.Databases import db





async def ObtenerUsuarioPorUsuario(nombreUsuario: str):
    try:
        query = """"
             select * from usuario u
                where
                u.usuario_id =$1 and u.estado ='AC'
            """
        rows = await db.fetch_one(query, nombreUsuario)
        return
    except Exception as e:
        logging.error("Ocurrió un error:\n" + traceback.format_exc())
        raise e







