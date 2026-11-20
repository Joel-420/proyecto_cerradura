import flet as ft
from estilos import *
from tablas import crear_tabla, crear_panel_tabla


def crear_kpi(titulo, valor, icono):
    return ft.Container(
        expand=1,
        bgcolor=PANEL,
        padding=20,
        border_radius=16,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column(spacing=5, controls=[ft.Text(titulo, color=TEXTO_SEC), valor]),
                icono,
            ],
        ),
    )


def crear_vista_dashboard(controles, callbacks, tabla_dashboard):
    encabezado = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Column(
                spacing=3,
                controls=[
                    ft.Text("Dashboard", size=30, weight=ft.FontWeight.BOLD, color=TEXTO),
                    ft.Text("Supervisión de accesos y control remoto por MQTT", size=13, color=TEXTO_SEC),
                ],
            ),
            ft.Row(
                spacing=10,
                controls=[
                    ft.Button(content="Abrir Puerta", icon=ft.Icons.LOCK_OPEN, bgcolor=VERDE, color=FONDO, on_click=callbacks["abrir"]),
                    ft.Button(content="Cerrar Puerta", icon=ft.Icons.LOCK, bgcolor=ROJO, color=TEXTO, on_click=callbacks["cerrar"]),
                ],
            ),
        ],
    )

    tarjetas = ft.Row(
        spacing=15,
        controls=[
            crear_kpi("ESTADO PUERTA", controles["valor_estado"], controles["icono_estado"]),
            crear_kpi("INTENTOS FALLIDOS", controles["valor_intentos"], controles["icono_intentos"]),
            crear_kpi("ÚLTIMO ACCESO", controles["valor_metodo"], controles["icono_metodo"]),
        ],
    )

    panel_simulacion = ft.Container(
        bgcolor=PANEL,
        padding=15,
        border_radius=16,
        border=ft.Border.all(1, BORDE),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("Simulación de eventos ESP32:", size=13, weight=ft.FontWeight.BOLD, color=TEXTO_SEC),
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.OutlinedButton("Simular RFID Válido", icon=ft.Icons.NFC, on_click=callbacks["rfid"]),
                        ft.OutlinedButton("Simular PIN Erróneo", icon=ft.Icons.DIALPAD, on_click=callbacks["error_pin"]),
                        ft.OutlinedButton("Resetear Alarma", icon=ft.Icons.RESTART_ALT, on_click=callbacks["reset"]),
                    ],
                ),
            ],
        ),
    )

    return ft.Column(
        expand=True,
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        controls=[encabezado, tarjetas, panel_simulacion, crear_panel_tabla(tabla_dashboard)],
    )


def crear_vista_hardware(barra_intentos, lbl_rango_intentos):
    tarjetas_modulos = ft.Row(
        spacing=15,
        controls=[
            _tarjeta_modulo(ft.Icons.NFC, "Lector RFID RC522", "Estado: Operativo (SPI)"),
            _tarjeta_modulo(ft.Icons.DIALPAD, "Teclado Matricial 4x4", "Estado: Operativo (GPIO)"),
            _tarjeta_modulo(ft.Icons.WIFI, "Cliente MQTT", "Broker: broker.emqx.io"),
        ],
    )

    return ft.Column(
        expand=True,
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text("Hardware y Módulos", size=30, weight=ft.FontWeight.BOLD, color=TEXTO),
            ft.Text("Estado individual de periféricos conectados a la ESP32", color=TEXTO_SEC),
            ft.Container(
                bgcolor=PANEL,
                padding=25,
                border_radius=16,
                border=ft.Border.all(1, BORDE),
                content=ft.Column(
                    spacing=15,
                    controls=[
                        ft.Row([ft.Icon(ft.Icons.SHIELD, color=VERDE), ft.Text("Umbral de Bloqueo por Intentos Fallidos", size=18, weight=ft.FontWeight.BOLD, color=TEXTO)]),
                        barra_intentos,
                        lbl_rango_intentos,
                    ],
                ),
            ),
            tarjetas_modulos,
        ],
    )


def _tarjeta_modulo(icono, nombre, subtitulo):
    return ft.Container(
        expand=1,
        bgcolor=PANEL,
        padding=20,
        border_radius=16,
        border=ft.Border.all(1, BORDE),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Row([ft.Icon(icono, color=VERDE), ft.Text(nombre, weight=ft.FontWeight.BOLD, color=TEXTO)]),
                ft.Text(subtitulo, color=TEXTO_SEC, size=13),
            ],
        ),
    )


def crear_vista_registros(datos):
    tabla_completa = crear_tabla(datos)
    return tabla_completa, ft.Column(
        expand=True,
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text("Registros", size=30, weight=ft.FontWeight.BOLD, color=TEXTO),
            ft.Text("Historial completo de accesos y eventos de seguridad", color=TEXTO_SEC),
            ft.Container(
                bgcolor=PANEL,
                padding=20,
                border_radius=16,
                border=ft.Border.all(1, BORDE),
                content=ft.Row(scroll=ft.ScrollMode.AUTO, controls=[tabla_completa]),
            ),
        ],
    )


def crear_vista_configuracion(txt_nuevo_pin, btn_actualizar_pin, lbl_estado_pin, switch_alarmas):
    return ft.Column(
        expand=True,
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text("Configuraciones", size=30, weight=ft.FontWeight.BOLD, color=TEXTO),
            ft.Text("Parámetros de seguridad y notificaciones del sistema", color=TEXTO_SEC),
            ft.Container(
                bgcolor=PANEL,
                padding=25,
                border_radius=16,
                border=ft.Border.all(1, BORDE),
                content=ft.Column(
                    spacing=15,
                    controls=[
                        ft.Text("Establecer PIN de Acceso", size=18, weight=ft.FontWeight.BOLD, color=TEXTO),
                        ft.Row(spacing=15, vertical_alignment=ft.CrossAxisAlignment.START, controls=[txt_nuevo_pin, btn_actualizar_pin]),
                        lbl_estado_pin,
                        ft.Divider(color=BORDE),
                        switch_alarmas,
                    ],
                ),
            ),
        ],
    )