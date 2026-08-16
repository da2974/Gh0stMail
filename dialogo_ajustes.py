"""
dialogo_ajustes.py

Ventana modal de configuración: tema visual, proveedor preferido,
notificaciones, intervalos de tiempo y patrón de detección de código
personalizado.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QSpinBox,
    QPushButton,
    QFrame,
    QTabWidget,
)

import utilidades


def _fila_ajuste(titulo, descripcion, widget_control):
    contenedor = QFrame()
    layout = QHBoxLayout(contenedor)
    layout.setContentsMargins(0, 10, 0, 10)

    bloque_texto = QVBoxLayout()
    bloque_texto.setSpacing(2)
    etiqueta_titulo = QLabel(titulo)
    etiqueta_titulo.setObjectName("etiquetaAjusteTitulo")
    bloque_texto.addWidget(etiqueta_titulo)

    if descripcion:
        etiqueta_descripcion = QLabel(descripcion)
        etiqueta_descripcion.setObjectName("etiquetaAjusteDescripcion")
        etiqueta_descripcion.setWordWrap(True)
        bloque_texto.addWidget(etiqueta_descripcion)

    layout.addLayout(bloque_texto, stretch=1)
    layout.addWidget(widget_control, alignment=Qt.AlignVCenter)

    return contenedor


def _separador():
    linea = QFrame()
    linea.setObjectName("separadorAjustes")
    linea.setFrameShape(QFrame.HLine)
    return linea


class DialogoAjustes(QDialog):
    """Emite `ajustes_aplicados` con el dict de configuración actualizado
    cada vez que el usuario pulsa Guardar."""

    ajustes_aplicados = Signal(dict)

    def __init__(self, configuracion_actual, proveedores_disponibles, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajustes")
        self.setMinimumWidth(480)
        self.setModal(True)

        self._configuracion = dict(configuracion_actual)
        self._proveedores_disponibles = proveedores_disponibles

        self._construir_interfaz()
        self._cargar_valores_actuales()

    # ------------------------------------------------------------------

    def _construir_interfaz(self):
        layout_raiz = QVBoxLayout(self)
        layout_raiz.setContentsMargins(20, 20, 20, 16)
        layout_raiz.setSpacing(14)

        pestañas = QTabWidget()
        pestañas.addTab(self._crear_pestana_general(), "General")
        pestañas.addTab(self._crear_pestana_tiempos(), "Tiempos")
        pestañas.addTab(self._crear_pestana_avanzado(), "Avanzado")
        layout_raiz.addWidget(pestañas, stretch=1)

        fila_botones = QHBoxLayout()
        fila_botones.addStretch()

        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.setObjectName("botonSecundario")
        boton_cancelar.setCursor(Qt.PointingHandCursor)
        boton_cancelar.clicked.connect(self.reject)

        boton_guardar = QPushButton("Guardar cambios")
        boton_guardar.setObjectName("botonPrimario")
        boton_guardar.setCursor(Qt.PointingHandCursor)
        boton_guardar.clicked.connect(self._guardar)

        fila_botones.addWidget(boton_cancelar)
        fila_botones.addWidget(boton_guardar)
        layout_raiz.addLayout(fila_botones)

    def _crear_pestana_general(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(4, 12, 4, 4)
        layout.setSpacing(0)

        self.combo_tema = QComboBox()
        self.combo_tema.addItem("Claro", userData="claro")
        self.combo_tema.addItem("Oscuro", userData="oscuro")
        layout.addWidget(_fila_ajuste(
            "Tema visual", "Cambia la apariencia de toda la aplicación.", self.combo_tema
        ))
        layout.addWidget(_separador())

        self.combo_proveedor = QComboBox()
        self.combo_proveedor.addItem("Automático (recomendado)", userData="auto")
        for identificador, nombre in self._proveedores_disponibles:
            self.combo_proveedor.addItem(nombre, userData=identificador)
        layout.addWidget(_fila_ajuste(
            "Proveedor de correo",
            "En modo automático, si un proveedor falla al crear la dirección "
            "se prueba con el siguiente disponible.",
            self.combo_proveedor,
        ))
        layout.addWidget(_separador())

        self.casilla_notificaciones = QCheckBox("Activadas")
        layout.addWidget(_fila_ajuste(
            "Notificaciones de escritorio",
            "Avisa cuando llega un mensaje nuevo, aunque la ventana esté minimizada.",
            self.casilla_notificaciones,
        ))
        layout.addWidget(_separador())

        self.casilla_minimizar_bandeja = QCheckBox("Activado")
        layout.addWidget(_fila_ajuste(
            "Minimizar a la bandeja del sistema",
            "Al cerrar la ventana, la aplicación sigue activa en segundo plano.",
            self.casilla_minimizar_bandeja,
        ))
        layout.addWidget(_separador())

        self.casilla_guardar_historial = QCheckBox("Activado")
        layout.addWidget(_fila_ajuste(
            "Guardar historial de mensajes",
            "Conserva una copia local de los correos recibidos por cada dirección.",
            self.casilla_guardar_historial,
        ))

        layout.addStretch()
        return pagina

    def _crear_pestana_tiempos(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(4, 12, 4, 4)
        layout.setSpacing(0)

        self.spin_autoactualizacion = QSpinBox()
        self.spin_autoactualizacion.setRange(5, 300)
        self.spin_autoactualizacion.setSuffix(" s")
        layout.addWidget(_fila_ajuste(
            "Intervalo de autoactualización",
            "Cada cuánto se comprueba la bandeja de entrada en segundo plano.",
            self.spin_autoactualizacion,
        ))
        layout.addWidget(_separador())

        self.spin_intervalo_espera = QSpinBox()
        self.spin_intervalo_espera.setRange(2, 60)
        self.spin_intervalo_espera.setSuffix(" s")
        layout.addWidget(_fila_ajuste(
            "Frecuencia al esperar un código",
            "Cada cuánto se consulta el servidor mientras usas "
            "«Esperar mensaje nuevo».",
            self.spin_intervalo_espera,
        ))
        layout.addWidget(_separador())

        self.spin_tiempo_maximo_espera = QSpinBox()
        self.spin_tiempo_maximo_espera.setRange(1, 30)
        self.spin_tiempo_maximo_espera.setSuffix(" min")
        layout.addWidget(_fila_ajuste(
            "Tiempo máximo de espera",
            "Tras cuánto tiempo se cancela automáticamente la espera de un "
            "mensaje nuevo si no llega nada.",
            self.spin_tiempo_maximo_espera,
        ))

        layout.addStretch()
        return pagina

    def _crear_pestana_avanzado(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(4, 12, 4, 4)
        layout.setSpacing(10)

        etiqueta_titulo = QLabel("Patrón de detección de código (expresión regular)")
        etiqueta_titulo.setObjectName("etiquetaAjusteTitulo")
        layout.addWidget(etiqueta_titulo)

        etiqueta_descripcion = QLabel(
            "Opcional. Si algún servicio concreto usa un formato de código que "
            "la detección automática no reconoce bien, define aquí tu propia "
            "expresión regular. Déjalo en blanco para usar la detección estándar."
        )
        etiqueta_descripcion.setObjectName("etiquetaAjusteDescripcion")
        etiqueta_descripcion.setWordWrap(True)
        layout.addWidget(etiqueta_descripcion)

        self.campo_patron_regex = QLineEdit()
        self.campo_patron_regex.setPlaceholderText(r"Ejemplo: \b[A-Z]{3}-\d{4}\b")
        layout.addWidget(self.campo_patron_regex)

        self.etiqueta_error_regex = QLabel("")
        self.etiqueta_error_regex.setObjectName("etiquetaAjusteDescripcion")
        self.etiqueta_error_regex.setStyleSheet("color: #C82333;")
        layout.addWidget(self.etiqueta_error_regex)

        layout.addStretch()
        return pagina

    # ------------------------------------------------------------------

    def _cargar_valores_actuales(self):
        c = self._configuracion

        idx_tema = self.combo_tema.findData(c.get("tema", "claro"))
        self.combo_tema.setCurrentIndex(max(0, idx_tema))

        idx_proveedor = self.combo_proveedor.findData(c.get("proveedor_preferido", "auto"))
        self.combo_proveedor.setCurrentIndex(max(0, idx_proveedor))

        self.casilla_notificaciones.setChecked(bool(c.get("notificaciones_activas", True)))
        self.casilla_minimizar_bandeja.setChecked(bool(c.get("minimizar_a_bandeja", True)))
        self.casilla_guardar_historial.setChecked(bool(c.get("guardar_historial_mensajes", True)))

        self.spin_autoactualizacion.setValue(int(c.get("intervalo_autoactualizacion_seg", 15)))
        self.spin_intervalo_espera.setValue(int(c.get("intervalo_espera_activa_seg", 5)))
        self.spin_tiempo_maximo_espera.setValue(int(c.get("duracion_maxima_espera_min", 2)))

        self.campo_patron_regex.setText(c.get("patron_codigo_personalizado", ""))

    def _guardar(self):
        patron = self.campo_patron_regex.text().strip()
        if patron and not utilidades.patron_es_valido(patron):
            self.etiqueta_error_regex.setText(
                "Esa expresión regular no es válida. Corrígela o déjala en blanco."
            )
            return

        nueva_configuracion = {
            "tema": self.combo_tema.currentData(),
            "proveedor_preferido": self.combo_proveedor.currentData(),
            "notificaciones_activas": self.casilla_notificaciones.isChecked(),
            "minimizar_a_bandeja": self.casilla_minimizar_bandeja.isChecked(),
            "guardar_historial_mensajes": self.casilla_guardar_historial.isChecked(),
            "intervalo_autoactualizacion_seg": self.spin_autoactualizacion.value(),
            "intervalo_espera_activa_seg": self.spin_intervalo_espera.value(),
            "duracion_maxima_espera_min": self.spin_tiempo_maximo_espera.value(),
            "patron_codigo_personalizado": patron,
        }

        self.ajustes_aplicados.emit(nueva_configuracion)
        self.accept()
