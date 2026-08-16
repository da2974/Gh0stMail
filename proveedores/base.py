"""
proveedores/base.py

Define la interfaz común que debe cumplir cualquier proveedor de correo
temporal, de forma que la aplicación pueda tratarlos de manera intercambiable
y hacer failover automático entre ellos.
"""

from abc import ABC, abstractmethod


class ErrorProveedor(Exception):
    """Error de comunicación con un proveedor de correo temporal."""


class MensajeResumen:
    """Representación normalizada de un mensaje en la lista de la bandeja."""

    def __init__(self, id_mensaje, remitente, asunto, fecha_iso, leido=True):
        self.id = id_mensaje
        self.remitente = remitente
        self.asunto = asunto or "(sin asunto)"
        self.fecha_iso = fecha_iso
        self.leido = leido

    def a_dict(self):
        return {
            "id": self.id,
            "remitente": self.remitente,
            "asunto": self.asunto,
            "fecha_iso": self.fecha_iso,
            "leido": self.leido,
        }

    @staticmethod
    def desde_dict(d):
        return MensajeResumen(
            d["id"], d["remitente"], d["asunto"], d.get("fecha_iso"), d.get("leido", True)
        )


class MensajeCompleto:
    """Representación normalizada de un mensaje con su cuerpo."""

    def __init__(self, id_mensaje, remitente, asunto, fecha_iso, cuerpo_texto):
        self.id = id_mensaje
        self.remitente = remitente
        self.asunto = asunto or "(sin asunto)"
        self.fecha_iso = fecha_iso
        self.cuerpo_texto = cuerpo_texto or ""


class ProveedorCorreoTemporal(ABC):
    """Interfaz que debe implementar cualquier proveedor de correo temporal."""

    nombre_visible = "Proveedor"
    identificador = "base"

    @abstractmethod
    def crear_cuenta(self):
        """Crea una cuenta nueva. Devuelve un dict con al menos:
        address, password, y cualquier dato interno necesario (token, etc.)
        bajo la clave 'datos_proveedor'."""

    @abstractmethod
    def refrescar_sesion(self, cuenta):
        """Renueva credenciales de sesión si el proveedor lo requiere.
        Recibe y modifica in-place el dict de la cuenta."""

    @abstractmethod
    def listar_mensajes(self, cuenta):
        """Devuelve una lista de MensajeResumen."""

    @abstractmethod
    def obtener_mensaje(self, cuenta, id_mensaje):
        """Devuelve un MensajeCompleto."""
