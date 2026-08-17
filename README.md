# 📧 Gestor de Correo Temporal

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![PySide6](https://img.shields.io/badge/PySide6-6.6%2B-41CD52?logo=qt)
![License](https://img.shields.io/badge/license-MIT-green)

Aplicación de escritorio con interfaz fluida y cuidada (temas claro/oscuro)
para crear direcciones de correo electrónico temporales, revisar su bandeja
de entrada y detectar automáticamente códigos de verificación.

## 📸 Capturas de pantalla

<img width="1918" height="1078" alt="image" src="https://github.com/user-attachments/assets/5a571647-d894-4833-ae2c-cfe679133fba" />

## ✨ Funcionalidades

- Creación de direcciones con **mail.tm** o **Guerrilla Mail**, con cambio
  automático de proveedor si uno falla (modo "Automático")
- Bandeja de entrada con búsqueda/filtro por remitente o asunto
- Detección automática de códigos de verificación, con patrón
  personalizable (expresión regular) desde Ajustes
- Historial local de mensajes por dirección, independiente de la bandeja
  en vivo
- Notificaciones de escritorio activables/desactivables
- Icono en la bandeja del sistema; la app puede seguir en segundo plano
  al cerrar la ventana (configurable)
- Tema claro u oscuro
- Exportar una dirección (y su contraseña, si aplica) a un archivo de texto
- Intervalos de autoactualización y de espera configurables

## 🚀 Instalación

```bash
git clone https://github.com/tu-usuario/gestor-correo-temporal.git
cd Gh0stMail
pip install -r requirements.txt
```

## ▶️ Uso

```bash
pythonw main.py
```

## 📁 Estructura del proyecto

| Archivo/Carpeta | Descripción |
|---|---|
| `main.py` | Ventana principal y lógica de interfaz |
| `dialogo_ajustes.py` | Ventana modal de configuración |
| `gestor_proveedores.py` | Selección de proveedor y failover automático |
| `proveedores/` | Implementaciones de mail.tm y Guerrilla Mail |
| `tareas.py` | Operaciones de red en hilos (QThread) |
| `configuracion.py` / `almacenamiento.py` | Persistencia en JSON |
| `notificaciones.py` | Notificaciones de escritorio vía bandeja del sistema |
| `utilidades.py` | Detección de códigos y formateo de fechas |
| `tema_claro.qss` / `tema_oscuro.qss` | Hojas de estilo |

## 🤝 Contribuir

Las contribuciones son bienvenidas. Si quieres proponer un cambio:

1. Haz un fork del repositorio
2. Crea una rama para tu cambio (`git checkout -b mi-mejora`)
3. Haz commit de tus cambios
4. Abre un Pull Request

## ☕ Apoya el proyecto

Si te resulta útil, puedes invitarme a un café:

[![PayPal](https://img.shields.io/badge/PayPal-Donar-00457C?logo=paypal)](https://paypal.me/Davidnt20)

## 📄 Licencia

Este proyecto está bajo la licencia MIT — consulta el archivo [LICENSE](LICENSE) para más detalles.
