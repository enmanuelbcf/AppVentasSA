import logging
import traceback
from typing import Optional

from core.Databases import db
from schema.clineteSchema import ClienteCreate, ClienteOut


async def BuscarUsuariosPorNombreParcialPaginado(nombreUsuario: str, negocioId:int, limit: int = 20, offset: int = 0):
    try:
        patron = f"%{(nombreUsuario or '').strip()}%"
        query = """
            SELECT u.*
            FROM cliente u
            WHERE u.nombre ILIKE $1
            and u.negocioId = $2
            ORDER BY u.nombre ASC
            LIMIT $3 OFFSET $4
        """
        # Pasa cada arg por separado, no en tupla/lista
        rows = await db.fetch_all(query, patron, negocioId, limit, offset)
        return [dict(r) for r in rows]
    except Exception as e:
        print(e)
        logging.error("Ocurrió un error:\n" + traceback.format_exc())
        raise

async def CrearCliente(cliente: ClienteCreate) -> Optional[ClienteOut]:
    try:
        query = """
            INSERT INTO cliente (nombre, rnc, telefono)
            VALUES ($1, $2, $3)
            RETURNING clienteid, nombre, rnc, telefono
        """
        row = await db.fetch_one(
            query,
            cliente.nombre,
            cliente.rnc,
            cliente.telefono,
        )
        return ClienteOut(**dict(row)) if row else None

    except Exception:
        logging.error("Ocurrió un error:\n" + traceback.format_exc())
        raise

