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
import idiomas
from idiomas import t


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

    ajustes_aplicados = Signal(dict)

    def __init__(self, configuracion_actual, proveedores_disponibles, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("titulo_dialogo_ajustes"))
        self.setMinimumWidth(480)
        self.setModal(True)

        self._configuracion = dict(configuracion_actual)
        self._proveedores_disponibles = proveedores_disponibles

        self._construir_interfaz()
        self._cargar_valores_actuales()


    def _construir_interfaz(self):
        layout_raiz = QVBoxLayout(self)
        layout_raiz.setContentsMargins(20, 20, 20, 16)
        layout_raiz.setSpacing(14)

        pestañas = QTabWidget()
        pestañas.addTab(self._crear_pestana_general(), t("pestana_general"))
        pestañas.addTab(self._crear_pestana_tiempos(), t("pestana_tiempos"))
        pestañas.addTab(self._crear_pestana_avanzado(), t("pestana_avanzado"))
        layout_raiz.addWidget(pestañas, stretch=1)

        fila_botones = QHBoxLayout()
        fila_botones.addStretch()

        boton_cancelar = QPushButton(t("boton_cancelar"))
        boton_cancelar.setObjectName("botonSecundario")
        boton_cancelar.setCursor(Qt.PointingHandCursor)
        boton_cancelar.clicked.connect(self.reject)

        boton_guardar = QPushButton(t("boton_guardar_cambios"))
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

        self.combo_idioma = QComboBox()
        for codigo, nombre_visible in idiomas.IDIOMAS_DISPONIBLES:
            self.combo_idioma.addItem(nombre_visible, userData=codigo)
        layout.addWidget(_fila_ajuste(
            t("ajuste_idioma_titulo"), t("ajuste_idioma_descripcion"), self.combo_idioma
        ))
        layout.addWidget(_separador())

        self.combo_tema = QComboBox()
        self.combo_tema.addItem(t("tema_claro"), userData="claro")
        self.combo_tema.addItem(t("tema_oscuro"), userData="oscuro")
        layout.addWidget(_fila_ajuste(
            t("ajuste_tema_titulo"), t("ajuste_tema_descripcion"), self.combo_tema
        ))
        layout.addWidget(_separador())

        self.combo_proveedor = QComboBox()
        self.combo_proveedor.addItem(t("proveedor_automatico"), userData="auto")
        for identificador, nombre in self._proveedores_disponibles:
            self.combo_proveedor.addItem(nombre, userData=identificador)
        layout.addWidget(_fila_ajuste(
            t("ajuste_proveedor_titulo"),
            t("ajuste_proveedor_descripcion"),
            self.combo_proveedor,
        ))
        layout.addWidget(_separador())

        self.casilla_notificaciones = QCheckBox(t("activadas"))
        layout.addWidget(_fila_ajuste(
            t("ajuste_notificaciones_titulo"),
            t("ajuste_notificaciones_descripcion"),
            self.casilla_notificaciones,
        ))
        layout.addWidget(_separador())

        self.casilla_minimizar_bandeja = QCheckBox(t("activado"))
        layout.addWidget(_fila_ajuste(
            t("ajuste_minimizar_bandeja_titulo"),
            t("ajuste_minimizar_bandeja_descripcion"),
            self.casilla_minimizar_bandeja,
        ))
        layout.addWidget(_separador())

        self.casilla_guardar_historial = QCheckBox(t("activado"))
        layout.addWidget(_fila_ajuste(
            t("ajuste_guardar_historial_titulo"),
            t("ajuste_guardar_historial_descripcion"),
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
            t("ajuste_autoactualizacion_titulo"),
            t("ajuste_autoactualizacion_descripcion"),
            self.spin_autoactualizacion,
        ))
        layout.addWidget(_separador())

        self.spin_intervalo_espera = QSpinBox()
        self.spin_intervalo_espera.setRange(2, 60)
        self.spin_intervalo_espera.setSuffix(" s")
        layout.addWidget(_fila_ajuste(
            t("ajuste_frecuencia_espera_titulo"),
            t("ajuste_frecuencia_espera_descripcion"),
            self.spin_intervalo_espera,
        ))
        layout.addWidget(_separador())

        self.spin_tiempo_maximo_espera = QSpinBox()
        self.spin_tiempo_maximo_espera.setRange(1, 30)
        self.spin_tiempo_maximo_espera.setSuffix(" min")
        layout.addWidget(_fila_ajuste(
            t("ajuste_tiempo_maximo_titulo"),
            t("ajuste_tiempo_maximo_descripcion"),
            self.spin_tiempo_maximo_espera,
        ))

        layout.addStretch()
        return pagina

    def _crear_pestana_avanzado(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(4, 12, 4, 4)
        layout.setSpacing(10)

        etiqueta_titulo = QLabel(t("ajuste_patron_titulo"))
        etiqueta_titulo.setObjectName("etiquetaAjusteTitulo")
        layout.addWidget(etiqueta_titulo)

        etiqueta_descripcion = QLabel(t("ajuste_patron_descripcion"))
        etiqueta_descripcion.setObjectName("etiquetaAjusteDescripcion")
        etiqueta_descripcion.setWordWrap(True)
        layout.addWidget(etiqueta_descripcion)

        self.campo_patron_regex = QLineEdit()
        self.campo_patron_regex.setPlaceholderText(t("ajuste_patron_placeholder"))
        layout.addWidget(self.campo_patron_regex)

        self.etiqueta_error_regex = QLabel("")
        self.etiqueta_error_regex.setObjectName("etiquetaAjusteDescripcion")
        self.etiqueta_error_regex.setStyleSheet("color: #C82333;")
        layout.addWidget(self.etiqueta_error_regex)

        layout.addStretch()
        return pagina


    def _cargar_valores_actuales(self):
        c = self._configuracion

        idx_idioma = self.combo_idioma.findData(c.get("idioma", "es"))
        self.combo_idioma.setCurrentIndex(max(0, idx_idioma))

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
            self.etiqueta_error_regex.setText(t("error_regex_invalida"))
            return

        nueva_configuracion = {
            "idioma": self.combo_idioma.currentData(),
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
