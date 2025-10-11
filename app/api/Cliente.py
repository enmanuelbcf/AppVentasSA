import traceback

from fastapi import APIRouter, HTTPException, Query
from fastapi.params import Depends
from starlette import status
from uvicorn import logging

from app.api.Auth import decode_token
from app.constants.general import ERROR_INTERNO_SISTEMA
from core.Databases import db
from crud.ClienteCrud import BuscarUsuariosPorNombreParcialPaginado
from schema.clineteSchema import ClienteOut, ClienteCreate

router = APIRouter(prefix='/Cliente', tags=['cliente'])

@router.get('/obtenerCliente', status_code=status.HTTP_200_OK)
async def obtenerUsuarioServices(
    nombreCliente: str = Query(..., min_length=1, description="Nombre parcial o completo"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    my_user=Depends(decode_token)
):
    try:
        data = await BuscarUsuariosPorNombreParcialPaginado(nombreCliente,my_user['negocio_id'], limit, offset)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )

        return data

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ERROR_INTERNO_SISTEMA} - {str(e)}"
        )

@router.post("/crearCliente", response_model=ClienteOut, status_code=status.HTTP_201_CREATED)
async def crear_cliente_service(
        payload: ClienteCreate,
my_user=Depends(decode_token)):
    """
    Crea un cliente. Valida/normaliza con Pydantic:
    - nombre requerido
    - rnc/cédula: solo dígitos (9 o 11)
    - teléfono: solo dígitos; si viene 11 y empieza con '1', recorta a 10
    """
    try:
        if payload.rnc:
            dup = await db.fetch_one("SELECT clienteid FROM cliente WHERE rnc = $1 LIMIT 1", payload.rnc)
            if dup:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El RNC/Cédula ya existe"
                )

        # Insert
        insert_sql = """
            INSERT INTO cliente (nombre, rnc, telefono)
            VALUES ($1, $2, $3)
            RETURNING clienteid, nombre, rnc, telefono
        """
        row = await db.fetch_one(insert_sql, payload.nombre, payload.rnc, payload.telefono)

        if not row:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo crear el cliente"
            )

        return ClienteOut(**dict(row))

    except HTTPException:
        raise
    except Exception as e:
        logging.error("Ocurrió un error:\n" + traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ERROR_INTERNO_SISTEMA} - {str(e)}"
        )