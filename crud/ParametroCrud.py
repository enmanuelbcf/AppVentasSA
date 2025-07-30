import logging
import traceback

from core.Databases import db


async def ObtenerParametro(nombre_parametro: str):
    try:
        query = """
             select s.valor from parametro s where s.nombre_parametro = $1
            """
        rows = await db.fetch_one(query, nombre_parametro)
        return dict(rows)
    except Exception as e:
        logging.error("Ocurrió un error:\n" + traceback.format_exc())
        raise e
