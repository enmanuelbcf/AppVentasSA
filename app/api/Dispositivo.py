from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.api.Auth import decode_token
from app.constants.general import ERROR_INTERNO_SISTEMA
from crud.Dispositivo_crud import insertar_dispositivo_usuario
from crud.UsuarioCrud import  ObtenerUsuariosPorUSuarioId
from schema.Dispositivo_schema import CrearDispositivoUsuario
from utils.Security import verificar_apy_key

router = APIRouter(prefix='/Dispositivo', tags=['Dispositivo' ])

@router.post('/Crear-Dispositivo/')
async def Crear_Dispositivo_Service(
    dispositivo: CrearDispositivoUsuario,
    user = Depends(decode_token)
):
    try:
        usuario =  await ObtenerUsuariosPorUSuarioId(usuario_id=user['usuario_id'])
        if usuario:
            await insertar_dispositivo_usuario(dispositivo, usuario['usuario_id'])
            return {'details': 'OK'}

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ERROR_INTERNO_SISTEMA} - {str(e)}"
        )