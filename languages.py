IDIOMAS_DISPONIBLES = [
    ("es", "Español"),
    ("en", "English"),
]

_idioma_actual = "es"

_TEXTOS = {
    "titulo_app": {
        "es": "Gestor de Correo Temporal",
        "en": "Temporary Mail Manager",
    },
    "subtitulo_app": {
        "es": "Direcciones desechables para verificaciones y registros puntuales",
        "en": "Disposable addresses for one-off verifications and sign-ups",
    },
    "boton_ajustes": {
        "es": "⚙  Ajustes",
        "en": "⚙  Settings",
    },
    "listo": {
        "es": "Listo.",
        "en": "Ready.",
    },

    "encabezado_direcciones": {
        "es": "DIRECCIONES CREADAS",
        "en": "CREATED ADDRESSES",
    },
    "boton_nueva_direccion": {
        "es": "＋  Nueva dirección",
        "en": "＋  New address",
    },
    "boton_creando_direccion": {
        "es": "Creando dirección…",
        "en": "Creating address…",
    },
    "placeholder_buscar_direccion": {
        "es": "Buscar dirección…",
        "en": "Search address…",
    },
    "placeholder_direccion_actual": {
        "es": "Selecciona o crea una dirección",
        "en": "Select or create an address",
    },
    "boton_copiar": {
        "es": "Copiar",
        "en": "Copy",
    },
    "boton_exportar": {
        "es": "Exportar",
        "en": "Export",
    },
    "boton_eliminar": {
        "es": "Eliminar",
        "en": "Delete",
    },

    "encabezado_bandeja_entrada": {
        "es": "BANDEJA DE ENTRADA",
        "en": "INBOX",
    },
    "encabezado_historial": {
        "es": "HISTORIAL DE MENSAJES",
        "en": "MESSAGE HISTORY",
    },
    "boton_ver_historial": {
        "es": "Ver historial",
        "en": "View history",
    },
    "boton_actualizar": {
        "es": "Actualizar",
        "en": "Refresh",
    },
    "boton_esperar_mensaje": {
        "es": "Esperar mensaje nuevo",
        "en": "Wait for new message",
    },
    "boton_esperando_mensaje": {
        "es": "Esperando mensaje nuevo…",
        "en": "Waiting for new message…",
    },
    "placeholder_buscar_mensajes": {
        "es": "Buscar por remitente o asunto…",
        "en": "Search by sender or subject…",
    },
    "columna_remitente": {
        "es": "Remitente",
        "en": "Sender",
    },
    "columna_asunto": {
        "es": "Asunto",
        "en": "Subject",
    },
    "columna_recibido": {
        "es": "Recibido",
        "en": "Received",
    },
    "estado_vacio_titulo": {
        "es": "Ninguna dirección seleccionada",
        "en": "No address selected",
    },
    "estado_vacio_texto": {
        "es": "Crea o selecciona una dirección de la izquierda\npara ver su bandeja de entrada.",
        "en": "Create or select an address on the left\nto view its inbox.",
    },
    "codigo_detectado": {
        "es": "CÓDIGO DETECTADO",
        "en": "CODE DETECTED",
    },
    "boton_copiar_codigo": {
        "es": "Copiar código",
        "en": "Copy code",
    },

    "menu_mostrar_ventana": {
        "es": "Mostrar ventana",
        "en": "Show window",
    },
    "menu_salir": {
        "es": "Salir",
        "en": "Quit",
    },
    "notificacion_app_en_segundo_plano": {
        "es": "La aplicación sigue activa en la bandeja del sistema.",
        "en": "The app is still running in the system tray.",
    },

    "estado_creando_direccion": {
        "es": "Creando una nueva dirección de correo…",
        "en": "Creating a new email address…",
    },
    "estado_direccion_creada": {
        "es": "Dirección creada con {proveedor}: {direccion}",
        "en": "Address created with {proveedor}: {direccion}",
    },
    "estado_no_se_pudo_crear": {
        "es": "No se pudo crear la dirección.",
        "en": "The address could not be created.",
    },
    "error_no_se_pudo_crear_detalle": {
        "es": "No se pudo crear la dirección.\n\n{detalle}",
        "en": "The address could not be created.\n\n{detalle}",
    },
    "dialogo_seleccionar_direccion": {
        "es": "Selecciona primero una dirección de la lista.",
        "en": "Select an address from the list first.",
    },
    "dialogo_seleccionar_direccion_simple": {
        "es": "Selecciona primero una dirección.",
        "en": "Select an address first.",
    },
    "titulo_eliminar_direccion": {
        "es": "Eliminar dirección",
        "en": "Delete address",
    },
    "confirmar_eliminar_direccion": {
        "es": (
            "¿Quitar «{direccion}» de la lista?\n\n"
            "Esto solo elimina el registro local; la cuenta puede seguir "
            "existiendo en el proveedor. El historial de mensajes de esta "
            "dirección también se eliminará."
        ),
        "en": (
            "Remove \"{direccion}\" from the list?\n\n"
            "This only deletes the local record; the account may still "
            "exist with the provider. The message history for this "
            "address will also be deleted."
        ),
    },
    "estado_direccion_eliminada": {
        "es": "Dirección eliminada de la lista local.",
        "en": "Address removed from the local list.",
    },
    "estado_direccion_copiada": {
        "es": "Dirección copiada al portapapeles.",
        "en": "Address copied to clipboard.",
    },
    "estado_codigo_copiado": {
        "es": "Código copiado al portapapeles.",
        "en": "Code copied to clipboard.",
    },
    "titulo_exportar_direccion": {
        "es": "Exportar dirección",
        "en": "Export address",
    },
    "filtro_archivos_texto": {
        "es": "Archivos de texto (*.txt)",
        "en": "Text files (*.txt)",
    },
    "exportar_sin_contrasena": {
        "es": "(este proveedor no usa contraseña)",
        "en": "(this provider does not use a password)",
    },
    "exportar_desconocido": {
        "es": "Desconocido",
        "en": "Unknown",
    },
    "exportar_etiqueta_direccion": {
        "es": "Dirección",
        "en": "Address",
    },
    "exportar_etiqueta_contrasena": {
        "es": "Contraseña",
        "en": "Password",
    },
    "exportar_etiqueta_proveedor": {
        "es": "Proveedor",
        "en": "Provider",
    },
    "exportar_etiqueta_creada": {
        "es": "Creada",
        "en": "Created",
    },
    "error_no_se_pudo_guardar_archivo": {
        "es": "No se pudo guardar el archivo.\n\n{detalle}",
        "en": "The file could not be saved.\n\n{detalle}",
    },
    "estado_direccion_exportada": {
        "es": "Dirección exportada correctamente.",
        "en": "Address exported successfully.",
    },
    "estado_consultando_bandeja": {
        "es": "Consultando bandeja de entrada…",
        "en": "Checking inbox…",
    },
    "estado_n_mensajes": {
        "es": "{n} mensaje(s) en la bandeja.",
        "en": "{n} message(s) in the inbox.",
    },
    "estado_bandeja_vacia": {
        "es": "La bandeja está vacía por ahora.",
        "en": "The inbox is empty for now.",
    },
    "estado_no_se_pudo_actualizar_bandeja": {
        "es": "No se pudo actualizar la bandeja de entrada.",
        "en": "The inbox could not be refreshed.",
    },
    "estado_bandeja_actualizada": {
        "es": "Bandeja de entrada actualizada.",
        "en": "Inbox updated.",
    },
    "estado_cargando_mensaje": {
        "es": "Cargando mensaje…",
        "en": "Loading message…",
    },
    "estado_mensaje_cargado": {
        "es": "Mensaje cargado.",
        "en": "Message loaded.",
    },
    "estado_no_se_pudo_cargar_mensaje": {
        "es": "No se pudo cargar el contenido del mensaje.",
        "en": "The message content could not be loaded.",
    },
    "estado_sin_historial": {
        "es": "Todavía no hay historial guardado para esta dirección.",
        "en": "There is no saved history for this address yet.",
    },
    "estado_mostrando_historial": {
        "es": "Mostrando {n} mensaje(s) del historial.",
        "en": "Showing {n} message(s) from history.",
    },
    "estado_salir_de_historial": {
        "es": "Sal de la vista de historial para poder esperar un mensaje nuevo.",
        "en": "Exit history view to be able to wait for a new message.",
    },
    "estado_esperando_mensaje": {
        "es": "Esperando un mensaje nuevo para detectar el código automáticamente…",
        "en": "Waiting for a new message to detect the code automatically…",
    },
    "estado_no_llego_mensaje": {
        "es": "No llegó ningún mensaje nuevo en el tiempo de espera.",
        "en": "No new message arrived within the waiting time.",
    },
    "estado_llego_mensaje_nuevo": {
        "es": "Ha llegado un mensaje nuevo.",
        "en": "A new message has arrived.",
    },
    "estado_espera_detenida_error": {
        "es": "Se detuvo la espera por un error de conexión.",
        "en": "Waiting stopped due to a connection error.",
    },
    "notificacion_nuevo_mensaje_titulo": {
        "es": "Nuevo mensaje recibido",
        "en": "New message received",
    },
    "notificacion_nuevo_mensaje_cuerpo": {
        "es": "De: {remitente}\n{asunto}",
        "en": "From: {remitente}\n{asunto}",
    },
    "notificacion_nuevo_mensaje_cuerpo_extra": {
        "es": "De: {remitente}\n{asunto}{extra}",
        "en": "From: {remitente}\n{asunto}{extra}",
    },
    "notificacion_mas_mensajes": {
        "es": " (+{n} más)",
        "en": " (+{n} more)",
    },
    "historial_solo_resumen": {
        "es": (
            "Este mensaje procede del historial local y solo conserva el "
            "remitente, el asunto y la fecha; el proveedor no expone su "
            "cuerpo completo una vez ha sido archivado.\n\n"
            "Remitente: {remitente}\n"
            "Asunto: {asunto}"
        ),
        "en": (
            "This message comes from the local history and only keeps "
            "the sender, subject, and date; the provider does not expose "
            "its full body once it has been archived.\n\n"
            "Sender: {remitente}\n"
            "Subject: {asunto}"
        ),
    },
    "estado_ajustes_guardados": {
        "es": "Ajustes guardados correctamente.",
        "en": "Settings saved successfully.",
    },

    "titulo_dialogo_ajustes": {
        "es": "Ajustes",
        "en": "Settings",
    },
    "pestana_general": {
        "es": "General",
        "en": "General",
    },
    "pestana_tiempos": {
        "es": "Tiempos",
        "en": "Timing",
    },
    "pestana_avanzado": {
        "es": "Avanzado",
        "en": "Advanced",
    },
    "boton_cancelar": {
        "es": "Cancelar",
        "en": "Cancel",
    },
    "boton_guardar_cambios": {
        "es": "Guardar cambios",
        "en": "Save changes",
    },
    "ajuste_idioma_titulo": {
        "es": "Idioma",
        "en": "Language",
    },
    "ajuste_idioma_descripcion": {
        "es": "Cambia el idioma de toda la aplicación.",
        "en": "Changes the language of the whole application.",
    },
    "ajuste_tema_titulo": {
        "es": "Tema visual",
        "en": "Visual theme",
    },
    "ajuste_tema_descripcion": {
        "es": "Cambia la apariencia de toda la aplicación.",
        "en": "Changes the appearance of the whole application.",
    },
    "tema_claro": {
        "es": "Claro",
        "en": "Light",
    },
    "tema_oscuro": {
        "es": "Oscuro",
        "en": "Dark",
    },
    "ajuste_proveedor_titulo": {
        "es": "Proveedor de correo",
        "en": "Mail provider",
    },
    "ajuste_proveedor_descripcion": {
        "es": (
            "En modo automático, si un proveedor falla al crear la dirección "
            "se prueba con el siguiente disponible."
        ),
        "en": (
            "In automatic mode, if a provider fails to create the address, "
            "the next available one is tried."
        ),
    },
    "proveedor_automatico": {
        "es": "Automático (recomendado)",
        "en": "Automatic (recommended)",
    },
    "ajuste_notificaciones_titulo": {
        "es": "Notificaciones de escritorio",
        "en": "Desktop notifications",
    },
    "ajuste_notificaciones_descripcion": {
        "es": "Avisa cuando llega un mensaje nuevo, aunque la ventana esté minimizada.",
        "en": "Notifies you when a new message arrives, even if the window is minimized.",
    },
    "activadas": {
        "es": "Activadas",
        "en": "Enabled",
    },
    "ajuste_minimizar_bandeja_titulo": {
        "es": "Minimizar a la bandeja del sistema",
        "en": "Minimize to system tray",
    },
    "ajuste_minimizar_bandeja_descripcion": {
        "es": "Al cerrar la ventana, la aplicación sigue activa en segundo plano.",
        "en": "When you close the window, the app keeps running in the background.",
    },
    "activado": {
        "es": "Activado",
        "en": "Enabled",
    },
    "ajuste_guardar_historial_titulo": {
        "es": "Guardar historial de mensajes",
        "en": "Save message history",
    },
    "ajuste_guardar_historial_descripcion": {
        "es": "Conserva una copia local de los correos recibidos por cada dirección.",
        "en": "Keeps a local copy of received emails for each address.",
    },
    "ajuste_auto_copiar_titulo": {
        "es": "Copiar el código automáticamente",
        "en": "Automatically copy the code",
    },
    "ajuste_auto_copiar_descripcion": {
        "es": "En cuanto se detecte un código de verificación, se copia solo al portapapeles.",
        "en": "As soon as a verification code is detected, it's copied to the clipboard automatically.",
    },
    "ajuste_sonido_titulo": {
        "es": "Sonido de aviso",
        "en": "Alert sound",
    },
    "ajuste_sonido_descripcion": {
        "es": "Reproduce un aviso sonoro cuando llega un mensaje nuevo.",
        "en": "Plays an alert sound when a new message arrives.",
    },
    "ajuste_autoactualizacion_titulo": {
        "es": "Intervalo de autoactualización",
        "en": "Auto-refresh interval",
    },
    "ajuste_autoactualizacion_descripcion": {
        "es": "Cada cuánto se comprueba la bandeja de entrada en segundo plano.",
        "en": "How often the inbox is checked in the background.",
    },
    "ajuste_frecuencia_espera_titulo": {
        "es": "Frecuencia al esperar un código",
        "en": "Frequency while waiting for a code",
    },
    "ajuste_frecuencia_espera_descripcion": {
        "es": "Cada cuánto se consulta el servidor mientras usas «Esperar mensaje nuevo».",
        "en": "How often the server is checked while using \"Wait for new message\".",
    },
    "ajuste_tiempo_maximo_titulo": {
        "es": "Tiempo máximo de espera",
        "en": "Maximum waiting time",
    },
    "ajuste_tiempo_maximo_descripcion": {
        "es": (
            "Tras cuánto tiempo se cancela automáticamente la espera de un "
            "mensaje nuevo si no llega nada."
        ),
        "en": (
            "After how long the wait for a new message is automatically "
            "canceled if nothing arrives."
        ),
    },
    "ajuste_patron_titulo": {
        "es": "Patrón de detección de código (expresión regular)",
        "en": "Code detection pattern (regular expression)",
    },
    "ajuste_patron_descripcion": {
        "es": (
            "Opcional. Si algún servicio concreto usa un formato de código que "
            "la detección automática no reconoce bien, define aquí tu propia "
            "expresión regular. Déjalo en blanco para usar la detección estándar."
        ),
        "en": (
            "Optional. If a specific service uses a code format that automatic "
            "detection doesn't recognize well, define your own regular "
            "expression here. Leave it blank to use standard detection."
        ),
    },
    "ajuste_patron_placeholder": {
        "es": r"Ejemplo: \b[A-Z]{3}-\d{4}\b",
        "en": r"Example: \b[A-Z]{3}-\d{4}\b",
    },
    "error_regex_invalida": {
        "es": "Esa expresión regular no es válida. Corrígela o déjala en blanco.",
        "en": "That regular expression is not valid. Fix it or leave it blank.",
    },

    "titulo_advertencia_almacenamiento": {
        "es": "Aviso sobre datos guardados",
        "en": "Notice about saved data",
    },
    "caducidad_desconocida": {
        "es": "sin caducidad conocida",
        "en": "no known expiration",
    },
    "caducidad_restante": {
        "es": "≈{min} min restantes (estimado)",
        "en": "≈{min} min left (estimated)",
    },
    "caducidad_expirada": {
        "es": "puede haber caducado",
        "en": "may have expired",
    },
    "estado_codigo_copiado_auto": {
        "es": "Código detectado y copiado automáticamente al portapapeles.",
        "en": "Code detected and automatically copied to the clipboard.",
    },
}


def establecer_idioma(codigo):
    global _idioma_actual
    if codigo in ("es", "en"):
        _idioma_actual = codigo


def idioma_actual():
    return _idioma_actual


def t(clave, **kwargs):
    entrada = _TEXTOS.get(clave)
    if entrada is None:
        return clave
    texto = entrada.get(_idioma_actual, entrada.get("es", clave))
    if kwargs:
        try:
            return texto.format(**kwargs)
        except (KeyError, IndexError):
            return texto
    return texto
