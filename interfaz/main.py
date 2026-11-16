import flet as ft


def main(page: ft.Page):
    # Configuración de ventana o frame
    page.window.width = 1200
    page.window.height = 720
    page.window.min_height = 600
    page.window.min_width = 900
    page.title = "Cerradura Inteligente - Panel de Control"
    page.theme_mode = ft.ThemeMode.DARK

    # 1. Barra lateral
    barra_lateral = ft.Container(
        width=260,
        padding=20,
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Text("Menú de Control", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Estado del Sistema: Conectado"),
                ft.Text("Modo: MQTT / Local"),
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
    )
    subtitulo = ft.Text(
        "Supervisión de accesos y control remoto por MQTT",
        size=13,
    )

    encabezado = ft.Column(spacing=3, controls=[titulo, subtitulo])
    dashboard.controls.append(encabezado)
    dashboard.controls.append(ft.Divider())

    # 4. Etiquetas de estado e información
    lbl_estado_puerta = ft.Text(
        "Estado actual: CERRADA",
        size=22,
        weight=ft.FontWeight.BOLD,
    )
    lbl_ultimo_evento = ft.Text(
        "Último evento: Ninguno registrado",
        size=16,
    )

    seccion_estado = ft.Column(
        spacing=10,
        controls=[
            lbl_estado_puerta,
            lbl_ultimo_evento,
        ],
    )
    dashboard.controls.append(seccion_estado)
    dashboard.controls.append(ft.Divider())

    # 5. Botones de control (Sintaxis actual: ft.Button)
    btn_abrir = ft.Button("ABRIR PUERTA")
    btn_cerrar = ft.Button("CERRAR PUERTA")

    contenedor_botones = ft.Row(
        spacing=20,
        controls=[btn_abrir, btn_cerrar],
    )
    dashboard.controls.append(contenedor_botones)
    dashboard.controls.append(ft.Divider())

    # 6. Sección de registro de actividad (Logs)
    titulo_logs = ft.Text(
        "Registro de Actividad",
        size=18,
        weight=ft.FontWeight.BOLD,
    )
    lbl_logs = ft.Text(
        "Esperando eventos de teclado, RFID o MQTT",
        size=14,
    )

    seccion_logs = ft.Column(
        spacing=10,
        controls=[
            titulo_logs,
            lbl_logs,
        ],
    )
    dashboard.controls.append(seccion_logs)


ft.run(main)