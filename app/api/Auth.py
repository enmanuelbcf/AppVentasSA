from datetime import timedelta, datetime
from typing import Annotated

from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose.exceptions import JWTClaimsError
from starlette import status
from starlette.responses import JSONResponse

from app.constants.general import ERROR_INTERNO_SISTEMA
from crud.ParametroCrud import ObtenerParametro
from crud.UsuarioCrud import ObtenerUsuariosPorUSuarioNombre
from utils.Security import verify_salt

router = APIRouter(prefix='/auth', tags=['auth'])


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/obtener-token')

SECRET_KEY = "secret_access"
REFRESH_SECRET_KEY = "secret_refresh"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

@router.post('/obtener-token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:

        user = await ObtenerUsuariosPorUSuarioNombre(form_data.username)

        if not user :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No se encontro el usuario')
        if user['estado'] =='IN':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Usuaurio Inactivo')
        psd = verify_salt(form_data.password, user.get('password'))
        if not psd:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Contraseña Incorrecta')

        generar_token = {'usuario_nombre': user['usuario_nombre'], 'correo_electronico': user['correo_electronico'], 'negocio_id': user['negocio_id'], 'usuario_id': user['usuario_id']}

        access_token = crear_token(
            generar_token,
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            secret = SECRET_KEY
        )

        refersh_token = crear_token(
            generar_token,
            expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            secret=REFRESH_SECRET_KEY
        )

        return {'data': {'access_token':access_token, 'expire_acces_token': ACCESS_TOKEN_EXPIRE_MINUTES, 'refersh_token': refersh_token,'expire_refersh_token':REFRESH_TOKEN_EXPIRE_DAYS}}

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )



@router.post('/refresh')
def refresh_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token,REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        user = payload.get('usuario_nombre')

        if user is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    generar_token = payload

    new_access_token = crear_token(
        generar_token,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        secret=SECRET_KEY
    )
    return {"access_token": new_access_token, "token_type": "bearer"}


def crear_token(payload: dict, expires_delta: timedelta, secret) -> str:
    to_encode = payload.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode,secret, algorithm=ALGORITHM)




async def decode_token(token: Annotated[str, Depends(oauth2_schema)])-> dict:
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        user = await ObtenerUsuariosPorUSuarioNombre(data['usuario_nombre'])
        return user
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Endpoint protegido por token'
        )
    except JWTClaimsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Endpoint protegido por token'
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Token Invalido'
        )
@router.get("/verificar-token")
def verificar_token(my_user: Annotated[dict, Depends(decode_token)]):
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"mensaje": "Token válido", "usuario": my_user['usuario_nombre']}
        )
    except HTTPException as err:
        if err.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        raise err

@router.get('/Obtener-Parametro/')
async def Crear_Dispositivo_Service(
    nombre_parametro:str,
    user = Depends(decode_token)
):
    try:
        valor =  await ObtenerParametro(nombre_parametro=nombre_parametro)
        if valor:
            return valor

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ERROR_INTERNO_SISTEMA} - {str(e)}"
        )
