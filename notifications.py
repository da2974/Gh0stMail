from PySide6.QtWidgets import QApplication


class GestorNotificaciones:
    def __init__(self, icono_bandeja):
        self._icono_bandeja = icono_bandeja
        self.activas = True
        self.sonido_activo = True

    def establecer_activas(self, valor):
        self.activas = bool(valor)

    def establecer_sonido_activo(self, valor):
        self.sonido_activo = bool(valor)

    def notificar(self, titulo, mensaje, duracion_ms=6000):
        if self.sonido_activo:
            # Aviso sonoro simple y multiplataforma vía Qt, sin depender
            # de QtMultimedia ni de archivos de audio empaquetados.
            QApplication.beep()
        if not self.activas:
            return
        if self._icono_bandeja is None:
            return
        self._icono_bandeja.showMessage(titulo, mensaje, msecs=duracion_ms)
