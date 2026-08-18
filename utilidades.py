import html
import re
from datetime import datetime, timezone

PATRONES_CODIGO_POR_DEFECTO = [
    r"\b\d{4,8}\b",
    r"\b[A-Z0-9]{5,8}\b",
]

_PATRON_ETIQUETA_BLOQUE = re.compile(
    r"</?(p|div|br|li|tr|table|h[1-6]|ul|ol)\b[^>]*>", re.IGNORECASE
)
_PATRON_ETIQUETA_SCRIPT_STYLE = re.compile(
    r"<(script|style)\b.*?</\1>", re.IGNORECASE | re.DOTALL
)
_PATRON_CUALQUIER_ETIQUETA = re.compile(r"<[^>]+>")
_PATRON_LINEAS_VACIAS = re.compile(r"\n{3,}")


def html_a_texto(contenido_html):
    """Convierte un cuerpo de mensaje en HTML a texto plano legible.

    No es un parser HTML completo (no maneja HTML malformado de forma
    perfecta), pero cubre el caso habitual de correos transaccionales:
    quita <script>/<style>, convierte separadores de bloque en saltos de
    línea, elimina el resto de etiquetas y decodifica entidades HTML.
    """
    if not contenido_html:
        return ""

    texto = _PATRON_ETIQUETA_SCRIPT_STYLE.sub(" ", contenido_html)
    texto = _PATRON_ETIQUETA_BLOQUE.sub("\n", texto)
    texto = _PATRON_CUALQUIER_ETIQUETA.sub("", texto)
    texto = html.unescape(texto)
    texto = _PATRON_LINEAS_VACIAS.sub("\n\n", texto)

    lineas = [linea.strip() for linea in texto.splitlines()]
    return "\n".join(lineas).strip()


def parece_html(texto):
    if not texto:
        return False
    fragmento = texto[:500].lower()
    return "<html" in fragmento or "<body" in fragmento or bool(
        re.search(r"</?(p|div|br|table|span)\b", fragmento)
    )


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


def marca_de_tiempo_iso_actual():
    return datetime.now(timezone.utc).isoformat()


def minutos_restantes_caducidad(creado_iso, duracion_estimada_min):
    """Devuelve los minutos restantes estimados antes de que caduque una
    dirección temporal, o None si no se puede calcular (proveedor sin
    caducidad conocida, o marca de tiempo ausente/no parseable).

    Esto es SIEMPRE una estimación: los proveedores gratuitos no
    garantizan estos tiempos, pueden extenderlos con actividad, o
    cambiarlos sin aviso.
    """
    if not duracion_estimada_min or not creado_iso:
        return None
    try:
        valor_normalizado = creado_iso.replace("Z", "+00:00")
        creado = datetime.fromisoformat(valor_normalizado)
        if creado.tzinfo is None:
            creado = creado.replace(tzinfo=timezone.utc)
    except (ValueError, AttributeError):
        return None

    transcurrido_min = (datetime.now(timezone.utc) - creado).total_seconds() / 60
    restante = duracion_estimada_min - transcurrido_min
    return max(0, round(restante))
