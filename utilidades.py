"""
utilidades.py

Funciones auxiliares independientes de la interfaz: detección de códigos
de verificación (con patrón por defecto o uno definido por el usuario),
formateo de fechas y validación de expresiones regulares.
"""

import re
from datetime import datetime

PATRONES_CODIGO_POR_DEFECTO = [
    r"\b\d{4,8}\b",
    r"\b[A-Z0-9]{5,8}\b",
]


def patron_es_valido(patron):
    if not patron:
        return True
    try:
        re.compile(patron)
        return True
    except re.error:
        return False


def extraer_codigo_verificacion(texto, patron_personalizado=""):
    if not texto:
        return None

    if patron_personalizado and patron_es_valido(patron_personalizado):
        try:
            coincidencia = re.search(patron_personalizado, texto)
        except re.error:
            coincidencia = None
        if coincidencia:
            return coincidencia.group(0)

    for patron in PATRONES_CODIGO_POR_DEFECTO:
        coincidencia = re.search(patron, texto)
        if coincidencia:
            return coincidencia.group(0)

    return None


def marca_de_tiempo_actual():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def formatear_fecha_mensaje(valor_iso):
    if not valor_iso:
        return ""
    try:
        valor_normalizado = valor_iso.replace("Z", "+00:00")
        dt = datetime.fromisoformat(valor_normalizado)
        return dt.strftime("%d/%m/%Y %H:%M")
    except (ValueError, AttributeError):
        return str(valor_iso)
