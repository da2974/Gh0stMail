"""
notificaciones.py

Envío de notificaciones de escritorio. Se apoya en QSystemTrayIcon, que
funciona de forma nativa en Windows, macOS y la mayoría de entornos Linux
sin depender de librerías adicionales.
"""


class GestorNotificaciones:
    def __init__(self, icono_bandeja):
        """icono_bandeja: instancia de QSystemTrayIcon ya creada y visible."""
        self._icono_bandeja = icono_bandeja
        self.activas = True

    def establecer_activas(self, valor):
        self.activas = bool(valor)

    def notificar(self, titulo, mensaje, duracion_ms=6000):
        if not self.activas:
            return
        if self._icono_bandeja is None:
            return
        self._icono_bandeja.showMessage(titulo, mensaje, msecs=duracion_ms)
