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
import idiomas
from idiomas import t
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


class ItemDireccion(QListWidgetItem):
    def __init__(self, cuenta):
        nombre_proveedor = NOMBRES_PROVEEDOR_VISIBLE.get(
            cuenta.get("proveedor", ""), cuenta.get("proveedor", "")
        )
        etiqueta = f"{cuenta['address']}\n{cuenta.get('creado', '')}  ·  {nombre_proveedor}"
        super().__init__(etiqueta)
        self.cuenta = cuenta
        self.setSizeHint(QSize(0, 58))


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.configuracion = configuracion.cargar_configuracion()
        idiomas.establecer_idioma(self.configuracion.get("idioma", "es"))

        self.setWindowTitle(t("titulo_app"))
        self.resize(1200, 720)
        self.setMinimumSize(1000, 580)

        self.gestor_proveedores = GestorProveedores()
        self.cuentas = almacenamiento.cargar_cuentas()
        self.historial = almacenamiento.cargar_historial()

        self.mensajes_actuales = []
        self.viendo_historial = False
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


    def _construir_bandeja_sistema(self):
        self.icono_bandeja = QSystemTrayIcon(self._icono_app, self)
        self.icono_bandeja.setToolTip(t("titulo_app"))

        menu = QMenu()
        self.accion_mostrar_bandeja = QAction(t("menu_mostrar_ventana"), self)
        self.accion_mostrar_bandeja.triggered.connect(self._mostrar_desde_bandeja)
        self.accion_salir_bandeja = QAction(t("menu_salir"), self)
        self.accion_salir_bandeja.triggered.connect(self._salir_completamente)

        menu.addAction(self.accion_mostrar_bandeja)
        menu.addSeparator()
        menu.addAction(self.accion_salir_bandeja)

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
        self.barra_estado.showMessage(t("listo"))

    def _crear_barra_superior(self):
        barra = QFrame()
        barra.setObjectName("barraSuperior")
        barra.setFixedHeight(64)

        layout = QHBoxLayout(barra)
        layout.setContentsMargins(20, 8, 20, 8)

        bloque_titulos = QVBoxLayout()
        bloque_titulos.setSpacing(0)

        self.etiqueta_titulo_app = QLabel(t("titulo_app"))
        self.etiqueta_titulo_app.setObjectName("tituloApp")
        self.etiqueta_subtitulo_app = QLabel(t("subtitulo_app"))
        self.etiqueta_subtitulo_app.setObjectName("subtituloApp")

        bloque_titulos.addWidget(self.etiqueta_titulo_app)
        bloque_titulos.addWidget(self.etiqueta_subtitulo_app)

        layout.addLayout(bloque_titulos)
        layout.addStretch()

        self.boton_ajustes = QPushButton(t("boton_ajustes"))
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
        self.etiqueta_encabezado_direcciones = QLabel(t("encabezado_direcciones"))
        self.etiqueta_encabezado_direcciones.setObjectName("encabezadoPanel")
        fila_encabezado.addWidget(self.etiqueta_encabezado_direcciones)
        fila_encabezado.addStretch()
        layout.addLayout(fila_encabezado)

        self.boton_nueva_direccion = QPushButton(t("boton_nueva_direccion"))
        self.boton_nueva_direccion.setObjectName("botonPrimario")
        self.boton_nueva_direccion.setCursor(Qt.PointingHandCursor)
        self.boton_nueva_direccion.clicked.connect(self._accion_crear_cuenta)
        layout.addWidget(self.boton_nueva_direccion)

        self.campo_busqueda_direcciones = QLineEdit()
        self.campo_busqueda_direcciones.setPlaceholderText(t("placeholder_buscar_direccion"))
        self.campo_busqueda_direcciones.textChanged.connect(self._filtrar_lista_direcciones)
        layout.addWidget(self.campo_busqueda_direcciones)

        self.lista_direcciones = QListWidget()
        self.lista_direcciones.setSelectionMode(QAbstractItemView.SingleSelection)
        self.lista_direcciones.currentItemChanged.connect(self._al_seleccionar_cuenta)
        layout.addWidget(self.lista_direcciones, stretch=1)

        self.campo_direccion_actual = QLineEdit()
        self.campo_direccion_actual.setReadOnly(True)
        self.campo_direccion_actual.setPlaceholderText(t("placeholder_direccion_actual"))
        self.campo_direccion_actual.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.campo_direccion_actual)

        fila_botones_pie = QHBoxLayout()
        self.boton_copiar_direccion = QPushButton(t("boton_copiar"))
        self.boton_copiar_direccion.setObjectName("botonSecundario")
        self.boton_copiar_direccion.setCursor(Qt.PointingHandCursor)
        self.boton_copiar_direccion.clicked.connect(self._accion_copiar_direccion)

        self.boton_exportar_cuenta = QPushButton(t("boton_exportar"))
        self.boton_exportar_cuenta.setObjectName("botonSecundario")
        self.boton_exportar_cuenta.setCursor(Qt.PointingHandCursor)
        self.boton_exportar_cuenta.clicked.connect(self._accion_exportar_cuenta)

        self.boton_eliminar_direccion = QPushButton(t("boton_eliminar"))
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
        self.etiqueta_encabezado_bandeja = QLabel(t("encabezado_bandeja_entrada"))
        self.etiqueta_encabezado_bandeja.setObjectName("encabezadoPanel")
        fila_encabezado.addWidget(self.etiqueta_encabezado_bandeja)
        fila_encabezado.addStretch()

        self.boton_ver_historial = QPushButton(t("boton_ver_historial"))
        self.boton_ver_historial.setObjectName("botonSecundario")
        self.boton_ver_historial.setCursor(Qt.PointingHandCursor)
        self.boton_ver_historial.setCheckable(True)
        self.boton_ver_historial.clicked.connect(self._alternar_vista_historial)

        self.boton_actualizar = QPushButton(t("boton_actualizar"))
        self.boton_actualizar.setObjectName("botonSecundario")
        self.boton_actualizar.setCursor(Qt.PointingHandCursor)
        self.boton_actualizar.clicked.connect(self._accion_actualizar_mensajes)

        self.boton_esperar_codigo = QPushButton(t("boton_esperar_mensaje"))
        self.boton_esperar_codigo.setObjectName("botonPrimario")
        self.boton_esperar_codigo.setCursor(Qt.PointingHandCursor)
        self.boton_esperar_codigo.clicked.connect(self._accion_esperar_codigo)

        fila_encabezado.addWidget(self.boton_ver_historial)
        fila_encabezado.addWidget(self.boton_actualizar)
        fila_encabezado.addWidget(self.boton_esperar_codigo)
        layout.addLayout(fila_encabezado)

        self.campo_busqueda_mensajes = QLineEdit()
        self.campo_busqueda_mensajes.setPlaceholderText(t("placeholder_buscar_mensajes"))
        self.campo_busqueda_mensajes.textChanged.connect(self._filtrar_tabla_mensajes)
        layout.addWidget(self.campo_busqueda_mensajes)

        self.pila_bandeja = QStackedWidget()

        self.pagina_vacia = self._crear_pagina_vacia()
        self.pila_bandeja.addWidget(self.pagina_vacia)

        splitter_vertical = QSplitter(Qt.Vertical)

        self.tabla_mensajes = QTableWidget(0, 3)
        self.tabla_mensajes.setHorizontalHeaderLabels([t("columna_remitente"), t("columna_asunto"), t("columna_recibido")])
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

        self.etiqueta_vacio_titulo = QLabel(t("estado_vacio_titulo"))
        self.etiqueta_vacio_titulo.setObjectName("estadoVacioTitulo")
        self.etiqueta_vacio_titulo.setAlignment(Qt.AlignCenter)

        self.etiqueta_vacio_texto = QLabel(t("estado_vacio_texto"))
        self.etiqueta_vacio_texto.setObjectName("estadoVacioTexto")
        self.etiqueta_vacio_texto.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.etiqueta_vacio_titulo)
        layout.addWidget(self.etiqueta_vacio_texto)
        return pagina

    def _crear_tarjeta_codigo(self):
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjetaCodigo")
        layout = QHBoxLayout(tarjeta)
        layout.setContentsMargins(14, 10, 14, 10)

        bloque_texto = QVBoxLayout()
        bloque_texto.setSpacing(2)
        self.etiqueta_codigo_titulo = QLabel(t("codigo_detectado"))
        self.etiqueta_codigo_titulo.setObjectName("etiquetaCodigoTitulo")
        self.etiqueta_valor_codigo = QLabel("")
        self.etiqueta_valor_codigo.setObjectName("etiquetaCodigo")

        bloque_texto.addWidget(self.etiqueta_codigo_titulo)
        bloque_texto.addWidget(self.etiqueta_valor_codigo)

        layout.addLayout(bloque_texto)
        layout.addStretch()

        self.boton_copiar_codigo = QPushButton(t("boton_copiar_codigo"))
        self.boton_copiar_codigo.setObjectName("botonSecundario")
        self.boton_copiar_codigo.setCursor(Qt.PointingHandCursor)
        self.boton_copiar_codigo.clicked.connect(self._accion_copiar_codigo)
        layout.addWidget(self.boton_copiar_codigo, alignment=Qt.AlignVCenter)

        return tarjeta


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
        self.boton_nueva_direccion.setText(t("boton_creando_direccion"))
        self._fijar_estado(t("estado_creando_direccion"))

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
        self.boton_nueva_direccion.setText(t("boton_nueva_direccion"))

        nombre_proveedor = NOMBRES_PROVEEDOR_VISIBLE.get(identificador_proveedor, identificador_proveedor)
        self._fijar_estado(t("estado_direccion_creada", proveedor=nombre_proveedor, direccion=datos_cuenta["address"]))

    def _al_crear_cuenta_error(self, mensaje):
        self.boton_nueva_direccion.setEnabled(True)
        self.boton_nueva_direccion.setText(t("boton_nueva_direccion"))
        self._fijar_estado(t("estado_no_se_pudo_crear"))
        self._mostrar_error(t("titulo_app"), t("error_no_se_pudo_crear_detalle", detalle=mensaje))

    def _accion_eliminar_cuenta(self):
        cuenta = self._cuenta_actual()
        if cuenta is None:
            QMessageBox.information(
                self, t("titulo_app"), t("dialogo_seleccionar_direccion")
            )
            return

        respuesta = QMessageBox.question(
            self,
            t("titulo_eliminar_direccion"),
            t("confirmar_eliminar_direccion", direccion=cuenta["address"]),
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

        self._fijar_estado(t("estado_direccion_eliminada"))

    def _accion_copiar_direccion(self):
        cuenta = self._cuenta_actual()
        if cuenta is None:
            return
        QApplication.clipboard().setText(cuenta["address"])
        self._fijar_estado(t("estado_direccion_copiada"))

    def _accion_exportar_cuenta(self):
        cuenta = self._cuenta_actual()
        if cuenta is None:
            QMessageBox.information(
                self, t("titulo_app"), t("dialogo_seleccionar_direccion")
            )
            return

        nombre_sugerido = cuenta["address"].replace("@", "_at_") + ".txt"
        ruta_destino, _ = QFileDialog.getSaveFileName(
            self, t("titulo_exportar_direccion"), nombre_sugerido, t("filtro_archivos_texto")
        )
        if not ruta_destino:
            return

        nombre_proveedor = NOMBRES_PROVEEDOR_VISIBLE.get(cuenta.get("proveedor", ""), t("exportar_desconocido"))
        contrasena = cuenta.get("password") or t("exportar_sin_contrasena")
        contenido = (
            f"{t('exportar_etiqueta_direccion')}:  {cuenta['address']}\n"
            f"{t('exportar_etiqueta_contrasena')}: {contrasena}\n"
            f"{t('exportar_etiqueta_proveedor')}:  {nombre_proveedor}\n"
            f"{t('exportar_etiqueta_creada')}:     {cuenta.get('creado', '')}\n"
        )

        try:
            with open(ruta_destino, "w", encoding="utf-8") as f:
                f.write(contenido)
        except OSError as e:
            self._mostrar_error(t("titulo_app"), t("error_no_se_pudo_guardar_archivo", detalle=e))
            return

        self._fijar_estado(t("estado_direccion_exportada"))


    def _accion_actualizar_mensajes(self):
        cuenta = self._cuenta_actual()
        if cuenta is None:
            return

        self.boton_ver_historial.setChecked(False)
        self.viendo_historial = False
        self.etiqueta_encabezado_bandeja.setText(t("encabezado_bandeja_entrada"))

        self._fijar_estado(t("estado_consultando_bandeja"))
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
            self._fijar_estado(t("estado_n_mensajes", n=len(mensajes)))
        else:
            self._fijar_estado(t("estado_bandeja_vacia"))

    def _al_listar_mensajes_error(self, mensaje):
        self.boton_actualizar.setEnabled(True)
        self._fijar_estado(t("estado_no_se_pudo_actualizar_bandeja"))

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

        self._fijar_estado(t("estado_cargando_mensaje"))

        self.hilo_activo = TareaObtenerMensaje(self.gestor_proveedores, cuenta, mensaje_resumen.id)
        self.hilo_activo.exito.connect(self._al_obtener_mensaje_exito)
        self.hilo_activo.error.connect(self._al_obtener_mensaje_error)
        self.hilo_activo.start()

    def _al_obtener_mensaje_exito(self, mensaje_completo):
        self.texto_cuerpo.setPlainText(mensaje_completo.cuerpo_texto.strip())
        self._detectar_y_mostrar_codigo(mensaje_completo.asunto, mensaje_completo.cuerpo_texto)
        self._fijar_estado(t("estado_mensaje_cargado"))

    def _al_obtener_mensaje_error(self, mensaje):
        self._fijar_estado(t("estado_no_se_pudo_cargar_mensaje"))

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
            self.etiqueta_encabezado_bandeja.setText(t("encabezado_historial"))
            entradas = almacenamiento.historial_de_direccion(self.historial, cuenta["address"])
            self.mensajes_actuales = [MensajeResumen.desde_dict(e) for e in entradas]
            self._refrescar_tabla_mensajes()
            self.pila_bandeja.setCurrentIndex(1 if self.mensajes_actuales else 0)
            if not self.mensajes_actuales:
                self._fijar_estado(t("estado_sin_historial"))
            else:
                self._fijar_estado(t("estado_mostrando_historial", n=len(self.mensajes_actuales)))
        else:
            self.etiqueta_encabezado_bandeja.setText(t("encabezado_bandeja_entrada"))
            self._accion_actualizar_mensajes()

    def _mostrar_mensaje_de_historial(self, mensaje_resumen):
        self.texto_cuerpo.setPlainText(
            t("historial_solo_resumen", remitente=mensaje_resumen.remitente, asunto=mensaje_resumen.asunto)
        )
        self._detectar_y_mostrar_codigo(mensaje_resumen.asunto, "")


    def _accion_esperar_codigo(self):
        cuenta = self._cuenta_actual()
        if cuenta is None:
            QMessageBox.information(self, t("titulo_app"), t("dialogo_seleccionar_direccion_simple"))
            return

        if self.viendo_historial:
            QMessageBox.information(
                self,
                t("titulo_app"),
                t("estado_salir_de_historial"),
            )
            return

        if self.hilo_espera is not None and self.hilo_espera.isRunning():
            return

        ids_conocidos = {m.id for m in self.mensajes_actuales}

        self.boton_esperar_codigo.setEnabled(False)
        self.boton_esperar_codigo.setText(t("boton_esperando_mensaje"))
        self._fijar_estado(t("estado_esperando_mensaje"), 0)

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
        self.boton_esperar_codigo.setText(t("boton_esperar_mensaje"))

        if not nuevo:
            self._fijar_estado(t("estado_no_llego_mensaje"))
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

        self._fijar_estado(t("estado_llego_mensaje_nuevo"))
        self.notificador.notificar(
            t("notificacion_nuevo_mensaje_titulo"),
            t("notificacion_nuevo_mensaje_cuerpo", remitente=nuevo.remitente, asunto=nuevo.asunto),
        )

    def _al_esperar_codigo_error(self, mensaje):
        self.boton_esperar_codigo.setEnabled(True)
        self.boton_esperar_codigo.setText(t("boton_esperar_mensaje"))
        self._fijar_estado(t("estado_espera_detenida_error"))


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
        self._hilo_autoactualizacion = hilo

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
            self._fijar_estado(t("estado_bandeja_actualizada"))

            if nuevos:
                primero = nuevos[0]
                extra = t("notificacion_mas_mensajes", n=len(nuevos) - 1) if len(nuevos) > 1 else ""
                self.notificador.notificar(
                    t("notificacion_nuevo_mensaje_titulo"),
                    t("notificacion_nuevo_mensaje_cuerpo_extra", remitente=primero.remitente, asunto=primero.asunto, extra=extra),
                )


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
        idioma_cambio = nueva_configuracion.get("idioma", "es") != self.configuracion.get("idioma", "es")
        nuevo_intervalo_ms = nueva_configuracion["intervalo_autoactualizacion_seg"] * 1000

        self.configuracion = nueva_configuracion
        configuracion.guardar_configuracion(self.configuracion)

        self.notificador.establecer_activas(self.configuracion["notificaciones_activas"])
        self.temporizador.setInterval(nuevo_intervalo_ms)

        if tema_cambio:
            self._aplicar_tema(self.configuracion["tema"])

        if idioma_cambio:
            idiomas.establecer_idioma(self.configuracion["idioma"])
            self._retraducir_interfaz()

        self._fijar_estado(t("estado_ajustes_guardados"))

    def _retraducir_interfaz(self):
        self.setWindowTitle(t("titulo_app"))
        QApplication.instance().setApplicationName(t("titulo_app"))

        self.icono_bandeja.setToolTip(t("titulo_app"))
        self.accion_mostrar_bandeja.setText(t("menu_mostrar_ventana"))
        self.accion_salir_bandeja.setText(t("menu_salir"))

        self.etiqueta_titulo_app.setText(t("titulo_app"))
        self.etiqueta_subtitulo_app.setText(t("subtitulo_app"))
        self.boton_ajustes.setText(t("boton_ajustes"))

        self.etiqueta_encabezado_direcciones.setText(t("encabezado_direcciones"))
        self.boton_nueva_direccion.setText(t("boton_nueva_direccion"))
        self.campo_busqueda_direcciones.setPlaceholderText(t("placeholder_buscar_direccion"))
        self.campo_direccion_actual.setPlaceholderText(t("placeholder_direccion_actual"))
        self.boton_copiar_direccion.setText(t("boton_copiar"))
        self.boton_exportar_cuenta.setText(t("boton_exportar"))
        self.boton_eliminar_direccion.setText(t("boton_eliminar"))

        self.etiqueta_encabezado_bandeja.setText(
            t("encabezado_historial") if self.viendo_historial else t("encabezado_bandeja_entrada")
        )
        self.boton_ver_historial.setText(t("boton_ver_historial"))
        self.boton_actualizar.setText(t("boton_actualizar"))
        if not (self.hilo_espera is not None and self.hilo_espera.isRunning()):
            self.boton_esperar_codigo.setText(t("boton_esperar_mensaje"))
        self.campo_busqueda_mensajes.setPlaceholderText(t("placeholder_buscar_mensajes"))
        self.tabla_mensajes.setHorizontalHeaderLabels(
            [t("columna_remitente"), t("columna_asunto"), t("columna_recibido")]
        )

        self.etiqueta_vacio_titulo.setText(t("estado_vacio_titulo"))
        self.etiqueta_vacio_texto.setText(t("estado_vacio_texto"))

        self.etiqueta_codigo_titulo.setText(t("codigo_detectado"))
        self.boton_copiar_codigo.setText(t("boton_copiar_codigo"))


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
                t("titulo_app"),
                t("notificacion_app_en_segundo_plano"),
            )
            return

        self.icono_bandeja.hide()
        event.accept()


def main():
    config_inicial = configuracion.cargar_configuracion()
    idiomas.establecer_idioma(config_inicial.get("idioma", "es"))

    aplicacion = QApplication(sys.argv)
    aplicacion.setApplicationName(t("titulo_app"))
    aplicacion.setQuitOnLastWindowClosed(False)

    fuente = QFont("Segoe UI", 10)
    aplicacion.setFont(fuente)

    ventana = VentanaPrincipal()
    ventana.show()

    sys.exit(aplicacion.exec())


if __name__ == "__main__":
    main()

