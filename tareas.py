"""
tareas.py

Objetos QThread que ejecutan las operaciones de red a través del gestor de
proveedores, sin bloquear el hilo principal de la interfaz. Cada tarea
emite señales Qt con el resultado o el error para que la ventana los
consuma de forma segura desde el hilo de la interfaz.
"""

import time

from PySide6.QtCore import QThread, Signal

from proveedores.base import ErrorProveedor


class TareaCrearCuenta(QThread):
    exito = Signal(dict, str)   # cuenta, identificador de proveedor usado
    error = Signal(str)

    def __init__(self, gestor_proveedores, preferencia, parent=None):
        super().__init__(parent)
        self.gestor = gestor_proveedores
        self.preferencia = preferencia

    def run(self):
        try:
            cuenta, identificador = self.gestor.crear_cuenta(self.preferencia)
        except ErrorProveedor as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"Error de conexión: {e}")
        else:
            self.exito.emit(cuenta, identificador)


class TareaListarMensajes(QThread):
    exito = Signal(list)   # lista de MensajeResumen
    error = Signal(str)

    def __init__(self, gestor_proveedores, cuenta, parent=None):
        super().__init__(parent)
        self.gestor = gestor_proveedores
        self.cuenta = cuenta

    def run(self):
        try:
            self.gestor.refrescar_sesion(self.cuenta)
            mensajes = self.gestor.listar_mensajes(self.cuenta)
        except ErrorProveedor as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"Error de conexión: {e}")
        else:
            self.exito.emit(mensajes)


class TareaObtenerMensaje(QThread):
    exito = Signal(object)   # MensajeCompleto
    error = Signal(str)

    def __init__(self, gestor_proveedores, cuenta, id_mensaje, parent=None):
        super().__init__(parent)
        self.gestor = gestor_proveedores
        self.cuenta = cuenta
        self.id_mensaje = id_mensaje

    def run(self):
        try:
            mensaje = self.gestor.obtener_mensaje(self.cuenta, self.id_mensaje)
        except ErrorProveedor as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"Error de conexión: {e}")
        else:
            self.exito.emit(mensaje)


class TareaEsperarMensajeNuevo(QThread):
    """Sondea la bandeja de entrada hasta que llega un mensaje no visto antes
    o se agota el tiempo máximo de espera."""

    exito = Signal(list, object)   # lista completa de resúmenes, nuevo (o None)
    error = Signal(str)

    def __init__(
        self,
        gestor_proveedores,
        cuenta,
        ids_conocidos,
        intervalo_seg=5,
        tiempo_maximo_seg=120,
        parent=None,
    ):
        super().__init__(parent)
        self.gestor = gestor_proveedores
        self.cuenta = cuenta
        self.ids_conocidos = set(ids_conocidos)
        self.intervalo_seg = max(2, intervalo_seg)
        self.tiempo_maximo_seg = max(self.intervalo_seg, tiempo_maximo_seg)
        self._cancelado = False

    def cancelar(self):
        self._cancelado = True

    def run(self):
        try:
            transcurrido = 0
            while transcurrido < self.tiempo_maximo_seg and not self._cancelado:
                self.gestor.refrescar_sesion(self.cuenta)
                mensajes = self.gestor.listar_mensajes(self.cuenta)
                nuevos = [m for m in mensajes if m.id not in self.ids_conocidos]
                if nuevos:
                    self.exito.emit(mensajes, nuevos[0])
                    return

                pasos = int(self.intervalo_seg * 2)
                for _ in range(pasos):
                    if self._cancelado:
                        return
                    time.sleep(0.5)
                transcurrido += self.intervalo_seg

            if not self._cancelado:
                self.exito.emit([], None)
        except ErrorProveedor as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"Error de conexión: {e}")
