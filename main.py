/*
tema_claro.qss

Tema visual claro de la aplicación: fondo neutro, tarjetas blancas,
un único color de acento y tipografía consistente.
*/

* {
    font-family: "Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
    color: #1F2328;
}

QMainWindow, QDialog {
    background-color: #F3F4F7;
}

#barraSuperior {
    background-color: #FFFFFF;
    border-bottom: 1px solid #E3E5EA;
}

#tituloApp {
    font-size: 16px;
    font-weight: 600;
    color: #14171A;
}

#subtituloApp {
    font-size: 11px;
    color: #7C828A;
}

#insigniaProveedor {
    font-size: 11px;
    font-weight: 600;
    color: #2F6FED;
    background-color: #EAF1FE;
    border-radius: 9px;
    padding: 4px 10px;
}

QFrame#panelTarjeta {
    background-color: #FFFFFF;
    border: 1px solid #E3E5EA;
    border-radius: 10px;
}

QLabel#encabezadoPanel {
    font-size: 12px;
    font-weight: 600;
    color: #40454C;
    letter-spacing: 0.3px;
}

QPushButton {
    border-radius: 7px;
    padding: 8px 16px;
    font-weight: 600;
    border: 1px solid transparent;
}

QPushButton#botonPrimario {
    background-color: #2F6FED;
    color: #FFFFFF;
}
QPushButton#botonPrimario:hover { background-color: #255FD1; }
QPushButton#botonPrimario:pressed { background-color: #1F4FB0; }
QPushButton#botonPrimario:disabled { background-color: #A9C2F5; color: #F0F4FF; }

QPushButton#botonSecundario {
    background-color: #FFFFFF;
    color: #303540;
    border: 1px solid #D7DBE0;
}
QPushButton#botonSecundario:hover { background-color: #F2F4F7; }
QPushButton#botonSecundario:pressed { background-color: #E6E9EE; }
QPushButton#botonSecundario:disabled { color: #ABB0B8; }
QPushButton#botonSecundario:checked {
    background-color: #EAF1FE;
    border: 1px solid #2F6FED;
    color: #1F4FB0;
}

QPushButton#botonPeligro {
    background-color: #FFFFFF;
    color: #C82333;
    border: 1px solid #F1C3C8;
}
QPushButton#botonPeligro:hover { background-color: #FDEBEC; }

QPushButton#botonTexto {
    background-color: transparent;
    color: #2F6FED;
    border: none;
    padding: 4px 6px;
    font-weight: 600;
    text-align: left;
}
QPushButton#botonTexto:hover { color: #1F4FB0; text-decoration: underline; }

QTabWidget::pane {
    border: 1px solid #E3E5EA;
    border-radius: 8px;
    background: #FFFFFF;
    top: -1px;
}
QTabBar::tab {
    background: transparent;
    color: #7C828A;
    padding: 8px 16px;
    font-weight: 600;
    border-bottom: 2px solid transparent;
}
QTabBar::tab:selected {
    color: #2F6FED;
    border-bottom: 2px solid #2F6FED;
}
QTabBar::tab:hover:!selected { color: #40454C; }

QListWidget {
    background-color: #FFFFFF;
    border: none;
    outline: none;
}
QListWidget::item {
    padding: 10px 8px;
    border-bottom: 1px solid #F0F1F3;
}
QListWidget::item:selected {
    background-color: #EAF1FE;
    color: #14171A;
    border-left: 3px solid #2F6FED;
}
QListWidget::item:hover:!selected { background-color: #F7F8FA; }

QTableWidget {
    background-color: #FFFFFF;
    border: none;
    gridline-color: #EFF0F3;
    selection-background-color: #EAF1FE;
    selection-color: #14171A;
}
QTableWidget::item { padding: 8px; border-bottom: 1px solid #F0F1F3; }

QHeaderView::section {
    background-color: #FAFBFC;
    color: #7C828A;
    font-weight: 600;
    font-size: 11px;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #E3E5EA;
}

QLineEdit, QSpinBox, QComboBox {
    background-color: #FAFBFC;
    border: 1px solid #D7DBE0;
    border-radius: 7px;
    padding: 8px 10px;
    selection-background-color: #C7D9FA;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid #2F6FED;
    background-color: #FFFFFF;
}
QLineEdit[readOnly="true"] {
    background-color: #F5F6F8;
    color: #40454C;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 13px;
}
QComboBox::drop-down { border: none; width: 24px; }
QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #D7DBE0;
    selection-background-color: #EAF1FE;
    selection-color: #14171A;
    outline: none;
}

QCheckBox { spacing: 8px; }
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #D7DBE0;
    background: #FFFFFF;
}
QCheckBox::indicator:checked {
    background: #2F6FED;
    border: 1px solid #2F6FED;
}

QTextEdit { background-color: #FFFFFF; border: none; padding: 4px; }

QFrame#tarjetaCodigo {
    background-color: #E9F7EC;
    border: 1px solid #B7E4C2;
    border-radius: 8px;
}
QLabel#etiquetaCodigo {
    color: #167A34;
    font-size: 16px;
    font-weight: 700;
    font-family: "Consolas", "Courier New", monospace;
}
QLabel#etiquetaCodigoTitulo {
    color: #2E8B4F;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.4px;
}

QLabel#estadoVacioTitulo { color: #40454C; font-size: 13px; font-weight: 600; }
QLabel#estadoVacioTexto { color: #9AA0A8; font-size: 12px; }

QLabel#etiquetaAjusteTitulo { font-size: 12px; font-weight: 600; color: #14171A; }
QLabel#etiquetaAjusteDescripcion { font-size: 11px; color: #7C828A; }
QFrame#separadorAjustes { background-color: #EEF0F3; max-height: 1px; min-height: 1px; }

QStatusBar {
    background-color: #FFFFFF;
    border-top: 1px solid #E3E5EA;
    color: #7C828A;
    font-size: 11px;
    padding: 2px 8px;
}

QScrollBar:vertical { background: transparent; width: 10px; margin: 0; }
QScrollBar::handle:vertical { background: #D7DBE0; border-radius: 5px; min-height: 24px; }
QScrollBar::handle:vertical:hover { background: #C1C6CD; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: transparent; height: 10px; }
QScrollBar::handle:horizontal { background: #D7DBE0; border-radius: 5px; min-width: 24px; }

QSplitter::handle { background-color: #F3F4F7; width: 1px; }

QToolTip {
    background-color: #14171A;
    color: #FFFFFF;
    border: none;
    padding: 6px 8px;
    border-radius: 4px;
}

QMenu {
    background-color: #FFFFFF;
    border: 1px solid #E3E5EA;
    border-radius: 8px;
    padding: 4px;
}
QMenu::item { padding: 7px 20px; border-radius: 5px; }
QMenu::item:selected { background-color: #EAF1FE; color: #14171A; }
