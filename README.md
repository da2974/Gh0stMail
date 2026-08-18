from providers.base import ErrorProveedor
from providers.mail_tm import ProveedorMailTM
from providers.guerrilla_mail import ProveedorGuerrillaMail
from providers.one_sec_mail import ProveedorOneSecMail


class GestorProveedores:
    def __init__(self):
        self._proveedores = {
            "mail_tm": ProveedorMailTM(),
            "guerrilla_mail": ProveedorGuerrillaMail(),
            "one_sec_mail": ProveedorOneSecMail(),
        }
        self._orden_auto = ["mail_tm", "guerrilla_mail", "one_sec_mail"]

    def duracion_estimada_min(self, identificador):
        proveedor = self._proveedores.get(identificador)
        if proveedor is None:
            return None
        return proveedor.duracion_estimada_min

    def proveedores_disponibles(self):
        return [(pid, p.nombre_visible) for pid, p in self._proveedores.items()]

    def obtener(self, identificador):
        proveedor = self._proveedores.get(identificador)
        if proveedor is None:
            raise ErrorProveedor(f"Proveedor desconocido: {identificador}")
        return proveedor

    def crear_cuenta(self, preferencia="auto"):

        if preferencia != "auto":
            proveedor = self.obtener(preferencia)
            cuenta = proveedor.crear_cuenta()
            return cuenta, preferencia

        errores = []
        for identificador in self._orden_auto:
            proveedor = self._proveedores[identificador]
            try:
                cuenta = proveedor.crear_cuenta()
                return cuenta, identificador
            except ErrorProveedor as e:
                errores.append(f"{proveedor.nombre_visible}: {e}")
                continue

        detalle = " | ".join(errores) if errores else "no hay proveedores configurados."
        raise ErrorProveedor(f"Ningún proveedor pudo crear la cuenta. {detalle}")

    def refrescar_sesion(self, cuenta):
        proveedor = self.obtener(cuenta["proveedor"])
        proveedor.refrescar_sesion(cuenta)

    def listar_mensajes(self, cuenta):
        proveedor = self.obtener(cuenta["proveedor"])
        return proveedor.listar_mensajes(cuenta)

    def obtener_mensaje(self, cuenta, id_mensaje):
        proveedor = self.obtener(cuenta["proveedor"])
        return proveedor.obtener_mensaje(cuenta, id_mensaje)
