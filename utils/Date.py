from datetime import datetime
import pytz

def obtener_fecha_rd(formato: str = '24h') -> str:
    tz_rd = pytz.timezone('America/Santo_Domingo')
    fecha = datetime.now(tz_rd)
    return formatear_fecha(fecha, formato)

def obtener_fecha_utc(formato: str = '24h') -> str:
    fecha = datetime.utcnow().replace(tzinfo=pytz.utc)
    return formatear_fecha(fecha, formato)

def formatear_fecha(fecha: datetime, formato: str = '12h') -> str:
    if formato == '12h':
        return fecha.strftime('%Y-%m-%d %I:%M %p')  # ej: 2025-06-21 02:30 PM
    else:  # formato '24h' por defecto
        return fecha.strftime('%Y-%m-%d %H:%M')     # ej: 2025-06-21 14:30




