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

API_BASE_URL = "https://api.mail.tm"
TIMEOUT = 15


def _generar_cadena(longitud, alfabeto):
    return "".join(random.choice(alfabeto) for _ in range(longitud))


class ProveedorMailTM(ProveedorCorreoTemporal):
    nombre_visible = "mail.tm"
    identificador = "mail_tm"
    # mail.tm no publica una caducidad fija para sus cuentas; en la
    # práctica pueden persistir bastante tiempo. Se deja sin estimar
    # para no mostrar una cuenta atrás falsa.
    duracion_estimada_min = None

    def __init__(self):
        self.session = requests.Session()

    def _dominio_disponible(self):
        try:
            resp = self.session.get(f"{API_BASE_URL}/domains", timeout=TIMEOUT)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise ErrorProveedor(f"mail.tm no responde: {e}") from e

        dominios = resp.json().get("hydra:member", [])
        if not dominios:
            raise ErrorProveedor("mail.tm no tiene dominios disponibles ahora mismo.")
        return dominios[0]["domain"]

    def _autenticar(self, direccion, password):
        try:
            resp = self.session.post(
                f"{API_BASE_URL}/token",
                json={"address": direccion, "password": password},
                timeout=TIMEOUT,
            )
        except requests.RequestException as e:
            raise ErrorProveedor(f"mail.tm no responde: {e}") from e

        if resp.status_code == 401:
            raise ErrorProveedor("Credenciales inválidas en mail.tm.")
        resp.raise_for_status()
        return resp.json()["token"]

    def crear_cuenta(self):
        dominio = self._dominio_disponible()
        usuario = _generar_cadena(10, string.ascii_lowercase + string.digits)
        direccion = f"{usuario}@{dominio}"
        password = _generar_cadena(14, string.ascii_letters + string.digits)

        try:
            resp = self.session.post(
                f"{API_BASE_URL}/accounts",
                json={"address": direccion, "password": password},
                timeout=TIMEOUT,
            )
        except requests.RequestException as e:
            raise ErrorProveedor(f"mail.tm no responde: {e}") from e

        if resp.status_code not in (200, 201):
            raise ErrorProveedor(f"mail.tm rechazó la creación de la cuenta ({resp.status_code}).")

        token = self._autenticar(direccion, password)

        return {
            "address": direccion,
            "password": password,
            "proveedor": self.identificador,
            "datos_proveedor": {"token": token},
        }

    def refrescar_sesion(self, cuenta):
        headers = {"Authorization": f"Bearer {cuenta['datos_proveedor'].get('token', '')}"}
        try:
            resp = self.session.get(f"{API_BASE_URL}/messages", headers=headers, timeout=TIMEOUT)
        except requests.RequestException as e:
            raise ErrorProveedor(f"mail.tm no responde: {e}") from e

        if resp.status_code == 401:
            nuevo_token = self._autenticar(cuenta["address"], cuenta["password"])
            cuenta["datos_proveedor"]["token"] = nuevo_token

    def listar_mensajes(self, cuenta):
        headers = {"Authorization": f"Bearer {cuenta['datos_proveedor'].get('token', '')}"}
        try:
            resp = self.session.get(f"{API_BASE_URL}/messages", headers=headers, timeout=TIMEOUT)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise ErrorProveedor(f"mail.tm no responde: {e}") from e

        crudos = resp.json().get("hydra:member", [])
        resultado = []
        for m in crudos:
            resultado.append(
                MensajeResumen(
                    id_mensaje=m["id"],
                    remitente=m.get("from", {}).get("address", "Desconocido"),
                    asunto=m.get("subject"),
                    fecha_iso=m.get("createdAt"),
                    leido=m.get("seen", True),
                )
            )
        return resultado

    def obtener_mensaje(self, cuenta, id_mensaje):
        headers = {"Authorization": f"Bearer {cuenta['datos_proveedor'].get('token', '')}"}
        try:
            resp = self.session.get(
                f"{API_BASE_URL}/messages/{id_mensaje}", headers=headers, timeout=TIMEOUT
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            raise ErrorProveedor(f"mail.tm no responde: {e}") from e

        m = resp.json()
        cuerpo = m.get("text")
        if not cuerpo:
            partes_html = m.get("html") or []
            cuerpo = utilidades.html_a_texto("\n".join(partes_html))
        elif utilidades.parece_html(cuerpo):
            cuerpo = utilidades.html_a_texto(cuerpo)

        return MensajeCompleto(
            id_mensaje=m["id"],
            remitente=m.get("from", {}).get("address", "Desconocido"),
            asunto=m.get("subject"),
            fecha_iso=m.get("createdAt"),
            cuerpo_texto=cuerpo,
        )
