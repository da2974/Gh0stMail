import requests

import utilidades
from .base import (
    ProveedorCorreoTemporal,
    ErrorProveedor,
    MensajeResumen,
    MensajeCompleto,
)

API_BASE_URL = "https://api.guerrillamail.com/ajax.php"
TIMEOUT = 15


class ProveedorGuerrillaMail(ProveedorCorreoTemporal):
    nombre_visible = "Guerrilla Mail"
    identificador = "guerrilla_mail"
    # Guerrilla Mail descarta las direcciones tras ~60 minutos de
    # inactividad. Cada consulta a la API extiende ese plazo.
    duracion_estimada_min = 60

    def __init__(self):
        self.session = requests.Session()

    def crear_cuenta(self):
        try:
            resp = self.session.get(
                API_BASE_URL, params={"f": "get_email_address"}, timeout=TIMEOUT
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            raise ErrorProveedor(f"Guerrilla Mail no responde: {e}") from e

        datos = resp.json()
        direccion = datos.get("email_addr")
        sid_token = datos.get("sid_token")
        if not direccion or not sid_token:
            raise ErrorProveedor("Guerrilla Mail no devolvió una dirección válida.")

        return {
            "address": direccion,
            "password": "",
            "proveedor": self.identificador,
            "datos_proveedor": {"sid_token": sid_token},
        }

    def refrescar_sesion(self, cuenta):
        # Guerrilla Mail no usa tokens que caduquen y deban renovarse con
        # credenciales (como mail.tm), pero SÍ descarta la dirección tras
        # ~60 min de inactividad. Volver a llamar a get_email_address con
        # el sid_token actual funciona como "keep-alive": extiende la
        # sesión y, si la dirección ya había expirado, el servidor puede
        # devolver una dirección nueva bajo el mismo sid_token.
        sid_token = cuenta.get("datos_proveedor", {}).get("sid_token", "")
        if not sid_token:
            return
        try:
            resp = self.session.get(
                API_BASE_URL,
                params={"f": "get_email_address", "sid_token": sid_token},
                timeout=TIMEOUT,
            )
            resp.raise_for_status()
        except requests.RequestException:
            # No es un fallo crítico: si la sesión expiró de verdad, la
            # siguiente llamada a listar_mensajes/obtener_mensaje fallará
            # con un error claro que sí se propaga al usuario.
            return

        datos = resp.json()
        nuevo_sid = datos.get("sid_token")
        if nuevo_sid:
            cuenta["datos_proveedor"]["sid_token"] = nuevo_sid
        # Nota: si la dirección ya había expirado, el servidor puede
        # devolver una dirección distinta bajo el mismo sid_token. No la
        # adoptamos automáticamente aquí para no desincronizar la UI y el
        # almacenamiento local a medio de una operación; si eso ocurre,
        # listar_mensajes/obtener_mensaje fallarán con un error claro.

    def listar_mensajes(self, cuenta):
        sid_token = cuenta["datos_proveedor"].get("sid_token", "")
        try:
            resp = self.session.get(
                API_BASE_URL,
                params={"f": "get_email_list", "offset": 0, "sid_token": sid_token},
                timeout=TIMEOUT,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            raise ErrorProveedor(f"Guerrilla Mail no responde: {e}") from e

        datos = resp.json()
        crudos = datos.get("list", [])
        resultado = []
        for m in crudos:
            if str(m.get("mail_id")) == "1" and "welcome" in (m.get("mail_subject") or "").lower():
                continue
            resultado.append(
                MensajeResumen(
                    id_mensaje=str(m.get("mail_id")),
                    remitente=m.get("mail_from", "Desconocido"),
                    asunto=m.get("mail_subject"),
                    fecha_iso=m.get("mail_date"),
                    leido=m.get("mail_read") not in (0, "0", None),
                )
            )
        return resultado

    def obtener_mensaje(self, cuenta, id_mensaje):
        sid_token = cuenta["datos_proveedor"].get("sid_token", "")
        try:
            resp = self.session.get(
                API_BASE_URL,
                params={"f": "fetch_email", "email_id": id_mensaje, "sid_token": sid_token},
                timeout=TIMEOUT,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            raise ErrorProveedor(f"Guerrilla Mail no responde: {e}") from e

        m = resp.json()
        cuerpo = m.get("mail_body") or m.get("mail_excerpt") or ""
        if utilidades.parece_html(cuerpo):
            cuerpo = utilidades.html_a_texto(cuerpo)

        return MensajeCompleto(
            id_mensaje=str(m.get("mail_id", id_mensaje)),
            remitente=m.get("mail_from", "Desconocido"),
            asunto=m.get("mail_subject"),
            fecha_iso=m.get("mail_date"),
            cuerpo_texto=cuerpo,
        )
