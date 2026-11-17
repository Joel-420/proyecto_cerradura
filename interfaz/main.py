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
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Icon(ft.Icons.SECURITY, color=VERDE, size=24),
                        ft.Text("Menú de Control", size=20, weight=ft.FontWeight.BOLD, color=TEXTO),
                    ],
                ),
                ft.Divider(color=BORDE),
                ft.Text("Estado del Sistema: Conectado", color=VERDE),
                ft.Text("Broker: broker.emqx.io", color=TEXTO_SEC, size=13),
                ft.Text("Modo: MQTT / Local", color=TEXTO_SEC, size=13),
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
        "Supervisión de accesos, seguridad y control remoto por MQTT",
        size=13,
        color=TEXTO_SEC,
    )

    encabezado = ft.Column(spacing=3, controls=[titulo, subtitulo])
    dashboard.controls.append(encabezado)
    dashboard.controls.append(ft.Divider(color=BORDE))

    # 4. Tarjetas KPI de estado e información
    def crear_kpi(titulo, valor, icono, color):
        return ft.Container(
            expand=1,
            bgcolor=PANEL,
            padding=20,
            border_radius=15,
            border=ft.Border.all(1, BORDE),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=5,
                        controls=[
                            ft.Text(titulo, size=12, weight=ft.FontWeight.BOLD, color=TEXTO_SEC),
                            valor,
                        ],
                    ),
                    ft.Icon(icono, color=color, size=32),
                ],
            ),
        )

    valor_estado = ft.Text("CERRADA", size=24, weight=ft.FontWeight.BOLD, color=ROJO)
    valor_intentos = ft.Text("0 / 3", size=24, weight=ft.FontWeight.BOLD, color=VERDE)
    valor_metodo = ft.Text("NINGUNO", size=24, weight=ft.FontWeight.BOLD, color=TEXTO)

    tarjetas = ft.Row(
        spacing=15,
        controls=[
            crear_kpi("ESTADO DE PUERTA", valor_estado, ft.Icons.LOCK, ROJO),
            crear_kpi("INTENTOS FALLIDOS", valor_intentos, ft.Icons.SHIELD, VERDE),
            crear_kpi("ÚLTIMO ACCESO", valor_metodo, ft.Icons.NFC, VERDE),
        ],
    )
    dashboard.controls.append(tarjetas)

    # 5. Botones de control y actualización de PIN
    btn_abrir = ft.Button(
        "ABRIR PUERTA",
        icon=ft.Icons.LOCK_OPEN,
        style=ft.ButtonStyle(
            bgcolor=VERDE,
            color=FONDO,
            padding=15,
        ),
    )
    btn_cerrar = ft.Button(
        "CERRAR PUERTA",
        icon=ft.Icons.LOCK,
        style=ft.ButtonStyle(
            bgcolor=ROJO,
            color=TEXTO,
            padding=15,
        ),
    )

    contenedor_botones = ft.Container(
        expand=1,
        bgcolor=PANEL,
        padding=20,
        border_radius=15,
        border=ft.Border.all(1, BORDE),
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Text("CONTROL REMOTO DE PUERTA", size=12, weight=ft.FontWeight.BOLD, color=TEXTO_SEC),
                ft.Row(
                    spacing=15,
                    controls=[btn_abrir, btn_cerrar],
                ),
            ],
        ),
    )

    txt_nuevo_pin = ft.TextField(
        label="Nuevo PIN (4 dígitos)",
        password=True,
        can_reveal_password=True,
        max_length=4,
        border_color=BORDE,
        focused_border_color=VERDE,
        width=200,
    )
    btn_actualizar_pin = ft.Button(
        "ESTABLECER PIN",
        icon=ft.Icons.KEY,
        style=ft.ButtonStyle(
            bgcolor=VERDE,
            color=TEXTO,
            padding=15,
        ),
    )
    lbl_estado_pin = ft.Text("PIN actual configurado: ****", size=12, color=TEXTO_SEC)

    contenedor_pin = ft.Container(
        expand=1,
        bgcolor=PANEL,
        padding=20,
        border_radius=15,
        border=ft.Border.all(1, BORDE),
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Text("CONFIGURACIÓN DE SEGURIDAD", size=12, weight=ft.FontWeight.BOLD, color=TEXTO_SEC),
                ft.Row(
                    spacing=15,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[txt_nuevo_pin, btn_actualizar_pin],
                ),
                lbl_estado_pin,
            ],
        ),
    )

    fila_controles = ft.Row(
        spacing=15,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[contenedor_botones, contenedor_pin],
    )
    dashboard.controls.append(fila_controles)

    # 6. Sección de registro de actividad
    titulo_logs = ft.Text(
        "Registro de Actividad",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=TEXTO,
    )
    lista_logs = ft.Column(
        spacing=8,
        controls=[
            ft.Text(
                "Esperando eventos de teclado, RFID o MQTT",
                size=14,
                color=TEXTO_SEC,
                font_family="monospace",
            ),
        ],
    )

    seccion_logs = ft.Container(
        bgcolor=PANEL,
        padding=20,
        border_radius=15,
        border=ft.Border.all(1, BORDE),
        content=ft.Column(
            spacing=10,
            controls=[
                titulo_logs,
                ft.Divider(color=BORDE),
                lista_logs,
            ],
        ),
    )
    dashboard.controls.append(seccion_logs)


ft.run(main)