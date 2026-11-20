import flet as ft
from estilos import *
from tablas import crear_tabla


def crear_vista_hardware(barra_intentos, lbl_rango_intentos):
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
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.SHIELD, color=VERDE),
                                ft.Text("Umbral de Bloqueo por Intentos Fallidos", size=18, weight=ft.FontWeight.BOLD, color=TEXTO),
                            ]
                        ),
                        barra_intentos,
                        lbl_rango_intentos,
                    ],
                ),
            ),
            ft.Row(
                spacing=15,
                controls=[
                    ft.Container(
                        expand=1,
                        bgcolor=PANEL,
                        padding=20,
                        border_radius=16,
                        border=ft.Border.all(1, BORDE),
                        content=ft.Column(
                            spacing=8,
                            controls=[
                                ft.Row([ft.Icon(ft.Icons.NFC, color=VERDE), ft.Text("Lector RFID RC522", weight=ft.FontWeight.BOLD, color=TEXTO)]),
                                ft.Text("Estado: Operativo (SPI)", color=TEXTO_SEC, size=13),
                            ],
                        ),
                    ),
                    ft.Container(
                        expand=1,
                        bgcolor=PANEL,
                        padding=20,
                        border_radius=16,
                        border=ft.Border.all(1, BORDE),
                        content=ft.Column(
                            spacing=8,
                            controls=[
                                ft.Row([ft.Icon(ft.Icons.DIALPAD, color=VERDE), ft.Text("Teclado Matricial 4x4", weight=ft.FontWeight.BOLD, color=TEXTO)]),
                                ft.Text("Estado: Operativo (GPIO)", color=TEXTO_SEC, size=13),
                            ],
                        ),
                    ),
                    ft.Container(
                        expand=1,
                        bgcolor=PANEL,
                        padding=20,
                        border_radius=16,
                        border=ft.Border.all(1, BORDE),
                        content=ft.Column(
                            spacing=8,
                            controls=[
                                ft.Row([ft.Icon(ft.Icons.WIFI, color=VERDE), ft.Text("Cliente MQTT", weight=ft.FontWeight.BOLD, color=TEXTO)]),
                                ft.Text("Broker: broker.emqx.io", color=TEXTO_SEC, size=13),
                            ],
                        ),
                    ),
                ],
            ),
        ],
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
                content=ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    controls=[tabla_completa],
                ),
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
                        ft.Row(
                            spacing=15,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            controls=[txt_nuevo_pin, btn_actualizar_pin],
                        ),
                        lbl_estado_pin,
                        ft.Divider(color=BORDE),
                        switch_alarmas,
                    ],
                ),
            ),
        ],
    )