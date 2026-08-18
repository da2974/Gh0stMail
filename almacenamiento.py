import json
import os
import stat
import time

try:
    from cryptography.fernet import Fernet, InvalidToken
    _CIFRADO_DISPONIBLE = True
except ImportError:
    _CIFRADO_DISPONIBLE = False

NOMBRE_ARCHIVO_CUENTAS = ".correo_temporal_cuentas.json"
NOMBRE_ARCHIVO_HISTORIAL = ".correo_temporal_historial.json"
NOMBRE_ARCHIVO_CLAVE = ".correo_temporal_clave.key"

# Mensajes de advertencia acumulados durante la carga (p.ej. archivos
# corruptos que tuvieron que restaurarse a un estado vacío). main.py los
# consulta una vez al arrancar para avisar al usuario en vez de perder
# datos en silencio.
advertencias_carga = []


def _ruta(nombre_archivo):
    return os.path.join(os.path.expanduser("~"), nombre_archivo)


def _obtener_o_crear_clave():
    """Clave local para cifrar el archivo de cuentas en reposo.

    Aviso honesto sobre el alcance de esta protección: la clave se
    guarda en el mismo equipo, en un archivo con permisos restringidos
    (solo lectura/escritura para el propietario en sistemas POSIX). Esto
    protege contra la lectura casual del archivo de cuentas (por ejemplo,
    otro usuario del mismo equipo, una copia de seguridad no cifrada
    compartida por error, o un vistazo rápido al contenido) pero NO
    protege frente a alguien con acceso completo a tu cuenta de usuario
    en este equipo, que podría leer también la clave.
    """
    if not _CIFRADO_DISPONIBLE:
        return None

    ruta_clave = _ruta(NOMBRE_ARCHIVO_CLAVE)
    if os.path.exists(ruta_clave):
        try:
            with open(ruta_clave, "rb") as f:
                return f.read().strip()
        except OSError:
            return None

    clave = Fernet.generate_key()
    try:
        with open(ruta_clave, "wb") as f:
            f.write(clave)
        try:
            os.chmod(ruta_clave, stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass  # No disponible en todas las plataformas (p.ej. Windows/FAT).
    except OSError:
        return None
    return clave


def _respaldar_archivo_corrupto(ruta):
    try:
        destino = f"{ruta}.corrupto-{int(time.time())}.bak"
        os.replace(ruta, destino)
        return destino
    except OSError:
        return None


def _leer_json(ruta, valor_por_defecto):
    if not os.path.exists(ruta):
        return valor_por_defecto
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        destino = _respaldar_archivo_corrupto(ruta)
        if destino:
            advertencias_carga.append(
                f"El archivo {os.path.basename(ruta)} estaba dañado y se "
                f"restauró vacío. Se guardó una copia en {destino} por si "
                "quieres intentar recuperar algo manualmente."
            )
        else:
            advertencias_carga.append(
                f"El archivo {os.path.basename(ruta)} estaba dañado y no se "
                "pudo leer; se restauró vacío."
            )
        return valor_por_defecto


def _escribir_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def _leer_json_cifrado(ruta, valor_por_defecto):
    clave = _obtener_o_crear_clave()
    if not os.path.exists(ruta):
        return valor_por_defecto

    if not clave:
        # Sin cifrado disponible: se cae a lectura en texto plano para no
        # dejar al usuario sin poder abrir la app.
        return _leer_json(ruta, valor_por_defecto)

    try:
        with open(ruta, "rb") as f:
            contenido_cifrado = f.read()
    except OSError:
        return valor_por_defecto

    try:
        contenido = Fernet(clave).decrypt(contenido_cifrado)
        return json.loads(contenido.decode("utf-8"))
    except InvalidToken:
        try:
            # Compatibilidad con instalaciones previas donde el archivo
            # aún estaba en texto plano (versiones anteriores de la app).
            return json.loads(contenido_cifrado.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            destino = _respaldar_archivo_corrupto(ruta)
            advertencias_carga.append(
                f"No se pudo descifrar {os.path.basename(ruta)} (¿clave "
                f"perdida o archivo dañado?). Se restauró vacío"
                + (f" y se guardó una copia en {destino}." if destino else ".")
            )
            return valor_por_defecto
    except (json.JSONDecodeError, UnicodeDecodeError):
        destino = _respaldar_archivo_corrupto(ruta)
        advertencias_carga.append(
            f"El archivo {os.path.basename(ruta)} estaba dañado y se "
            f"restauró vacío" + (f" (copia en {destino})." if destino else ".")
        )
        return valor_por_defecto


def _escribir_json_cifrado(ruta, datos):
    clave = _obtener_o_crear_clave()
    contenido = json.dumps(datos, indent=2, ensure_ascii=False).encode("utf-8")
    if not clave:
        with open(ruta, "wb") as f:
            f.write(contenido)
        return
    with open(ruta, "wb") as f:
        f.write(Fernet(clave).encrypt(contenido))


def cargar_cuentas():
    return _leer_json_cifrado(_ruta(NOMBRE_ARCHIVO_CUENTAS), [])


def guardar_cuentas(cuentas):
    _escribir_json_cifrado(_ruta(NOMBRE_ARCHIVO_CUENTAS), cuentas)


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
