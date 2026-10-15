from datetime import datetime, time
import random


def is_horario_atencion() -> bool:
    """(S4) Valida si el negocio está ABIERTO (9:00 a.m. a 7:00 p.m.)"""
    now = datetime.now().time()
    apertura = time(9, 0)
    cierre = time(19, 0)
    return apertura <= now <= cierre


def generar_codigo_recuperacion() -> str:
    """(S2) Simula el envío de código por correo"""
    return str(random.randint(100000, 999999))
