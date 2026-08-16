"""
proveedores/guerrilla_mail.py

Implementación del proveedor Guerrilla Mail sobre la interfaz común
ProveedorCorreoTemporal. A diferencia de mail.tm, Guerrilla Mail no usa
tokens Bearer: identifica la sesión mediante un "sid_token" que viaja como
parámetro de consulta en cada petición.
"""

import requests

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
            "password": "",  # Guerrilla Mail no usa contraseña, la sesión es el sid_token
            "proveedor": self.identificador,
            "datos_proveedor": {"sid_token": sid_token},
        }

    def refrescar_sesion(self, cuenta):
        # Guerrilla Mail extiende la sesión automáticamente con cada consulta
        # que incluya el sid_token; no requiere una renovación explícita.
        return

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
            # Guerrilla Mail incluye un mensaje de bienvenida con id "1" que
            # no es un correo real recibido; se omite de la bandeja.
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

        return MensajeCompleto(
            id_mensaje=str(m.get("mail_id", id_mensaje)),
            remitente=m.get("mail_from", "Desconocido"),
            asunto=m.get("mail_subject"),
            fecha_iso=m.get("mail_date"),
            cuerpo_texto=cuerpo,
        )
