from fastapi import APIRouter, HTTPException, status
from app.constants.general import ERROR_INTERNO_SISTEMA
from crud.Cuadre_crud import insertar_cuadre_venta
from schema.Cuadre_schema import CrearCuadreVenta

router = APIRouter(prefix='/Cuadre', tags=['Cuadre' ])


@router.post('/Crear-Cuadre-Venta/')
async def Crear_Cuadre_Venta_Service(
    cuadre: CrearCuadreVenta
):
    try:
        await insertar_cuadre_venta(cuadre)
        return {'details': 'OK'}

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ERROR_INTERNO_SISTEMA} - {str(e)}"
        )
