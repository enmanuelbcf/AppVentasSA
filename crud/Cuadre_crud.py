import logging
import traceback
from datetime import datetime

from core.Databases import db
from crud.Historico_crud import insertar_bicatora_errores
from schema.Bitacora_schema import CrearBitacoraErrores
from schema.Cuadre_schema import CrearCuadreVenta


async def insertar_cuadre_venta(cuadre: CrearCuadreVenta):
    try:
        query = '''
           INSERT INTO cuadre_ventas (
    usuario_id,
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
        await db.execute(
            query,
            cuadre.usuario_id,
            cuadre.nombre_completo,
            cuadre.numero_caja,
            cuadre.cuadre_id,
            cuadre.efectivo,
            cuadre.monto_cheque,
            cuadre.monto_tarjeta,
            cuadre.monto_credito,
            cuadre.monto_transferencia,
            datetime.now(),


        )
    except Exception as e:
        logging.error("Ocurrió un error:\n" + traceback.format_exc())

        bitacora_error = CrearBitacoraErrores(
            servicioId=1,
            descripcionError=e,
            datosRelacionados=cuadre,
            usuario_id=cuadre.usuario_id
        )
        await insertar_bicatora_errores(bitacora_error)

        raise e