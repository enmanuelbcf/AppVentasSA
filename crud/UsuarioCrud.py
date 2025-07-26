import json
from datetime import datetime

from asyncpg import UniqueViolationError
from dns.e164 import query
from fastapi import HTTPException
from starlette import status

from app.constants.general import  ERROR_INTERNO_SISTEMA, Estados
from core.Databases import db
import asyncio

from schema.Usuario_schema import UsuarioCrate
from utils.Security import  hash_password


async def ObtenerUsuarios():
    query = 'SELECT * FROM usuario'
    try:
        return await db.fetch_all(query)
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []

async def ActualizarPassword(usuario_nombre:str, nueva_password: str):
    try:
        hashed_password = hash_password(nueva_password)

        query = '''
            UPDATE usuario 
            SET password = $1 
            WHERE usuario_nombre = $2
        '''

        query_status ='''UPDATE usuario 
            SET estado = $1 
            WHERE usuario_nombre = $2'''

        await db.execute(query, hashed_password, usuario_nombre)
        await db.execute(query_status, Estados.ACTIVO, usuario_nombre)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la contraseña: {str(e)}"
        )



async def CrearUsuario(usuario: UsuarioCrate):
    try:
        query = '''
           INSERT INTO usuario (nombre, usuario_nombre, password,correo_electronico, fecha_creacion, negocio_id)
           VALUES ($1, $2, $3, $4, $5, $6)
       '''
        await db.execute(
            query,
            usuario.nombre,
            usuario.usuario_nombre,
            hash_password('12345678'),
            usuario.correo_electronico,
            datetime.now(),
            usuario.negocio_id
        )
    except UniqueViolationError as e:
        raise ValueError("Ya existe un usuario con ese correo o usuario.")
    except Exception as e:
        raise ValueError(f"{ERROR_INTERNO_SISTEMA}")

async def ObtenerUsuariosPorUSuarioNombre(UsuarioNombre:str):
    query = 'SELECT * FROM usuario where usuario_nombre = $1'
    try:
        row= await db.fetch_one(query,UsuarioNombre)
        if row:
            return dict(row)
        else:
            return None
    except Exception as e:
        raise e

async def ObtenerUsuariosPorUSuarioId(usuario_id:int):
    query = 'SELECT * FROM usuario where usuario_id = $1'
    try:
        row= await db.fetch_one(query,usuario_id)
        return row
    except Exception as e:
        raise e

async def ObtenerUsuariosPorUSuarioNombreService(UsuarioNombre:str):
    query = 'SELECT nombre , correo_electronico , usuario_nombre , estado  FROM usuario where usuario_nombre  = $1'
    try:
        row= await db.fetch_one(query,UsuarioNombre)
        return dict(row)
    except Exception as e:
        raise e