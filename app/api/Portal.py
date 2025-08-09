from http.client import HTTPResponse

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query
from starlette import status

from app.constants.general import ERROR_INTERNO_SISTEMA
from crud.portal_Crud import ObtenerNegocioAdminService, GestionApikey, ObtenerUsuarioAdminService, GestionUsuario, \
    Unlock_user, Reset_password, ver_dispositivos
from schema.Usuario_schema import PasswordUpdateRequest
from utils.Security import verificar_apy_key

router = APIRouter(prefix='/PortalAdmin', tags=['PortalAdmin'])



@router.get('/Obtener-NegocioAdmin-Servcice')
async def obtener_negocio_admin_service(
    user=Depends(verificar_apy_key),
    descripcion: str = Query(None),
    negocio_id: int = Query(None)
):
    try:
        data = await ObtenerNegocioAdminService(descripcion=descripcion, negocio_id=negocio_id)
        return data
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_INTERNO_SISTEMA
        )

@router.get('/Gestion-apkey')
async def obtener_negocio_admin_service(
    user=Depends(verificar_apy_key),
    negocio_id: int = Query(None)
):
    try:
        data = await GestionApikey(negocio_id=negocio_id)
        if data:
            return {'OK'}
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_INTERNO_SISTEMA
        )

@router.get('/Obtener-Usuario-Admin-Service')
async def obtener_usuario_admin_service(
    user=Depends(verificar_apy_key),
    nombre: str = Query(None),
    usuario_nombre: str = Query(None),
    estado: str = Query(None),
    negocio_id: int = Query(None),
    negocio: str = Query(None),
):
    try:
        data = await ObtenerUsuarioAdminService(
            nombre=nombre,
            usuario_nombre=usuario_nombre,
            estado=estado,
            negocio_id=negocio_id,
            negocio = negocio
        )
        return data
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_INTERNO_SISTEMA
        )

@router.get('/Gestion-usuario')
async def obtener_usuario_admin_service(
    user=Depends(verificar_apy_key),
    usuario_id: int = Query(None)
):
    try:
        data = await GestionUsuario(usuario_id=usuario_id)
        if data:
            return data
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_INTERNO_SISTEMA
        )

@router.get('/Desbloquear-usuario')
async def desbloquer_usuario(
    user=Depends(verificar_apy_key),
    usuario_id: int = Query(None)
):
    try:
        data = await Unlock_user(usuario_id=usuario_id)
        if data :
            return data
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_INTERNO_SISTEMA
        )

@router.get('/Resetear-usuario')
async def resetear_usuario(
    user=Depends(verificar_apy_key),
    usuario_id: int = Query(None)

):
    try:
        data = await Reset_password(usuario_id=usuario_id)
        if data:
            return data
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_INTERNO_SISTEMA
        )

@router.get('/Obtener-Dispositivo')
async def Obtener_dispositivo_services(
    user=Depends(verificar_apy_key),
    usuario_nombre: str = Query(..., description='Nombre Usuario'),
    estado: str = Query(None)

):
    try:
        data = await ver_dispositivos(
            usuario_nombre=usuario_nombre,
            estado=estado
        )
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No se encontro datos')
        return data
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ERROR_INTERNO_SISTEMA
        )