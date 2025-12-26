import os
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app.api.Usaurio import router as usuario_router
from app.api.Dispositivo import router as dispositivo_router
from app.api.Admin import router as Admin_router
from app.api.Auth import router as Auth_router
from app.api.Negocio import router as Negocio_router
from app.api.Portal import router as portal_router
from app.api.Cliente import router as cliente_router
from core.Databases import db
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect(settings.DATABASE_URL)
    print("📦 Base de datos conectada")
    yield
    await db.disconnect()
    print('Base de datos desconectada')

app = FastAPI(lifespan=lifespan)

app.include_router(usuario_router)
app.include_router(dispositivo_router)
app.include_router(Admin_router)
app.include_router(Negocio_router)
app.include_router(Auth_router)
app.include_router(portal_router)
app.include_router(cliente_router)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))  # Usa PORT de Railway o 8000 por defecto local
    # uvicorn.run(app, host="192.168.100.87", port=port)
    uvicorn.run(app, host="127.0.0.1", port=port)