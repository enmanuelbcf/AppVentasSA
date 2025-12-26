import traceback

from fastapi import APIRouter, HTTPException, Query
from fastapi.params import Depends
from starlette import status
from uvicorn import logging

from app.api.Auth import decode_token
from app.constants.general import ERROR_INTERNO_SISTEMA
from core.Databases import db
from crud.ClienteCrud import BuscarUsuariosPorNombreParcialPaginado, CrearCliente
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


@router.post("/crear-cliente", status_code=status.HTTP_201_CREATED)
async def crear_cliente_service(
    payload: ClienteCreate,
    my_user=Depends(decode_token)
):

    try:
        if not payload.nombre or payload.nombre.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El campo 'nombre' es obligatorio."
            )
        if payload.rnc:
            rnc = payload.rnc.replace("-", "").strip()
            if not (len(rnc) in (9, 11) and rnc.isdigit()):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El RNC/Cédula debe tener 9 (RNC) o 11 (Cédula) dígitos numéricos."
                )


        negocio_id = my_user["negocio_id"]
        nuevo_cliente = await CrearCliente(payload, negocio_id)

        if not nuevo_cliente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo crear el cliente. Verifique los datos enviados."
            )

        return {
            "status": "success",
            "message": "Cliente creado correctamente.",
            "data": nuevo_cliente
        }

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logging.error(
            f"❌ Error interno al crear cliente (negocio_id={my_user.get('negocio_id')}):\n"
            + traceback.format_exc()
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ERROR_INTERNO_SISTEMA} - {str(e)}"
        )
