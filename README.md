# Gestor de Correo Temporal

Aplicación de escritorio (PySide6) para crear direcciones de correo
electrónico temporales, revisar su bandeja de entrada y detectar
automáticamente códigos de verificación.

## Instalación

```
pip install -r requirements.txt
```

## Ejecución

```
python3 main.py
```

## Estructura del proyecto

- `main.py` — ventana principal y lógica de interfaz
- `dialogo_ajustes.py` — ventana modal de configuración
- `gestor_proveedores.py` — selección de proveedor y failover automático
- `proveedores/` — implementaciones de mail.tm y Guerrilla Mail
- `tareas.py` — operaciones de red en hilos (QThread)
- `configuracion.py` / `almacenamiento.py` — persistencia en JSON
- `notificaciones.py` — notificaciones de escritorio vía bandeja del sistema
- `utilidades.py` — detección de códigos y formateo de fechas
- `tema_claro.qss` / `tema_oscuro.qss` — hojas de estilo

## Funcionalidades

- Creación de direcciones con mail.tm o Guerrilla Mail, con cambio
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
