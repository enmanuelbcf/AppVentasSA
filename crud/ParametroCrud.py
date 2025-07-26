from core.Databases import db


async def ObtenerParametro(nombre_parametro: str):
    try:
        query = """
             select s.valor from parametro s where s.nombre_parametro = $1
            """
        rows = await db.fetch_one(query, nombre_parametro)
        return dict(rows)
    except Exception as e:
        raise e
