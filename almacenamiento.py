import json
import os

NOMBRE_ARCHIVO_CUENTAS = ".correo_temporal_cuentas.json"
NOMBRE_ARCHIVO_HISTORIAL = ".correo_temporal_historial.json"


def _ruta(nombre_archivo):
    return os.path.join(os.path.expanduser("~"), nombre_archivo)


def _leer_json(ruta, valor_por_defecto):
    if not os.path.exists(ruta):
        return valor_por_defecto
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return valor_por_defecto


def _escribir_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def cargar_cuentas():
    return _leer_json(_ruta(NOMBRE_ARCHIVO_CUENTAS), [])


def guardar_cuentas(cuentas):
    _escribir_json(_ruta(NOMBRE_ARCHIVO_CUENTAS), cuentas)


def cargar_historial():
    return _leer_json(_ruta(NOMBRE_ARCHIVO_HISTORIAL), {})


def guardar_historial(historial):
    _escribir_json(_ruta(NOMBRE_ARCHIVO_HISTORIAL), historial)


def registrar_mensajes_en_historial(historial, direccion, mensajes_resumen):
    entradas = historial.setdefault(direccion, [])
    ids_existentes = {e["id"] for e in entradas}

    for m in mensajes_resumen:
        if m.id not in ids_existentes:
            entradas.append(m.a_dict())

    return historial


def historial_de_direccion(historial, direccion):
    return historial.get(direccion, [])


def eliminar_historial_de_direccion(historial, direccion):
    historial.pop(direccion, None)
    return historial
