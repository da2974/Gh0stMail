class GestorNotificaciones:
    def __init__(self, icono_bandeja):
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
