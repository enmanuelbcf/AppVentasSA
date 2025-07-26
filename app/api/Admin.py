from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import APIKeyHeader
from starlette import status
from typing import List


from app.constants.general import API_KEY_NAME, ERROR_INTERNO_SISTEMA, NO_DATA_FOUND
from core.config import settings
from crud.Negocio_crud import crear_negocio, verNegocios
from schema.Negocios_schema import negociosRespose
from utils.Security import verificar_apy_key

router = APIRouter(prefix='/Admin', tags=['Admin' ])
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

@router.post('/Crear-Negocio/{descricion}/{apikey}')
async def Crear_Negocio_Service(descricion, apikey, api = Depends(verificar_apy_key) ):
    try:
        data = await crear_negocio(descricion,apikey)
        return {'details': 'OK'}

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ERROR_INTERNO_SISTEMA}{str(e)}"
        )
@router.get('/Ver-Negocios', response_model=List[negociosRespose])
async def Crear_Negocio_Service(apikey=Depends(verificar_apy_key)):
    try:
        data = await verNegocios()

        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
        return data
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ERROR_INTERNO_SISTEMA}{str(e)}"
        )