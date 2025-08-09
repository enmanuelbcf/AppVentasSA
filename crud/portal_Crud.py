import logging
import traceback

from dns.e164 import query
from fastapi import HTTPException

from core.Databases import db


import logging
import traceback
from fastapi import HTTPException

from utils.Security import hash_password


async def ObtenerNegocioAdminService(descripcion: str = None, negocio_id: int = None):
    base_query = '''
        SELECT
            n.id AS Negocio_id,
            n.descripcion AS Descripcion,
            ak.api_key AS Apikey,
            ak.estado AS Estado
        FROM negocios n
        JOIN api_keys ak ON ak.negocio_id = n.id
    '''

    where_clauses = []
    values = []

    if descripcion:
        where_clauses.append(f"n.descripcion ILIKE ${len(values) + 1}")
        values.append(f"%{descripcion}%")

    if negocio_id is not None:
        where_clauses.append(f"ak.negocio_id = ${len(values) + 1}")
        values.append(negocio_id)

    if where_clauses:
        base_query += " WHERE " + ' AND '.join(where_clauses)

    try:
        result = await db.fetch_all(base_query, *values)
        return [dict(row) for row in result]
    except Exception:
        logging.error("Error en ObtenerNegocioAdminService: " + traceback.format_exc())


async def GestionApikey(negocio_id: int = None):

    query_buscar_estado_apy_key ='''
    select estado from api_keys n where negocio_id =$1; 
    '''

    upadte_estado_ac = '''
        update api_keys ak set estado = 'IN' where ak.negocio_id =$1
    '''

    upadte_estado_in = '''
           update api_keys ak set estado = 'AC' where ak.negocio_id =$1
       '''

    try:
        estado = await db.fetch_one(query_buscar_estado_apy_key, negocio_id)
        if estado['estado']=='AC':
            await db.fetch_one(upadte_estado_ac, negocio_id)
            return True
        elif estado['estado'] == 'IN':
            await db.fetch_one(upadte_estado_in, negocio_id)
            return True

    except Exception as e:
        logging.error("Error en ObtenerNegocioAdminService: " + traceback.format_exc())
        raise  e



async def ObtenerUsuarioAdminService(
    nombre: str | None = None,
    usuario_nombre: str | None = None,
    estado: str | None = None,
    negocio_id: int | None = None,
    negocio: str | None = None
):
    base_query = '''
        select
            u.usuario_id,
            u.nombre,
            u.usuario_nombre,
            u.correo_electronico,
            u.negocio_id,
            n.descripcion as Negocio,
            u.fecha_creacion,
            u.estado
        from usuario u 
        join negocios n  on n.id = u.negocio_id
    '''

    where_clauses = []
    values = []

    if nombre:
        where_clauses.append(f"u.nombre ILIKE ${len(values) + 1}")
        values.append(f"%{nombre}%")

    if usuario_nombre:
        where_clauses.append(f"u.usuario_nombre ILIKE ${len(values) + 1}")
        values.append(f"%{usuario_nombre}%")

    if estado:
        where_clauses.append(f"u.estado = ${len(values) + 1}")
        values.append(estado)

    if negocio_id is not None:
        where_clauses.append(f"u.negocio_id = ${len(values) + 1}")
        values.append(negocio_id)

    if negocio is not None:
        where_clauses.append(f'n.descripcion ILIKE ${len(values) + 1}')
        values.append(f'%{negocio}%')

    if where_clauses:
        base_query += " WHERE " + " AND ".join(where_clauses)

    try:
        result = await db.fetch_all(base_query, *values)
        return [dict(row) for row in result]
    except Exception as e:
        logging.error("Error en ObtenerUsuarioAdminService: " + traceback.format_exc())
        return e # o podés propagar la excepción si lo preferís


async def GestionUsuario(usuario_id: int = None):

    query_buscar_estado_apy_key ='''
    select estado from usuario u where u.usuario_id  =$1; 
    '''

    upadte_estado_ac = '''
        update usuario ak set estado = 'IN' where ak.usuario_id =$1
    '''

    upadte_estado_in = '''
           update usuario ak set estado = 'AC' where ak.usuario_id =$1
       '''

    try:
        estado = await db.fetch_one(query_buscar_estado_apy_key, usuario_id)
        if estado['estado']=='AC':
            await db.fetch_one(upadte_estado_ac, usuario_id)
            return True
        elif estado['estado'] == 'IN':
            await db.fetch_one(upadte_estado_in, usuario_id)
            return True

    except Exception as e:
        logging.error("Error en GestionUsuario: " + traceback.format_exc())
        raise  e


async def Reset_password(usuario_id: int):

    upadte_estado_ac = '''
        update usuario ak set estado = 'PE', password=$1 where ak.usuario_id =$2
    '''
    try:
        await db.fetch_one(upadte_estado_ac, hash_password('12345678'), usuario_id)
        return True
    except Exception as e:
        logging.error("Error en GestionUsuario: " + traceback.format_exc())
        raise  e

async def Unlock_user(usuario_id: int):

    query_buscar_estado_apy_key = '''
       select estado from usuario u where u.usuario_id  =$1; 
       '''
    upadte_estado_ac = '''
        update usuario ak set estado = 'AC', intento_sesion=0 where ak.usuario_id =$1
    '''
    try:
        estado = await db.fetch_one(query_buscar_estado_apy_key, usuario_id)
        if estado['estado'] !='BL':
             return False
        await db.fetch_one(upadte_estado_ac, usuario_id)
        return True
    except Exception as e:
        logging.error("Error en GestionUsuario: " + traceback.format_exc())
        raise  e

import logging
import traceback

async def ver_dispositivos(
     usuario_nombre: str | None = None,
     estado: str | None = None
):
    query = '''
        SELECT
            u.usuario_nombre,
            dp.player_id,
            dp.modelo_movil,
            dp.marca_movil,
            dp.estado
        FROM dispositivos_usuario dp
        JOIN usuario u ON u.usuario_id = dp.usuario_id
    '''
    where_clauses = []
    values = []

    if usuario_nombre:
        where_clauses.append(f"u.usuario_nombre = ${len(values) + 1}")
        values.append(usuario_nombre)

    if estado:
        where_clauses.append(f"dp.estado ILIKE ${len(values) + 1}")
        values.append(f"%{estado}%")

    if where_clauses:
        # Asegúrate de dejar espacios antes y después de WHERE y AND
        query += " WHERE " + " AND ".join(where_clauses)

    try:
        datos = await db.fetch_all(query, *values)
        return [dict(row) for row in datos]
    except Exception as e:
        logging.error("Error en ver_dispositivos: %s", traceback.format_exc())
        raise





