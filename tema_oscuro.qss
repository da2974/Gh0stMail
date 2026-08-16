/*
tema_oscuro.qss

Tema visual oscuro de la aplicación, con la misma estructura que el tema
claro para asegurar coherencia entre ambos modos.
*/

* {
    font-family: "Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
    color: #E6E8EB;
}

QMainWindow, QDialog {
    background-color: #16181C;
}

#barraSuperior {
    background-color: #1D2025;
    border-bottom: 1px solid #2A2E35;
}

#tituloApp {
    font-size: 16px;
    font-weight: 600;
    color: #F2F3F5;
}

#subtituloApp {
    font-size: 11px;
    color: #9498A0;
}

#insigniaProveedor {
    font-size: 11px;
    font-weight: 600;
    color: #6FA1FF;
    background-color: #1F2B45;
    border-radius: 9px;
    padding: 4px 10px;
}

QFrame#panelTarjeta {
    background-color: #1D2025;
    border: 1px solid #2A2E35;
    border-radius: 10px;
}

QLabel#encabezadoPanel {
    font-size: 12px;
    font-weight: 600;
    color: #C3C7CD;
    letter-spacing: 0.3px;
}

QPushButton {
    border-radius: 7px;
    padding: 8px 16px;
    font-weight: 600;
    border: 1px solid transparent;
}

QPushButton#botonPrimario {
    background-color: #4A80F0;
    color: #FFFFFF;
}
QPushButton#botonPrimario:hover { background-color: #3D6FDC; }
QPushButton#botonPrimario:pressed { background-color: #3260C4; }
QPushButton#botonPrimario:disabled { background-color: #34405E; color: #7C87A0; }

QPushButton#botonSecundario {
    background-color: #23262C;
    color: #DADCE0;
    border: 1px solid #34383F;
}
QPushButton#botonSecundario:hover { background-color: #2A2E35; }
QPushButton#botonSecundario:pressed { background-color: #1F2227; }
QPushButton#botonSecundario:disabled { color: #5B5F68; }
QPushButton#botonSecundario:checked {
    background-color: #1F2B45;
    border: 1px solid #4A80F0;
    color: #9EC0FF;
}

QPushButton#botonPeligro {
    background-color: #23262C;
    color: #F1707E;
    border: 1px solid #4A2A31;
}
QPushButton#botonPeligro:hover { background-color: #33191D; }

QPushButton#botonTexto {
    background-color: transparent;
    color: #6FA1FF;
    border: none;
    padding: 4px 6px;
    font-weight: 600;
    text-align: left;
}
QPushButton#botonTexto:hover { color: #9EC0FF; text-decoration: underline; }

QTabWidget::pane {
    border: 1px solid #2A2E35;
    border-radius: 8px;
    background: #1D2025;
    top: -1px;
}
QTabBar::tab {
    background: transparent;
    color: #8A8F98;
    padding: 8px 16px;
    font-weight: 600;
    border-bottom: 2px solid transparent;
}
QTabBar::tab:selected {
    color: #6FA1FF;
    border-bottom: 2px solid #6FA1FF;
}
QTabBar::tab:hover:!selected { color: #DADCE0; }

QListWidget {
    background-color: #1D2025;
    border: none;
    outline: none;
}
QListWidget::item {
    padding: 10px 8px;
    border-bottom: 1px solid #26292F;
}
QListWidget::item:selected {
    background-color: #1F2B45;
    color: #F2F3F5;
    border-left: 3px solid #4A80F0;
}
QListWidget::item:hover:!selected { background-color: #23262C; }

QTableWidget {
    background-color: #1D2025;
    border: none;
    gridline-color: #26292F;
    selection-background-color: #1F2B45;
    selection-color: #F2F3F5;
}
QTableWidget::item { padding: 8px; border-bottom: 1px solid #26292F; }

QHeaderView::section {
    background-color: #181A1F;
    color: #8A8F98;
    font-weight: 600;
    font-size: 11px;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #2A2E35;
}

QLineEdit, QSpinBox, QComboBox {
    background-color: #16181C;
    border: 1px solid #34383F;
    border-radius: 7px;
    padding: 8px 10px;
    color: #E6E8EB;
    selection-background-color: #3D6FDC;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid #4A80F0;
    background-color: #1D2025;
}
QLineEdit[readOnly="true"] {
    background-color: #1A1C21;
    color: #C3C7CD;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 13px;
}
QComboBox::drop-down { border: none; width: 24px; }
QComboBox QAbstractItemView {
    background-color: #1D2025;
    border: 1px solid #34383F;
    selection-background-color: #1F2B45;
    selection-color: #F2F3F5;
    outline: none;
    color: #E6E8EB;
}

QCheckBox { spacing: 8px; color: #E6E8EB; }
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #34383F;
    background: #16181C;
}
QCheckBox::indicator:checked {
    background: #4A80F0;
    border: 1px solid #4A80F0;
}

QTextEdit { background-color: #1D2025; border: none; padding: 4px; color: #E6E8EB; }

QFrame#tarjetaCodigo {
    background-color: #163825;
    border: 1px solid #245C3A;
    border-radius: 8px;
}
QLabel#etiquetaCodigo {
    color: #5FD68C;
    font-size: 16px;
    font-weight: 700;
    font-family: "Consolas", "Courier New", monospace;
}
QLabel#etiquetaCodigoTitulo {
    color: #4FBF7C;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.4px;
}

QLabel#estadoVacioTitulo { color: #C3C7CD; font-size: 13px; font-weight: 600; }
QLabel#estadoVacioTexto { color: #6B707A; font-size: 12px; }

QLabel#etiquetaAjusteTitulo { font-size: 12px; font-weight: 600; color: #F2F3F5; }
QLabel#etiquetaAjusteDescripcion { font-size: 11px; color: #8A8F98; }
QFrame#separadorAjustes { background-color: #26292F; max-height: 1px; min-height: 1px; }

QStatusBar {
    background-color: #1D2025;
    border-top: 1px solid #2A2E35;
    color: #8A8F98;
    font-size: 11px;
    padding: 2px 8px;
}

QScrollBar:vertical { background: transparent; width: 10px; margin: 0; }
QScrollBar::handle:vertical { background: #34383F; border-radius: 5px; min-height: 24px; }
QScrollBar::handle:vertical:hover { background: #40454D; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: transparent; height: 10px; }
QScrollBar::handle:horizontal { background: #34383F; border-radius: 5px; min-width: 24px; }

QSplitter::handle { background-color: #16181C; width: 1px; }

QToolTip {
    background-color: #F2F3F5;
    color: #16181C;
    border: none;
    padding: 6px 8px;
    border-radius: 4px;
}

QMenu {
    background-color: #1D2025;
    border: 1px solid #2A2E35;
    border-radius: 8px;
    padding: 4px;
    color: #E6E8EB;
}
QMenu::item { padding: 7px 20px; border-radius: 5px; }
QMenu::item:selected { background-color: #1F2B45; color: #F2F3F5; }
