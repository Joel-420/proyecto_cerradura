import flet as ft
from estilos import *


def main(page: ft.Page):
    # Configuración de ventana o frame
    page.window.width = 1200
    page.window.height = 720
    page.bgcolor = FONDO
    page.window.min_height = 600
    page.window.min_width = 900
    page.title = "Cerradura Inteligente - Panel de Control"
    page.theme_mode = ft.ThemeMode.DARK

    # 1. Barra lateral
    barra_lateral = ft.Container(
        width=260,
        bgcolor=PANEL,
        padding=20,
        border_radius=15,
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Text("Menú de Control", size=20, weight=ft.FontWeight.BOLD, color=TEXTO),
                ft.Divider(),
                ft.Text("Estado del Sistema: Conectado", color=VERDE),
                ft.Text("Modo: MQTT / Local", color=TEXTO_SEC),
            ],
        ),
    )

    # 2. Área principal y Dashboard con scroll
    dashboard = ft.Column(
        expand=True,
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
    )

    area_principal = ft.Container(
        expand=True,
        padding=30,
        content=dashboard,
    )

    estructura = ft.Row(
        expand=True,
        spacing=0,
        controls=[barra_lateral, area_principal],
    )
    page.add(estructura)

    # 3. Encabezado
    titulo = ft.Text(
        "Panel de Control de Cerradura",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=TEXTO,
    )
    subtitulo = ft.Text(
        "Supervisión de accesos y control remoto por MQTT",
        size=13,
        color=TEXTO_SEC,
    )

    encabezado = ft.Column(spacing=3, controls=[titulo, subtitulo])
    dashboard.controls.append(encabezado)
    dashboard.controls.append(ft.Divider())

    # 4. Etiquetas de estado e información
    lbl_estado_puerta = ft.Text(
        "Estado actual: CERRADA",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=ROJO,
    )
    lbl_ultimo_evento = ft.Text(
        "Último evento: Ninguno registrado",
        size=16,
        color=TEXTO_SEC,
    )

    seccion_estado = ft.Container(
        bgcolor=PANEL,
        padding=20,
        border_radius=15,
        content=ft.Column(
            spacing=10,
            controls=[
                lbl_estado_puerta,
                lbl_ultimo_evento,
            ],
        ),
    )
    dashboard.controls.append(seccion_estado)

    # 5. Botones de control
    btn_abrir = ft.Button(
        "ABRIR PUERTA",
        style=ft.ButtonStyle(
            bgcolor=VERDE,
            color=TEXTO,
        ),
    )
    btn_cerrar = ft.Button(
        "CERRAR PUERTA",
        style=ft.ButtonStyle(
            bgcolor=ROJO,
            color=TEXTO,
        ),
    )

    contenedor_botones = ft.Container(
        bgcolor=PANEL,
        padding=20,
        border_radius=15,
        content=ft.Row(
            spacing=20,
            controls=[btn_abrir, btn_cerrar],
        ),
    )
    dashboard.controls.append(contenedor_botones)

    # 6. Sección de registro de actividad
    titulo_logs = ft.Text(
        "Registro de Actividad",
        size=18,
        weight=ft.FontWeight.BOLD
    )
    lbl_logs = ft.Text(
        "Esperando eventos de teclado, RFID o MQTT",
        size=14,
        color=TEXTO_SEC,
    )

    seccion_logs = ft.Container(
        bgcolor = PANEL,
        padding=20,
        border_radius=15,
        content=ft.Column(
            spacing=10,
            controls=[
                titulo_logs,
                ft.Divider(),
                lbl_logs,
            ],
        ),
    )
    dashboard.controls.append(seccion_logs)


ft.run(main)