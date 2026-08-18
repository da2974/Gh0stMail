# Cambios aplicados

## 🔴 Seguridad
- **Cifrado en reposo del archivo de cuentas** (`almacenamiento.py`): `~/.correo_temporal_cuentas.json`
  ahora se guarda cifrado con Fernet (AES simétrico). La clave vive en
  `~/.correo_temporal_clave.key` con permisos `600` (solo el propietario puede
  leerla, en sistemas POSIX). Esto protege contra la lectura casual del
  archivo, pero no contra alguien con acceso total a tu cuenta de usuario en
  este equipo — eso es una limitación honesta, no una promesa de seguridad
  absoluta.
  - Compatible con instalaciones anteriores: si el archivo aún está en texto
    plano de una versión previa, se lee igual y se vuelve a guardar cifrado.
  - Si falta el paquete `cryptography`, la app sigue funcionando (cae a texto
    plano) en vez de romperse.
- **Aviso al exportar**: sigue existiendo la exportación a `.txt` sin cifrar
  (es una función explícita para compartir contigo mismo), documentado como
  limitación conocida a considerar si quieres una versión más estricta.

## 🟠 Bugs corregidos
- **HTML sin procesar en el cuerpo del mensaje**: nueva función
  `utilidades.html_a_texto()` limpia `<script>`/`<style>`, convierte
  separadores de bloque en saltos de línea y decodifica entidades. Aplicado
  en los tres proveedores.
- **Hilos (`QThread`) que podían destruirse en marcha**: nuevo método
  `_lanzar_hilo()` en `main.py` mantiene una referencia fuerte a todo hilo en
  curso hasta que termina, evitando el crash clásico de PySide
  "QThread: Destroyed while thread is still running" si el usuario cambia de
  cuenta o repite una acción rápido.
- **Errores de auto-actualización ya no se pierden en silencio**: antes
  `hilo.error.connect(lambda _m: None)`; ahora se refleja en la barra de
  estado.
- **Reautenticación de Guerrilla Mail**: `refrescar_sesion()` no hacía nada;
  ahora hace un "keep-alive" real contra la API para extender la sesión.
- **Cadena `"Código copiado al portapapeles."` hardcodeada en español**:
  ahora usa `t("estado_codigo_copiado")`, ya traducida.
- **Archivos JSON corruptos ya no se pierden en silencio**: se hace una copia
  de seguridad (`archivo.json.corrupto-<timestamp>.bak`) y se avisa al
  usuario con un diálogo al arrancar, en vez de resetear sin decir nada.
- **Cierre de la app con hilos en curso**: `closeEvent` ahora da un margen
  breve a los hilos en vuelo (no solo al de "esperar mensaje") antes de
  cerrar de verdad.

## 🔵 Funcionalidades nuevas
- **Tercer proveedor: 1secMail** (`proveedores/one_sec_mail.py`), para no
  depender solo de mail.tm/Guerrilla Mail si uno de los dos falla o limita.
- **Aviso de caducidad estimada** junto a cada dirección en la lista
  (por ejemplo "≈45 min restantes (estimado)"), calculado a partir de la
  fecha de creación y la duración típica conocida del proveedor. Para
  proveedores sin caducidad publicada (mail.tm, 1secMail) no se muestra nada,
  para no inventar un dato. Se actualiza solo cada minuto.
- **Auto-copiar el código al portapapeles** en cuanto se detecta (ajuste
  desactivado por defecto, en Ajustes → General).
- **Sonido de aviso** al llegar un mensaje nuevo (ajuste activado por
  defecto, silenciable independientemente de las notificaciones de
  escritorio).

## Notas para instalar
Se añadió `cryptography` a `requirements.txt`:
```
pip install -r requirements.txt
```

## Lo que queda pendiente (no incluido en esta pasada)
- Migrar `main.py` (sigue siendo grande) a varios módulos/widgets separados.
- Tests automatizados y CI.
- Soporte de adjuntos.
- Empaquetado a `.exe`/`.AppImage`/`.dmg` con icono embebido.
- Cifrado con contraseña maestra elegida por el usuario (en vez de clave
  local automática) para quien quiera protección más fuerte.
