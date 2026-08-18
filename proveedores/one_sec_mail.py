import random
import string

import requests

import utilidades
from .base import (
    ProveedorCorreoTemporal,
    ErrorProveedor,
    MensajeResumen,
    MensajeCompleto,
)

API_BASE_URL = "https://www.1secmail.com/api/v1/"
TIMEOUT = 15


def _generar_cadena(longitud, alfabeto):
    return "".join(random.choice(alfabeto) for _ in range(longitud))


class ProveedorOneSecMail(ProveedorCorreoTemporal):
    nombre_visible = "1secMail"
    identificador = "one_sec_mail"
    # 1secMail no requiere ni permite renovar la dirección: los mensajes
    # simplemente dejan de estar disponibles pasado un tiempo indefinido
    # (no publicado de forma fiable), así que no se estima caducidad.
    duracion_estimada_min = None

    def __init__(self):
        self.session = requests.Session()

    def _dominios_disponibles(self):
        try:
            resp = self.session.get(
                API_BASE_URL, params={"action": "getDomainList"}, timeout=TIMEOUT
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            raise ErrorProveedor(f"1secMail no responde: {e}") from e

        dominios = resp.json()
        if not dominios:
            raise ErrorProveedor("1secMail no tiene dominios disponibles ahora mismo.")
        return dominios

    def crear_cuenta(self):
        dominios = self._dominios_disponibles()
        usuario = _generar_cadena(10, string.ascii_lowercase + string.digits)
        dominio = random.choice(dominios)
        direccion = f"{usuario}@{dominio}"

        # 1secMail no tiene endpoint de "creación"; una dirección existe
        # simplemente por recibir correos a ese buzón. No hay contraseña
        # ni token: la propia dirección hace de identificador.
        return {
            "address": direccion,
            "password": "",
            "proveedor": self.identificador,
            "datos_proveedor": {"login": usuario, "domain": dominio},
        }

    def refrescar_sesion(self, cuenta):
        return

    def listar_mensajes(self, cuenta):
        datos_proveedor = cuenta.get("datos_proveedor", {})
        login = datos_proveedor.get("login")
        dominio = datos_proveedor.get("domain")
        if not login or not dominio:
            raise ErrorProveedor("Faltan datos de la cuenta de 1secMail.")

        try:
            resp = self.session.get(
                API_BASE_URL,
                params={"action": "getMessages", "login": login, "domain": dominio},
                timeout=TIMEOUT,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            raise ErrorProveedor(f"1secMail no responde: {e}") from e

        crudos = resp.json() or []
        resultado = []
        for m in crudos:
            resultado.append(
                MensajeResumen(
                    id_mensaje=str(m.get("id")),
                    remitente=m.get("from", "Desconocido"),
                    asunto=m.get("subject"),
                    fecha_iso=m.get("date"),
                    leido=True,
                )
            )
        return resultado

    def obtener_mensaje(self, cuenta, id_mensaje):
        datos_proveedor = cuenta.get("datos_proveedor", {})
        login = datos_proveedor.get("login")
        dominio = datos_proveedor.get("domain")
        if not login or not dominio:
            raise ErrorProveedor("Faltan datos de la cuenta de 1secMail.")

        try:
            resp = self.session.get(
                API_BASE_URL,
                params={
                    "action": "readMessage",
                    "login": login,
                    "domain": dominio,
                    "id": id_mensaje,
                },
                timeout=TIMEOUT,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            raise ErrorProveedor(f"1secMail no responde: {e}") from e

        m = resp.json()
        cuerpo = m.get("textBody") or m.get("htmlBody") or ""
        if utilidades.parece_html(cuerpo):
            cuerpo = utilidades.html_a_texto(cuerpo)

        return MensajeCompleto(
            id_mensaje=str(m.get("id", id_mensaje)),
            remitente=m.get("from", "Desconocido"),
            asunto=m.get("subject"),
            fecha_iso=m.get("date"),
            cuerpo_texto=cuerpo,
        )
