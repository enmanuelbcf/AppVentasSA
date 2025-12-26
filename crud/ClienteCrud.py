import logging
import traceback
from typing import Optional

from asyncpg import UniqueViolationError

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

async def CrearCliente(cliente: ClienteCreate, negocio_id: int) -> Optional[ClienteOut]:
    try:
        # 🔹 Validación básica
        if not cliente.nombre or cliente.nombre.strip() == "":
            raise ValueError("El nombre del cliente es obligatorio")

        query = """
            INSERT INTO cliente (nombre, rnc, telefono, negocioid)
            VALUES ($1, $2, $3, $4)
            RETURNING clienteid, nombre, rnc, telefono, negocioid
        """

        # 🔹 Inserción del registro
        row = await db.fetch_one(
            query,
            cliente.nombre.strip(),
            cliente.rnc.strip() if cliente.rnc else None,
            cliente.telefono.strip() if cliente.telefono else None,
            negocio_id
        )

        # 🔹 Devolver el cliente creado
        return ClienteOut(**dict(row)) if row else None

    except UniqueViolationError as e:
        logging.warning(f"⚠️ RNC duplicado: {cliente.rnc}")
        raise Exception(f"Ya existe un cliente con el RNC {cliente.rnc}")

    except ValueError as ve:
        logging.warning(f"⚠️ Error de validación: {ve}")
        raise Exception(str(ve))

    except Exception as e:
        logging.error("❌ Ocurrió un error inesperado:\n" + traceback.format_exc())
        raise Exception(f"Error al crear cliente: {str(e)}")

