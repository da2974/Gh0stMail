#!/usr/bin/env python3
"""
Gestor de Correo Temporal
=========================

Aplicación de escritorio para crear y administrar direcciones de correo
electrónico temporales, revisar su bandeja de entrada, localizar
automáticamente códigos de verificación recibidos y consultar el
historial de mensajes de direcciones anteriores.

Requiere:
    pip install PySide6 requests

Ejecución:
    python3 main.py
"""

import os
import sys

from PySide6.QtCore import Qt, QTimer, QSize, QPointF
from PySide6.QtGui import QFont, QIcon, QAction, QPixmap, QPainter, QColor, QPolygonF
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QFrame,
    QSplitter,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QHeaderView,
    QAbstractItemView,
    QMessageBox,
    QStatusBar,
    QSystemTrayIcon,
    QMenu,
    QFileDialog,
)

import configuracion
import almacenamiento
import utilidades
from gestor_proveedores import GestorProveedores
from proveedores.base import MensajeResumen
from notificaciones import GestorNotificaciones
from dialogo_ajustes import DialogoAjustes
from tareas import (
    TareaCrearCuenta,
    TareaListarMensajes,
    TareaObtenerMensaje,
    TareaEsperarMensajeNuevo,
)

DIRECTORIO_APP = os.path.dirname(os.path.abspath(__file__))

NOMBRES_PROVEEDOR_VISIBLE = {
    "mail_tm": "mail.tm",
    "guerrilla_mail": "Guerrilla Mail",
}


def _construir_icono_aplicacion():
    """Genera un icono simple en tiempo de ejecución (un sobre estilizado)
    para no depender de un archivo de imagen externo."""
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)

    pintor = QPainter(pixmap)
    pintor.setRenderHint(QPainter.Antialiasing)

    pintor.setBrush(QColor("#2F6FED"))
    pintor.setPen(Qt.NoPen)
    pintor.drawRoundedRect(4, 12, 56, 40, 8, 8)

    pintor.setBrush(QColor("#FFFFFF"))
    puntos = [
        (4, 16), (32, 38), (60, 16),
    ]
    poligono = QPolygonF([QPointF(x, y) for x, y in puntos])
    pintor.drawPolygon(poligono)

    pintor.end()
    return QIcon(pixmap)


# ----------------------------------------------------------------------
# Widget de fila de dirección en la lista lateral
# ----------------------------------------------------------------------

class ItemDireccion(QListWidgetItem):
    def __init__(self, cuenta):
        nombre_proveedor = NOMBRES_PROVEEDOR_VISIBLE.get(
            cuenta.get("proveedor", ""), cuenta.get("proveedor", "")
        )
        etiqueta = f"{cuenta['address']}\n{cuenta.get('creado', '')}  ·  {nombre_proveedor}"
        super().__init__(etiqueta)
        self.cuenta = cuenta
        self.setSizeHint(QSize(0, 58))


# ----------------------------------------------------------------------
# Ventana principal
# ----------------------------------------------------------------------

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Correo Temporal")
        self.resize(1200, 720)
        self.setMinimumSize(1000, 580)

        self.configuracion = configuracion.cargar_configuracion()
        self.gestor_proveedores = GestorProveedores()
        self.cuentas = almacenamiento.cargar_cuentas()
        self.historial = almacenamiento.cargar_historial()

        self.mensajes_actuales = []       # lista de MensajeResumen de la cuenta activa
        self.viendo_historial = False     # True si se está mostrando historial, no bandeja en vivo
        self.codigo_actual = None
        self.hilo_activo = None
        self.hilo_espera = None
        self._hilo_autoactualizacion = None
        self._salir_solicitado = False

        self._icono_app = _construir_icono_aplicacion()
        self.setWindowIcon(self._icono_app)

        self._construir_bandeja_sistema()
        self.notificador = GestorNotificaciones(self.icono_bandeja)
        self.notificador.establecer_activas(self.configuracion["notificaciones_activas"])

        self._construir_interfaz()
        self._aplicar_tema(self.configuracion["tema"])
        self._poblar_lista_cuentas()

        self.temporizador = QTimer(self)
        self.temporizador.timeout.connect(self._autoactualizar_silencioso)
        self.temporizador.start(self.configuracion["intervalo_autoactualizacion_seg"] * 1000)

    # ------------------------------------------------------------------
    # Bandeja del sistema
    # ------------------------------------------------------------------

    def _construir_bandeja_sistema(self):
        self.icono_bandeja = QSystemTrayIcon(self._icono_app, self)
        self.icono_bandeja.setToolTip("Gestor de Correo Temporal")

        menu = QMenu()
        accion_mostrar = QAction("Mostrar ventana", self)
        accion_mostrar.triggered.connect(self._mostrar_desde_bandeja)
        accion_salir = QAction("Salir", self)
        accion_salir.triggered.connect(self._salir_completamente)

        menu.addAction(accion_mostrar)
        menu.addSeparator()
        menu.addAction(accion_salir)

        self.icono_bandeja.setContextMenu(menu)
        self.icono_bandeja.activated.connect(self._al_activar_icono_bandeja)
        self.icono_bandeja.show()

    def _al_activar_icono_bandeja(self, motivo):
        if motivo == QSystemTrayIcon.Trigger:
            self._mostrar_desde_bandeja()

    def _mostrar_desde_bandeja(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def _salir_completamente(self):
        self._salir_solicitado = True
        self.close()

    # ------------------------------------------------------------------
    # Construcción de la interfaz
    # ------------------------------------------------------------------

    def _construir_interfaz(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout_raiz = QVBoxLayout(widget_central)
        layout_raiz.setContentsMargins(0, 0, 0, 0)
        layout_raiz.setSpacing(0)

        layout_raiz.addWidget(self._crear_barra_superior())

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)

        panel_izquierdo = self._crear_panel_direcciones()
        panel_derecho = self._crear_panel_mensajes()

        splitter.addWidget(panel_izquierdo)
        splitter.addWidget(panel_derecho)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([360, 840])

        contenedor_splitter = QWidget()
        layout_contenedor = QHBoxLayout(contenedor_splitter)
        layout_contenedor.setContentsMargins(16, 16, 16, 16)
        layout_contenedor.addWidget(splitter)

        layout_raiz.addWidget(contenedor_splitter, stretch=1)

        self.barra_estado = QStatusBar()
        self.setStatusBar(self.barra_estado)
        self.barra_estado.showMessage("Listo.")

    def _crear_barra_superior(self):
        barra = QFrame()
        barra.setObjectName("barraSuperior")
        barra.setFixedHeight(64)

        layout = QHBoxLayout(barra)
        layout.setContentsMargins(20, 8, 20, 8)

        bloque_titulos = QVBoxLayout()
        bloque_titulos.setSpacing(0)

        titulo = QLabel("Gestor de Correo Temporal")
        titulo.setObjectName("tituloApp")
        subtitulo = QLabel("Direcciones desechables para verificaciones y registros puntuales")
        subtitulo.setObjectName("subtituloApp")

        bloque_titulos.addWidget(titulo)
        bloque_titulos.addWidget(subtitulo)

        layout.addLayout(bloque_titulos)
        layout.addStretch()

        self.boton_ajustes = QPushButton("⚙  Ajustes")
        self.boton_ajustes.setObjectName("botonSecundario")
        self.boton_ajustes.setCursor(Qt.PointingHandCursor)
        self.boton_ajustes.clicked.connect(self._abrir_ajustes)
        layout.addWidget(self.boton_ajustes)

        return barra

    def _crear_panel_direcciones(self):
        panel = QFrame()
        panel.setObjectName("panelTarjeta")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        fila_encabezado = QHBoxLayout()
        encabezado = QLabel("DIRECCIONES CREADAS")
        encabezado.setObjectName("encabezadoPanel")
        fila_encabezado.addWidget(encabezado)
        fila_encabezado.addStretch()
        layout.addLayout(fila_encabezado)

        self.boton_nueva_direccion = QPushButton("＋  Nueva dirección")
        self.boton_nueva_direccion.setObjectName("botonPrimario")
        self.boton_nueva_direccion.setCursor(Qt.PointingHandCursor)
        self.boton_nueva_direccion.clicked.connect(self._accion_crear_cuenta)
        layout.addWidget(self.boton_nueva_direccion)

        self.campo_busqueda_direcciones = QLineEdit()
        self.campo_busqueda_direcciones.setPlaceholderText("Buscar dirección…")
        self.campo_busqueda_direcciones.textChanged.connect(self._filtrar_lista_direcciones)
        layout.addWidget(self.campo_busqueda_direcciones)

        self.lista_direcciones = QListWidget()
        self.lista_direcciones.setSelectionMode(QAbstractItemView.SingleSelection)
        self.lista_direcciones.currentItemChanged.connect(self._al_seleccionar_cuenta)
        layout.addWidget(self.lista_direcciones, stretch=1)

        self.campo_direccion_actual = QLineEdit()
        self.campo_direccion_actual.setReadOnly(True)
        self.campo_direccion_actual.setPlaceholderText("Selecciona o crea una dirección")
        self.campo_direccion_actual.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.campo_direccion_actual)

        fila_botones_pie = QHBoxLayout()
        self.boton_copiar_direccion = QPushButton("Copiar")
        self.boton_copiar_direccion.setObjectName("botonSecundario")
        self.boton_copiar_direccion.setCursor(Qt.PointingHandCursor)
        self.boton_copiar_direccion.clicked.connect(self._accion_copiar_direccion)

        self.boton_exportar_cuenta = QPushButton("Exportar")
        self.boton_exportar_cuenta.setObjectName("botonSecundario")
        self.boton_exportar_cuenta.setCursor(Qt.PointingHandCursor)
        self.boton_exportar_cuenta.clicked.connect(self._accion_exportar_cuenta)

        self.boton_eliminar_direccion = QPushButton("Eliminar")
        self.boton_eliminar_direccion.setObjectName("botonPeligro")
        self.boton_eliminar_direccion.setCursor(Qt.PointingHandCursor)
        self.boton_eliminar_direccion.clicked.connect(self._accion_eliminar_cuenta)

        fila_botones_pie.addWidget(self.boton_copiar_direccion)
        fila_botones_pie.addWidget(self.boton_exportar_cuenta)
        fila_botones_pie.addWidget(self.boton_eliminar_direccion)
        layout.addLayout(fila_botones_pie)

        return panel

    def _crear_panel_mensajes(self):
        panel = QFrame()
        panel.setObjectName("panelTarjeta")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        fila_encabezado = QHBoxLayout()
        self.etiqueta_encabezado_bandeja = QLabel("BANDEJA DE ENTRADA")
        self.etiqueta_encabezado_bandeja.setObjectName("encabezadoPanel")
        fila_encabezado.addWidget(self.etiqueta_encabezado_bandeja)
        fila_encabezado.addStretch()

        self.boton_ver_historial = QPushButton("Ver historial")
        self.boton_ver_historial.setObjectName("botonSecundario")
        self.boton_ver_historial.setCursor(Qt.PointingHandCursor)
        self.boton_ver_historial.setCheckable(True)
        self.boton_ver_historial.clicked.connect(self._alternar_vista_historial)

        self.boton_actualizar = QPushButton("Actualizar")
        self.boton_actualizar.setObjectName("botonSecundario")
        self.boton_actualizar.setCursor(Qt.PointingHandCursor)
        self.boton_actualizar.clicked.connect(self._accion_actualizar_mensajes)

        self.boton_esperar_codigo = QPushButton("Esperar mensaje nuevo")
        self.boton_esperar_codigo.setObjectName("botonPrimario")
        self.boton_esperar_codigo.setCursor(Qt.PointingHandCursor)
        self.boton_esperar_codigo.clicked.connect(self._accion_esperar_codigo)

        fila_encabezado.addWidget(self.boton_ver_historial)
        fila_encabezado.addWidget(self.boton_actualizar)
        fila_encabezado.addWidget(self.boton_esperar_codigo)
        layout.addLayout(fila_encabezado)

        self.campo_busqueda_mensajes = QLineEdit()
        self.campo_busqueda_mensajes.setPlaceholderText("Buscar por remitente o asunto…")
        self.campo_busqueda_mensajes.textChanged.connect(self._filtrar_tabla_mensajes)
        layout.addWidget(self.campo_busqueda_mensajes)

        self.pila_bandeja = QStackedWidget()

        self.pagina_vacia = self._crear_pagina_vacia()
        self.pila_bandeja.addWidget(self.pagina_vacia)

        splitter_vertical = QSplitter(Qt.Vertical)

        self.tabla_mensajes = QTableWidget(0, 3)
        self.tabla_mensajes.setHorizontalHeaderLabels(["Remitente", "Asunto", "Recibido"])
        self.tabla_mensajes.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tabla_mensajes.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla_mensajes.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tabla_mensajes.verticalHeader().setVisible(False)
        self.tabla_mensajes.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_mensajes.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabla_mensajes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_mensajes.itemSelectionChanged.connect(self._al_seleccionar_mensaje)

        panel_detalle = QWidget()
        layout_detalle = QVBoxLayout(panel_detalle)
        layout_detalle.setContentsMargins(0, 8, 0, 0)
        layout_detalle.setSpacing(8)

        self.tarjeta_codigo = self._crear_tarjeta_codigo()
        self.tarjeta_codigo.hide()
        layout_detalle.addWidget(self.tarjeta_codigo)

        self.texto_cuerpo = QTextEdit()
        self.texto_cuerpo.setReadOnly(True)
        layout_detalle.addWidget(self.texto_cuerpo, stretch=1)

        splitter_vertical.addWidget(self.tabla_mensajes)
        splitter_vertical.addWidget(panel_detalle)
        splitter_vertical.setStretchFactor(0, 3)
        splitter_vertical.setStretchFactor(1, 2)

        self.pila_bandeja.addWidget(splitter_vertical)
        layout.addWidget(self.pila_bandeja, stretch=1)

        self.pila_bandeja.setCurrentWidget(self.pagina_vacia)

        return panel

    def _crear_pagina_vacia(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(6)

        titulo = QLabel("Ninguna dirección seleccionada")
        titulo.setObjectName("estadoVacioTitulo")
        titulo.setAlignment(Qt.AlignCenter)

        texto = QLabel("Crea o selecciona una dirección de la izquierda\npara ver su bandeja de entrada.")
        texto.setObjectName("estadoVacioTexto")
        texto.setAlignment(Qt.AlignCenter)

        layout.addWidget(titulo)
        layout.addWidget(texto)
        return pagina

    def _crear_tarjeta_codigo(self):
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjetaCodigo")
        layout = QHBoxLayout(tarjeta)
        layout.setContentsMargins(14, 10, 14, 10)

        bloque_texto = QVBoxLayout()
        bloque_texto.setSpacing(2)
        titulo = QLabel("CÓDIGO DETECTADO")
        titulo.setObjectName("etiquetaCodigoTitulo")
        self.etiqueta_valor_codigo = QLabel("")
        self.etiqueta_valor_codigo.setObjectName("etiquetaCodigo")

        bloque_texto.addWidget(titulo)
        bloque_texto.addWidget(self.etiqueta_valor_codigo)

        layout.addLayout(bloque_texto)
        layout.addStretch()

        self.boton_copiar_codigo = QPushButton("Copiar código")
        self.boton_copiar_codigo.setObjectName("botonSecundario")
        self.boton_copiar_codigo.setCursor(Qt.PointingHandCursor)
        self.boton_copiar_codigo.clicked.connect(self._accion_copiar_codigo)
        layout.addWidget(self.boton_copiar_codigo, alignment=Qt.AlignVCenter)

        return tarjeta

    # ------------------------------------------------------------------
    # Utilidades de estado y tema
    # ------------------------------------------------------------------

    def _fijar_estado(self, mensaje, tiempo_ms=5000):
        self.barra_estado.showMessage(mensaje, tiempo_ms)

    def _cuenta_actual(self):
        item = self.lista_direcciones.currentItem()
        if item is None:
            return None
        return item.cuenta

    def _mostrar_error(self, titulo, mensaje):
        QMessageBox.critical(self, titulo, mensaje)

    def _aplicar_tema(self, nombre_tema):
        nombre_archivo = "tema_oscuro.qss" if nombre_tema == "oscuro" else "tema_claro.qss"
        ruta = os.path.join(DIRECTORIO_APP, nombre_archivo)
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except OSError:
            pass

    def _filtrar_lista_direcciones(self, texto):
        texto = texto.strip().lower()
        for i in range(self.lista_direcciones.count()):
            item = self.lista_direcciones.item(i)
            visible = texto in item.cuenta["address"].lower()
            item.setHidden(not visible)

    def _filtrar_tabla_mensajes(self, texto):
        texto = texto.strip().lower()
        for fila in range(self.tabla_mensajes.rowCount()):
            item_remitente = self.tabla_mensajes.item(fila, 0)
            item_asunto = self.tabla_mensajes.item(fila, 1)
            contenido = f"{item_remitente.text()} {item_asunto.text()}".lower()
            self.tabla_mensajes.setRowHidden(fila, texto not in contenido)

    # ------------------------------------------------------------------
    # Lista de direcciones
    # ------------------------------------------------------------------

    def _poblar_lista_cuentas(self):
        self.lista_direcciones.blockSignals(True)
        self.lista_direcciones.clear()
        for cuenta in self.cuentas:
            self.lista_direcciones.addItem(ItemDireccion(cuenta))
        self.lista_direcciones.blockSignals(False)

    def _al_seleccionar_cuenta(self, actual, _anterior):
        self.boton_ver_historial.setChecked(False)
        self.viendo_historial = False

        if actual is None:
            self.pila_bandeja.setCurrentWidget(self.pagina_vacia)
            self.campo_direccion_actual.clear()
            return

        cuenta = actual.cuenta
        self.campo_direccion_actual.setText(cuenta["address"])
        self._ocultar_codigo()
        self.texto_cuerpo.clear()
        self.campo_busqueda_mensajes.clear()
        self._accion_actualizar_mensajes()

    def _accion_crear_cuenta(self):
        self.boton_nueva_direccion.setEnabled(False)
        self.boton_nueva_direccion.setText("Creando dirección…")
        self._fijar_estado("Creando una nueva dirección de correo…")

        preferencia = self.configuracion.get("proveedor_preferido", "auto")
        self.hilo_activo = TareaCrearCuenta(self.gestor_proveedores, preferencia)
        self.hilo_activo.exito.connect(self._al_crear_cuenta_exito)
        self.hilo_activo.error.connect(self._al_crear_cuenta_error)
        self.hilo_activo.start()

    def _al_crear_cuenta_exito(self, datos_cuenta, identificador_proveedor):
        datos_cuenta["proveedor"] = identificador_proveedor
        datos_cuenta["creado"] = utilidades.marca_de_tiempo_actual()
        self.cuentas.append(datos_cuenta)
        almacenamiento.guardar_cuentas(self.cuentas)

        item = ItemDireccion(datos_cuenta)
        self.lista_direcciones.addItem(item)
        self.lista_direcciones.setCurrentItem(item)

        self.boton_nueva_direccion.setEnabled(True)
        self.boton_nueva_direccion.setText("＋  Nueva dirección")

        nombre_proveedor = NOMBRES_PROVEEDOR_VISIBLE.get(identificador_proveedor, identificador_proveedor)
        self._fijar_estado(f"Dirección creada con {nombre_proveedor}: {datos_cuenta['address']}")

    def _al_crear_cuenta_error(self, mensaje):
        self.boton_nueva_direccion.setEnabled(True)
        self.boton_nueva_direccion.setText("＋  Nueva dirección")
        self._fijar_estado("No se pudo crear la dirección.")
        self._mostrar_error("Gestor de Correo Temporal", f"No se pudo crear la dirección.\n\n{mensaje}")

    def _accion_eliminar_cuenta(self):
        cuenta = self._cuenta_actual()
        if cuenta is None:
            QMessageBox.information(
                self, "Gestor de Correo Temporal", "Selecciona primero una dirección de la lista."
            )
            return

        respuesta = QMessageBox.question(
            self,
            "Eliminar dirección",
            f"¿Quitar «{cuenta['address']}» de la lista?\n\n"
            "Esto solo elimina el registro local; la cuenta puede seguir "
            "existiendo en el proveedor. El historial de mensajes de esta "
            "dirección también se eliminará.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if respuesta != QMessageBox.Yes:
            return

        fila = self.lista_direcciones.currentRow()
        self.cuentas.pop(fila)
        almacenamiento.guardar_cuentas(self.cuentas)
        almacenamiento.eliminar_historial_de_direccion(self.historial, cuenta["address"])
        almacenamiento.guardar_historial(self.historial)

        self.lista_direcciones.takeItem(fila)

        self.mensajes_actuales = []
        self.texto_cuerpo.clear()
        self._ocultar_codigo()
        self.campo_direccion_actual.clear()
        self.pila_bandeja.setCurrentWidget(self.pagina_vacia)

        self._fijar_estado("Dirección eliminada de la lista local.")

    def _accion_copiar_direccion(self):
        cuenta = self._cuenta_actual()
        if cuenta is None:
            return
        QApplication.clipboard().setText(cuenta["address"])
        self._fijar_estado("Dirección copiada al portapapeles.")

    def _accion_exportar_cuenta(self):
        cuenta = self._cuenta_actual()
        if cuenta is None:
            QMessageBox.information(
                self, "Gestor de Correo Temporal", "Selecciona primero una dirección de la lista."
            )
            return

        nombre_sugerido = cuenta["address"].replace("@", "_at_") + ".txt"
        ruta_destino, _ = QFileDialog.getSaveFileName(
            self, "Exportar dirección", nombre_sugerido, "Archivos de texto (*.txt)"
        )
        if not ruta_destino:
            return

        nombre_proveedor = NOMBRES_PROVEEDOR_VISIBLE.get(cuenta.get("proveedor", ""), "Desconocido")
        contenido = (
            f"Dirección:  {cuenta['address']}\n"
            f"Contraseña: {cuenta.get('password') or '(este proveedor no usa contraseña)'}\n"
            f"Proveedor:  {nombre_proveedor}\n"
            f"Creada:     {cuenta.get('creado', '')}\n"
        )

        try:
            with open(ruta_destino, "w", encoding="utf-8") as f:
                f.write(contenido)
        except OSError as e:
            self._mostrar_error("Gestor de Correo Temporal", f"No se pudo guardar el archivo.\n\n{e}")
            return

        self._fijar_estado("Dirección exportada correctamente.")

    # ------------------------------------------------------------------
    # Mensajes — bandeja en vivo
    # ------------------------------------------------------------------

    def _accion_actualizar_mensajes(self):
        cuenta = self._cuenta_actual()
        if cuenta is None:
            return

        self.boton_ver_historial.setChecked(False)
        self.viendo_historial = False
        self.etiqueta_encabezado_bandeja.setText("BANDEJA DE ENTRADA")

        self._fijar_estado("Consultando bandeja de entrada…")
        self.boton_actualizar.setEnabled(False)

        self.hilo_activo = TareaListarMensajes(self.gestor_proveedores, cuenta)
        self.hilo_activo.exito.connect(self._al_listar_mensajes_exito)
        self.hilo_activo.error.connect(self._al_listar_mensajes_error)
        self.hilo_activo.start()

    def _al_listar_mensajes_exito(self, mensajes):
        self.boton_actualizar.setEnabled(True)
        self.mensajes_actuales = mensajes
        self._refrescar_tabla_mensajes()
        self._registrar_en_historial_si_procede()

        if mensajes:
            self.pila_bandeja.setCurrentIndex(1)
            self._fijar_estado(f"{len(mensajes)} mensaje(s) en la bandeja.")
        else:
            self._fijar_estado("La bandeja está vacía por ahora.")

    def _al_listar_mensajes_error(self, mensaje):
        self.boton_actualizar.setEnabled(True)
        self._fijar_estado("No se pudo actualizar la bandeja de entrada.")

    def _refrescar_tabla_mensajes(self):
        self.tabla_mensajes.setRowCount(0)
        for mensaje in self.mensajes_actuales:
            fila = self.tabla_mensajes.rowCount()
            self.tabla_mensajes.insertRow(fila)

            remitente = mensaje.remitente
            asunto = mensaje.asunto
            fecha = utilidades.formatear_fecha_mensaje(mensaje.fecha_iso)

            self.tabla_mensajes.setItem(fila, 0, QTableWidgetItem(remitente))
            self.tabla_mensajes.setItem(fila, 1, QTableWidgetItem(asunto))
            self.tabla_mensajes.setItem(fila, 2, QTableWidgetItem(fecha))

        if self.campo_busqueda_mensajes.text():
            self._filtrar_tabla_mensajes(self.campo_busqueda_mensajes.text())

    def _registrar_en_historial_si_procede(self):
        if not self.configuracion.get("guardar_historial_mensajes", True):
            return
        cuenta = self._cuenta_actual()
        if cuenta is None:
            return
        almacenamiento.registrar_mensajes_en_historial(
            self.historial, cuenta["address"], self.mensajes_actuales
        )
        almacenamiento.guardar_historial(self.historial)

    def _al_seleccionar_mensaje(self):
        filas = self.tabla_mensajes.selectionModel().selectedRows()
        if not filas:
            return
        idx = filas[0].row()
        if idx >= len(self.mensajes_actuales):
            return

        mensaje_resumen = self.mensajes_actuales[idx]

        if self.viendo_historial:
            self._mostrar_mensaje_de_historial(mensaje_resumen)
            return

        cuenta = self._cuenta_actual()
        if cuenta is None:
            return

        self._fijar_estado("Cargando mensaje…")

        self.hilo_activo = TareaObtenerMensaje(self.gestor_proveedores, cuenta, mensaje_resumen.id)
        self.hilo_activo.exito.connect(self._al_obtener_mensaje_exito)
        self.hilo_activo.error.connect(self._al_obtener_mensaje_error)
        self.hilo_activo.start()

    def _al_obtener_mensaje_exito(self, mensaje_completo):
        self.texto_cuerpo.setPlainText(mensaje_completo.cuerpo_texto.strip())
        self._detectar_y_mostrar_codigo(mensaje_completo.asunto, mensaje_completo.cuerpo_texto)
        self._fijar_estado("Mensaje cargado.")

    def _al_obtener_mensaje_error(self, mensaje):
        self._fijar_estado("No se pudo cargar el contenido del mensaje.")

    def _detectar_y_mostrar_codigo(self, asunto, cuerpo):
        patron_personalizado = self.configuracion.get("patron_codigo_personalizado", "")
        codigo = utilidades.extraer_codigo_verificacion(
            f"{asunto} {cuerpo}", patron_personalizado
        )
        if codigo:
            self._mostrar_codigo(codigo)
        else:
            self._ocultar_codigo()

    def _mostrar_codigo(self, codigo):
        self.codigo_actual = codigo
        self.etiqueta_valor_codigo.setText(codigo)
        self.tarjeta_codigo.show()

    def _ocultar_codigo(self):
        self.codigo_actual = None
        self.tarjeta_codigo.hide()

    def _accion_copiar_codigo(self):
        if not self.codigo_actual:
            return
        QApplication.clipboard().setText(self.codigo_actual)
        self._fijar_estado("Código copiado al portapapeles.")

    # ------------------------------------------------------------------
    # Historial de mensajes
    # ------------------------------------------------------------------

    def _alternar_vista_historial(self, activo):
        cuenta = self._cuenta_actual()
        if cuenta is None:
            self.boton_ver_historial.setChecked(False)
            return

        self.viendo_historial = activo
        self.texto_cuerpo.clear()
        self._ocultar_codigo()
        self.campo_busqueda_mensajes.clear()

        if activo:
            self.etiqueta_encabezado_bandeja.setText("HISTORIAL DE MENSAJES")
            entradas = almacenamiento.historial_de_direccion(self.historial, cuenta["address"])
            self.mensajes_actuales = [MensajeResumen.desde_dict(e) for e in entradas]
            self._refrescar_tabla_mensajes()
            self.pila_bandeja.setCurrentIndex(1 if self.mensajes_actuales else 0)
            if not self.mensajes_actuales:
                self._fijar_estado("Todavía no hay historial guardado para esta dirección.")
            else:
                self._fijar_estado(f"Mostrando {len(self.mensajes_actuales)} mensaje(s) del historial.")
        else:
            self.etiqueta_encabezado_bandeja.setText("BANDEJA DE ENTRADA")
            self._accion_actualizar_mensajes()

    def _mostrar_mensaje_de_historial(self, mensaje_resumen):
        # El historial solo guarda el resumen (remitente/asunto/fecha), no el
        # cuerpo completo, para no duplicar el almacenamiento del proveedor.
        self.texto_cuerpo.setPlainText(
            "Este mensaje procede del historial local y solo conserva el "
            "remitente, el asunto y la fecha; el proveedor no expone su "
            "cuerpo completo una vez ha sido archivado.\n\n"
            f"Remitente: {mensaje_resumen.remitente}\n"
            f"Asunto: {mensaje_resumen.asunto}"
        )
        self._detectar_y_mostrar_codigo(mensaje_resumen.asunto, "")

    # ------------------------------------------------------------------
    # Espera activa de un mensaje nuevo
    # ------------------------------------------------------------------

    def _accion_esperar_codigo(self):
        cuenta = self._cuenta_actual()
        if cuenta is None:
            QMessageBox.information(self, "Gestor de Correo Temporal", "Selecciona primero una dirección.")
            return

        if self.viendo_historial:
            QMessageBox.information(
                self,
                "Gestor de Correo Temporal",
                "Sal de la vista de historial para poder esperar un mensaje nuevo.",
            )
            return

        if self.hilo_espera is not None and self.hilo_espera.isRunning():
            return

        ids_conocidos = {m.id for m in self.mensajes_actuales}

        self.boton_esperar_codigo.setEnabled(False)
        self.boton_esperar_codigo.setText("Esperando mensaje nuevo…")
        self._fijar_estado("Esperando un mensaje nuevo para detectar el código automáticamente…", 0)

        intervalo = self.configuracion.get("intervalo_espera_activa_seg", 5)
        tiempo_maximo = self.configuracion.get("duracion_maxima_espera_min", 2) * 60

        self.hilo_espera = TareaEsperarMensajeNuevo(
            self.gestor_proveedores, cuenta, ids_conocidos, intervalo, tiempo_maximo
        )
        self.hilo_espera.exito.connect(self._al_esperar_codigo_exito)
        self.hilo_espera.error.connect(self._al_esperar_codigo_error)
        self.hilo_espera.start()

    def _al_esperar_codigo_exito(self, mensajes, nuevo):
        self.boton_esperar_codigo.setEnabled(True)
        self.boton_esperar_codigo.setText("Esperar mensaje nuevo")

        if not nuevo:
            self._fijar_estado("No llegó ningún mensaje nuevo en el tiempo de espera.")
            return

        self.mensajes_actuales = mensajes
        self._refrescar_tabla_mensajes()
        self._registrar_en_historial_si_procede()
        self.pila_bandeja.setCurrentIndex(1)

        for i, m in enumerate(mensajes):
            if m.id == nuevo.id:
                self.tabla_mensajes.selectRow(i)
                self.tabla_mensajes.scrollToItem(self.tabla_mensajes.item(i, 0))
                break

        self._fijar_estado("Ha llegado un mensaje nuevo.")
        self.notificador.notificar(
            "Nuevo mensaje recibido",
            f"De: {nuevo.remitente}\n{nuevo.asunto}",
        )

    def _al_esperar_codigo_error(self, mensaje):
        self.boton_esperar_codigo.setEnabled(True)
        self.boton_esperar_codigo.setText("Esperar mensaje nuevo")
        self._fijar_estado("Se detuvo la espera por un error de conexión.")

    # ------------------------------------------------------------------
    # Autoactualización periódica en segundo plano
    # ------------------------------------------------------------------

    def _autoactualizar_silencioso(self):
        cuenta = self._cuenta_actual()
        if cuenta is None or self.viendo_historial:
            return
        if self.hilo_espera is not None and self.hilo_espera.isRunning():
            return

        hilo = TareaListarMensajes(self.gestor_proveedores, cuenta)
        hilo.exito.connect(self._al_autoactualizar_exito)
        hilo.error.connect(lambda _m: None)
        hilo.start()
        self._hilo_autoactualizacion = hilo  # referencia para evitar recolección prematura

    def _al_autoactualizar_exito(self, mensajes):
        ids_antes = {m.id for m in self.mensajes_actuales}
        ids_despues = {m.id for m in mensajes}

        if ids_despues != ids_antes:
            nuevos = [m for m in mensajes if m.id not in ids_antes]

            self.mensajes_actuales = mensajes
            self._refrescar_tabla_mensajes()
            self._registrar_en_historial_si_procede()
            if mensajes:
                self.pila_bandeja.setCurrentIndex(1)
            self._fijar_estado("Bandeja de entrada actualizada.")

            if nuevos:
                primero = nuevos[0]
                extra = f" (+{len(nuevos) - 1} más)" if len(nuevos) > 1 else ""
                self.notificador.notificar(
                    "Nuevo mensaje recibido",
                    f"De: {primero.remitente}\n{primero.asunto}{extra}",
                )

    # ------------------------------------------------------------------
    # Ajustes
    # ------------------------------------------------------------------

    def _abrir_ajustes(self):
        dialogo = DialogoAjustes(
            self.configuracion,
            self.gestor_proveedores.proveedores_disponibles(),
            parent=self,
        )
        dialogo.ajustes_aplicados.connect(self._al_aplicar_ajustes)
        dialogo.exec()

    def _al_aplicar_ajustes(self, nueva_configuracion):
        tema_cambio = nueva_configuracion["tema"] != self.configuracion.get("tema")
        nuevo_intervalo_ms = nueva_configuracion["intervalo_autoactualizacion_seg"] * 1000

        self.configuracion = nueva_configuracion
        configuracion.guardar_configuracion(self.configuracion)

        self.notificador.establecer_activas(self.configuracion["notificaciones_activas"])
        self.temporizador.setInterval(nuevo_intervalo_ms)

        if tema_cambio:
            self._aplicar_tema(self.configuracion["tema"])

        self._fijar_estado("Ajustes guardados correctamente.")

    # ------------------------------------------------------------------
    # Cierre de la aplicación
    # ------------------------------------------------------------------

    def closeEvent(self, event):
        if self.hilo_espera is not None and self.hilo_espera.isRunning():
            self.hilo_espera.cancelar()
            self.hilo_espera.wait(1000)

        minimizar_a_bandeja = self.configuracion.get("minimizar_a_bandeja", True)
        soporta_bandeja = QSystemTrayIcon.isSystemTrayAvailable()

        if minimizar_a_bandeja and soporta_bandeja and not self._salir_solicitado:
            event.ignore()
            self.hide()
            self.notificador.notificar(
                "Gestor de Correo Temporal",
                "La aplicación sigue activa en la bandeja del sistema.",
            )
            return

        self.icono_bandeja.hide()
        event.accept()


def main():
    aplicacion = QApplication(sys.argv)
    aplicacion.setApplicationName("Gestor de Correo Temporal")
    aplicacion.setQuitOnLastWindowClosed(False)

    fuente = QFont("Segoe UI", 10)
    aplicacion.setFont(fuente)

    ventana = VentanaPrincipal()
    ventana.show()

    sys.exit(aplicacion.exec())


if __name__ == "__main__":
    main()

