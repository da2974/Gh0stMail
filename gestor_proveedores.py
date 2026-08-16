"""
gestor_proveedores.py

Coordina los distintos proveedores de correo temporal disponibles. Permite
elegir uno concreto o dejar que la aplicación decida automáticamente,
haciendo "failover" al siguiente proveedor de la lista si el preferido
falla al crear una cuenta nueva.

Los mensajes de una cuenta ya creada siempre se consultan con el proveedor
que la creó: el failover solo aplica al momento de crear la dirección,
no se pueden mezclar proveedores para una misma cuenta.
"""

from proveedores.base import ErrorProveedor
from proveedores.mail_tm import ProveedorMailTM
from proveedores.guerrilla_mail import ProveedorGuerrillaMail


class GestorProveedores:
    def __init__(self):
        self._proveedores = {
            "mail_tm": ProveedorMailTM(),
            "guerrilla_mail": ProveedorGuerrillaMail(),
        }
        # Orden de intento cuando el modo es "auto"
        self._orden_auto = ["mail_tm", "guerrilla_mail"]

    def proveedores_disponibles(self):
        """Lista de (identificador, nombre_visible) para mostrar en ajustes."""
        return [(pid, p.nombre_visible) for pid, p in self._proveedores.items()]

    def obtener(self, identificador):
        proveedor = self._proveedores.get(identificador)
        if proveedor is None:
            raise ErrorProveedor(f"Proveedor desconocido: {identificador}")
        return proveedor

    def crear_cuenta(self, preferencia="auto"):
        """Crea una cuenta usando el proveedor preferido; si falla y la
        preferencia es 'auto', prueba con el resto en orden.
        Devuelve (cuenta_dict, identificador_usado)."""

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
