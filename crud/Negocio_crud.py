import logging
import traceback
from typing import List, Optional
from zoneinfo import ZoneInfo

from annotated_types import Timezone
from cffi.cffi_opcode import PRIM_INT
from dns.e164 import query
import json

from app.constants.general import Estados
from core.Databases import db
from crud.ParametroCrud import ObtenerParametro
from schema.Negocios_schema import crearCuadreVenta
from schema.preventaSchema import PreventaBase
from utils.Security import hash_password


async def insertar_cuadre_venta(cuadre: crearCuadreVenta, negocio_id:int):
    try:
        query='''
                INSERT INTO cuadre_ventas (
            usuario,
            nombre_completo,
            numero_caja,
            cuadre_id,
            efectivo,
            monto_cheque,
            monto_tarjeta,
            monto_credito,
            monto_transferencia,
            negocio_id,
            fecha_creacion
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11
        );
        '''
        fecha_rd = datetime.now(ZoneInfo("America/Santo_Domingo"))
        await db.execute(
            query,
            cuadre.usuario,
            cuadre.nombre_completo,
            cuadre.numero_caja,
            cuadre.cuadre_id,
            cuadre.efectivo,
            cuadre.monto_cheque,
            cuadre.monto_tarjeta,
            cuadre.monto_credito,
            cuadre.monto_transferencia,
            negocio_id,
            fecha_rd
        )

    except Exception as e:
        raise e

from datetime import datetime, timedelta


import math  # para usar math.ceil

import math

import math

async def ObtenerCuadrePorNegocioYFechas(
        NegocioId: int,
        FechaInicio: datetime,
        FechaFin: datetime,
        pagina: int = 1
):
    valor = await ObtenerParametro("REGISTROS_POR_PAGINA")
    limit = int(valor['valor'])
    offset = (pagina - 1) * limit

    query_deb_cre = """
       SELECT 
    SUM(cu.efectivo) AS efectivo,
    SUM(cu.monto_cheque) AS monto_cheque,
    SUM(cu.monto_tarjeta) AS monto_tarjeta,
    SUM(cu.monto_credito) AS monto_credito,
    SUM(cu.monto_transferencia) AS monto_transferencia,
    COUNT(DISTINCT cu.numero_caja) AS total_cajas,
    COUNT(distinct cu.usuario) as cajeros,
    count(*) as Transacciones
FROM 
    cuadre_ventas cu
WHERE 
    cu.negocio_id = $1
    AND cu.fecha_creacion::date BETWEEN $2 and $3
    
    """

    query_consulta = '''
        SELECT *,
               COUNT(*) OVER() AS total_registros
        FROM cuadre_ventas
        WHERE negocio_id = $1
          AND fecha_creacion::date BETWEEN $2 AND $3
        ORDER BY fecha_creacion DESC
        LIMIT $4 OFFSET $5
    '''
    try:
        rows = await db.fetch_all(query_consulta, NegocioId, FechaInicio, FechaFin, limit, offset)
        resumen = await db.fetch_one(query_deb_cre,NegocioId, FechaInicio, FechaFin)

        if not rows:
            return {
                'total_registros': 0,
                'total_paginas': 0,
                'pagina_actual': pagina,
                'registros_pagina': 0,
                'datos': []
            }

        total = rows[0]['total_registros']
        count_page = len(rows)
        total_paginas = math.ceil(total / limit) if limit > 0 else 1

        return {
            'efectivo': resumen['efectivo'],
            'monto_cheque': resumen['monto_cheque'],
            'monto_tarjeta': resumen['monto_tarjeta'],
            'monto_credito': resumen['monto_credito'],
            'monto_transferencia': resumen['monto_transferencia'],
            'total_cajas': resumen['total_cajas'],
            'cajeros': resumen['cajeros'],
            'transacciones': resumen['transacciones'],
            'datos': rows,
            'total_registros': total,
            'total_paginas': total_paginas,
            'pagina_actual': pagina,
            'registros_pagina': count_page

        }

    except Exception as e:
        logging.error("Ocurrió un error:\n" + traceback.format_exc())
        raise e



async def ObtenerPlayersNegocio(NegocioId: int):
    query = '''
       select du.player_id, u.usuario_id, du.dispositivos_usuario_id  from dispositivos_usuario du 
         join usuario u on u.usuario_id = du.usuario_id 
        where u.negocio_id = $1 and not (u.estado ='IN' or du.estado ='IN')
    '''
    try:
        rows = await db.fetch_all(query, NegocioId)
        lista_simple = [row for row in rows]
        return lista_simple
    except Exception as e:
        raise e

async def crear_negocio(descripcion:str, apikey:str):

    try:
        query = 'insert into negocios (descripcion) values ($1) returning id'
        result = await db.fetch_one(query, descripcion)
        negocioId = result[0]
        query_apikey = 'insert into api_keys (api_key,negocio_id) values ($1, $2)'
        await db.execute(query_apikey, hash_password(apikey), negocioId)

    except Exception as e:
        logging.error("Ocurrió un error:\n" + traceback.format_exc())
        raise e

async def verNegocios():
    try:
        query = 'select * from negocios'
        rows = await db.fetch_all(query)
        return [dict(row) for row in rows]
    except Exception as e:
        raise e

async def buscar_negocio_por_id(negocioId: int):
    try:
        query= 'select * from api_keys where negocio_id = $1 and estado =$2'
        rows = await db.fetch_one(query, negocioId, Estados.ACTIVO)
        return rows
    except Exception as e:
        logging.error("Ocurrió un error:\n" + traceback.format_exc())
        raise e

async def obtenerNegocioPorId(negocioId: int):
    try:
        query= 'select * from negocios where id =$1'
        rows = await db.fetch_one(query, negocioId)
        return rows
    except Exception as e:
        logging.error("Ocurrió un error:\n" + traceback.format_exc())
        raise e

async def crear_negocio(descripcion:str, apikey:str):

    try:
        query = 'insert into negocios (descripcion) values ($1) returning id'
        result = await db.fetch_one(query, descripcion)
        negocioId = result[0]
        query_apikey = 'insert into api_keys (api_key,negocio_id) values ($1, $2)'
        await db.execute(query_apikey, hash_password(apikey), negocioId)

    except Exception as e:
        logging.error("Ocurrió un error:\n" + traceback.format_exc())
        raise e

async def crear_orden(negocioId:int, preventa:  List[PreventaBase],usuarioId:int, ncf:str):
    try:
        query_orden = 'insert into ordenes (clienteid, fecha, negocioId, usuarioId, ncf) values ($1, now(), $2, $3, $4) returning ordenid'
        result = await db.fetch_one(query_orden, preventa[0].clienteid, negocioId, usuarioId, ncf)
        ordenid = result[0]

        query_preventa = 'insert into preventa (ordenid, cantidad,codigoproducto, descripcion, precio) values ($1, $2, $3, $4, $5)'
        for item in preventa:
            await db.execute(
                query_preventa,
                ordenid,
                item.cantidad,
                item.codigoproducto,
                item.descripcion,
                item.precio
            )

        return ordenid

    except Exception as e:
        logging.error("Ocurrió un error:" + traceback.format_exc())
        raise e


async def obtenerOrden(usuarioId: int, ordenId: int = None, nombre: str = None):
    try:
        query_orden = '''
        SELECT
    JSON_BUILD_OBJECT(
        'ordenId', O.ORDENID,
        'usuarioId', O.USUARIOID,
        'nombre', C.NOMBRE,
        'rnc', c.rnc,
        'ncf', o.ncf, 
        'preventa', JSON_AGG(
            JSON_BUILD_OBJECT(
                'descripcion', P.DESCRIPCION,
                'cantidad', P.CANTIDAD,
                'precio', P.PRECIO,
                'codigoProducto', P.CODIGOPRODUCTO
            )
        )
    ) AS orden
FROM ORDENES O
JOIN PREVENTA P ON P.ORDENID = O.ORDENID
JOIN CLIENTE C ON C.CLIENTEID = O.CLIENTEID
WHERE
    O.USUARIOID = $1
    AND ($2::int IS NULL OR O.ORDENID = $2::int)
    AND ($3::text IS NULL OR C.NOMBRE ILIKE '%' || $3::text || '%')
GROUP BY
    O.ORDENID, O.USUARIOID, C.NOMBRE,C.RNC,O.NCF
order by o.FECHA DESC;
        '''

        result = await db.fetch_all(query_orden, usuarioId, ordenId, nombre)

        ordenes = [json.loads(r['orden']) for r in result]

        return ordenes

    except Exception as e:
        logging.error("Error en obtenerOrden: " + traceback.format_exc())
        raise e
