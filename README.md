# 📧 Gestor de Correo Temporal

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![PySide6](https://img.shields.io/badge/PySide6-6.6%2B-41CD52?logo=qt)
![License](https://img.shields.io/badge/license-MIT-green)

Aplicación de escritorio con interfaz fluida y cuidada (temas claro/oscuro)
para crear direcciones de correo electrónico temporales, revisar su bandeja
de entrada y detectar automáticamente códigos de verificación.

## 📸 Capturas de pantalla

<img width="1918" height="1078" alt="Captura de pantalla 2026-08-17 024334" src="https://github.com/user-attachments/assets/f5662978-0a63-41bb-ae45-fc7df134198c" />


## ✨ Funcionalidades

- Creación de direcciones con **3 proveedores** (mail.tm, Guerrilla Mail, 1secMail), con cambio
  automático de proveedor si uno falla (modo "Automático")
- **Selector de proveedor en Ajustes** → General → "Proveedor de correo" para elegir según necesidad
- Bandeja de entrada con búsqueda/filtro por remitente o asunto
- Detección automática de códigos de verificación, con patrón
  personalizable (expresión regular) desde Ajustes
- Historial local de mensajes por dirección, independiente de la bandeja
  en vivo
- Notificaciones de escritorio activables/desactivables + sonido opcional
- Icono en la bandeja del sistema; la app puede seguir en segundo plano
  al cerrar la ventana (configurable)
- Tema claro u oscuro
- Idioma español o inglés, seleccionable desde Ajustes
- Exportar una dirección (y su contraseña, si aplica) a un archivo de texto
- Intervalos de autoactualización y de espera configurables
- **Cifrado en reposo** del archivo de cuentas (Fernet/AES)
- **Aviso de caducidad estimada** en la lista de direcciones

## Proveedores de correo

| Proveedor | Mejor para | Duración |
|-----------|------------|----------|
| **mail.tm** (recomendado por defecto) | **Usar días/semanas**: 2FA, recuperar contraseña, notificaciones futuras, cualquier cosa que necesite llegar mañana o la semana que viene | Días / semanas (según uso) |
| **Guerrilla Mail** | **Código AHORA**: registro rápido, verificación inmediata, "necesito el código ya" | ~60 min si no se usa (se renueva al consultar) |
| **1secMail** | **Respaldo** si los dos anteriores fallan o están lentos | Indefinida (no publicada) |

## 🌐 Idiomas
La aplicación está disponible en **español** e **inglés**. Puedes cambiar
el idioma en cualquier momento desde Ajustes → General → Idioma; el cambio
se aplica al instante, sin reiniciar la aplicación.

## 🚀 Instalación

```bash
git clone https://github.com/da2974/Gh0stMail.git
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
| `gestor_proveedores.py` | Selección de proveedor y failover automático (3 proveedores) |
| `proveedores/` | Implementaciones de mail.tm, Guerrilla Mail y 1secMail |
| `tareas.py` | Operaciones de red en hilos (QThread) |
| `configuracion.py` / `almacenamiento.py` | Persistencia en JSON (cuentas cifradas con Fernet) |
| `notificaciones.py` | Notificaciones de escritorio vía bandeja del sistema (+ sonido) |
| `utilidades.py` | Detección de códigos, HTML→texto, formateo de fechas, caducidad |
| `idiomas.py` | Textos de la interfaz en español e inglés |
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
