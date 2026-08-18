import json
import os

NOMBRE_ARCHIVO_CONFIG = ".correo_temporal_config.json"

VALORES_DEFECTO = {
    "tema": "claro",
    "idioma": "es",
    "proveedor_preferido": "auto",
    "notificaciones_activas": True,
    "minimizar_a_bandeja": True,
    "intervalo_autoactualizacion_seg": 15,
    "intervalo_espera_activa_seg": 5,
    "duracion_maxima_espera_min": 2,
    "patron_codigo_personalizado": "",
    "guardar_historial_mensajes": True,
    "auto_copiar_codigo": False,
    "sonido_activo": True,
}


def ruta_archivo_config():
    return os.path.join(os.path.expanduser("~"), NOMBRE_ARCHIVO_CONFIG)


def cargar_configuracion():
    ruta = ruta_archivo_config()
    config = dict(VALORES_DEFECTO)

    if os.path.exists(ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                guardada = json.load(f)
            if isinstance(guardada, dict):
                config.update(guardada)
        except (json.JSONDecodeError, OSError):
            pass

    return config


def guardar_configuracion(config):
    ruta = ruta_archivo_config()
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
