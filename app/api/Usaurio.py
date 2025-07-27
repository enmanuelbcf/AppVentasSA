from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status
from app.api.Auth import decode_token
from core.config import settings
from crud.UsuarioCrud import ObtenerUsuarios, ActualizarPassword, CrearUsuario, ObtenerUsuariosPorUSuarioNombre, \
    ObtenerUsuariosPorUSuarioNombreService
from schema.Usuario_schema import UsuarioResponse, PasswordUpdateRequest, UsuarioCrate, UsuarioResponseService
from utils.Security import verificar_apy_key

router = APIRouter(prefix='/Usuario', tags=['Usuario'])

from fastapi import HTTPException

@router.get("/ObtenerUsuario", response_model=List[UsuarioResponse])
async def Obtener_Usuarios_Service():
    try:
        data = await ObtenerUsuarios()
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron usuarios"
            )
        usuarios = [dict(row) for row in data]
        return usuarios

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
@router.patch("/Actualizar-usuario")
async def actualizar_password_service(request: PasswordUpdateRequest,
                                      user = Depends(decode_token)
                                      ):
    print(user)
    try:
        data = await ObtenerUsuariosPorUSuarioNombre(user['usuario_nombre'])

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron usuarios"
            )
        if data['estado'] == 'IN':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario Inactivo"
            )
        print(data)
        await ActualizarPassword(user['usuario_nombre'], request.nueva_password)
        return {"message": "Contraseña actualizada correctamente"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {str(e)}"
        )

@router.post('/Crear-usuario')
async def Crear_usuario_Service(usuario: UsuarioCrate, header:dict = Depends(verificar_apy_key)):
    try:
        await CrearUsuario(usuario)
        return {'datails: OK'}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {str(e)}"
        )

@router.get("/ObtenerUsuario/{usuario_name}", response_model=UsuarioResponseService)
async def Obtener_Usuarios_Por_Usuario_Nombre_Service(usuario_name):
    try:
        data = await ObtenerUsuariosPorUSuarioNombreService(usuario_name)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron usuarios"
            )
        return data

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
@router.get('Obtener-Verison-Mobil')
async def obtener_version_movil_service():
    return settings.OBTENER_VERSION_MOVIL