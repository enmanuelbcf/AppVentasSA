from datetime import datetime
from http.client import HTTPResponse
from telnetlib import STATUS
from tkinter.constants import E
from typing import Optional, Annotated

from fastapi import APIRouter, Header, HTTPException, Depends, Query
from starlette import status
from starlette.responses import JSONResponse

from app.api.Auth import decode_token
from app.constants.general import ERROR_INTERNO_SISTEMA, CUANDRE_INSERTADO, APIKEY_INVALIDA, ENCABEZADOS_REQUERIDOS
from crud.MessageCrud import RegistrarMensaje
from crud.Negocio_crud import buscar_negocio_por_id
from crud.Negocio_crud import insertar_cuadre_venta, ObtenerCuadrePorNegocioYFechas, ObtenerPlayersNegocio
from schema.Negocios_schema import crearCuadreVenta, negociosRespose
from service.one_signal_service import send_push_notification
from utils.Security import verificar_apy_key, verify_salt

router = APIRouter(prefix='/Negocio', tags=['/Negocio'])


async def validar_headers(
        api_key: Optional[str] = Header(None, alias="X-API-Key"),
        negocio_id: Optional[int] = Header(None, alias="X-Negocio-Id")
):


    if not api_key or not negocio_id:
        raise HTTPException(status_code=400, detail=f'{ENCABEZADOS_REQUERIDOS}')

    data = await buscar_negocio_por_id(negocio_id)

    if not data:
        raise HTTPException(status_code=400, detail=f"{APIKEY_INVALIDA}")


    if not verify_salt(password=api_key,hashed_password_from_db= data['api_key']) :
        raise HTTPException(status_code=403, detail=f"{APIKEY_INVALIDA}")

    return {"api_key": api_key, 'data': data}



@router.post('/envio-cuadre-ventas')
async def Envio_cuadre(cuadre: crearCuadreVenta, headers_validado:dict = Depends(validar_headers)):
    try:
        negocioId =headers_validado['data']['negocio_id']
        await insertar_cuadre_venta(cuadre,negocioId )

        data = await ObtenerPlayersNegocio(negocioId)

        mensaje = f'El señor@ {cuadre.nombre_completo} ha realizado un cuadre'
        if data:

            players = [player['player_id'] for player in data]

            send_push = await send_push_notification(
                heading='Notificación de Cuadre de caja',
                content=mensaje,
                player_ids=players

            )

            await RegistrarMensaje(dispostitvos=data, texto_mensaje=mensaje, id_notificacion_push=send_push['id'])

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"mensaje": f"{CUANDRE_INSERTADO}"}

        )

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'{ERROR_INTERNO_SISTEMA} - {str(e)}'
        )

@router.get('/Obtener-Cuadre-Venta/')
async def Obtener_Cuadre_Venta_Service(
    fecha_inicio: datetime = Query(..., description="Formato: YYYY-MM-DD"),
    fecha_fin: datetime = Query(..., description="Formato: YYYY-MM-DD"),
    pagina: Optional[int] = Query(1, ge=1, description="Número de página, por defecto 1"),
    my_user = Depends(decode_token)
):
    try:

        cuadre = await ObtenerCuadrePorNegocioYFechas(
            NegocioId=my_user['negocio_id'],
            FechaInicio=fecha_inicio,
            FechaFin=fecha_fin,
            pagina=pagina,

        )
        if cuadre:
            return cuadre
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró cuadre para el negocio ID {my_user['negocio_id']} entre {fecha_inicio.date()} y {fecha_fin.date()}."
            )

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ERROR_INTERNO_SISTEMA} - {str(e)}"
        )



