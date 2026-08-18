from abc import ABC, abstractmethod


class ErrorProveedor(Exception):
    pass


class MensajeResumen:

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

    def __init__(self, id_mensaje, remitente, asunto, fecha_iso, cuerpo_texto):
        self.id = id_mensaje
        self.remitente = remitente
        self.asunto = asunto or "(sin asunto)"
        self.fecha_iso = fecha_iso
        self.cuerpo_texto = cuerpo_texto or ""


class ProveedorCorreoTemporal(ABC):

    nombre_visible = "Proveedor"
    identificador = "base"

    # Duración estimada, en minutos, antes de que el proveedor suela
    # descartar una dirección inactiva. None = desconocida / sin límite
    # publicado. Es SIEMPRE aproximada: los proveedores gratuitos no la
    # garantizan y pueden cambiarla sin aviso.
    duracion_estimada_min = None

    @abstractmethod
    def crear_cuenta(self):
        pass

    @abstractmethod
    def refrescar_sesion(self, cuenta):
        pass

    @abstractmethod
    def listar_mensajes(self, cuenta):
        pass

    @abstractmethod
    def obtener_mensaje(self, cuenta, id_mensaje):
        pass
