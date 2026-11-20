from datetime import datetime
from pathlib import Path
import flet as ft
from estilos import *
from tablas import crear_tabla, crear_panel_tabla
from vistas import crear_vista_hardware, crear_vista_registros, crear_vista_configuracion
from navegacion import crear_navegacion


def main(page: ft.Page):

    estado = {
        "intentos_fallidos": 0,
        "bloqueado": False,
        "pin_actual": "1234",
    }

    datos_registros = [
        ["08:00:00", "SISTEMA", "Panel de control inicializado", "AUTORIZADO"],
    ]


    def agregar_registro(metodo, detalle, estado_evento):
        hora = datetime.now().strftime("%H:%M:%S")
        datos_registros.insert(0, [hora, metodo, detalle, estado_evento])

        color_estado = VERDE if estado_evento == "AUTORIZADO" else ROJO
        nueva_fila = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(hora, color=TEXTO)),
                ft.DataCell(ft.Text(metodo, color=TEXTO_SEC, weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text(detalle, color=TEXTO)),
                ft.DataCell(ft.Text(estado_evento, color=color_estado, weight=ft.FontWeight.BOLD)),
            ]
        )


        tabla_dashboard.rows.insert(0, nueva_fila)
        if len(tabla_dashboard.rows) > 6:
            tabla_dashboard.rows.pop()

        tabla_completa.rows.insert(
            0,
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(hora, color=TEXTO)),
                    ft.DataCell(ft.Text(metodo, color=TEXTO_SEC, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(detalle, color=TEXTO)),
                    ft.DataCell(ft.Text(estado_evento, color=color_estado, weight=ft.FontWeight.BOLD)),
                ]
            ),
        )

    def actualizar_estado_puerta(abierta, metodo):
        if abierta:
            valor_estado.value = "ABIERTA"
            valor_estado.color = VERDE
            icono_estado.name = ft.Icons.LOCK_OPEN
            icono_estado.color = VERDE
        else:
            valor_estado.value = "CERRADA"
            valor_estado.color = ROJO
            icono_estado.name = ft.Icons.LOCK
            icono_estado.color = ROJO
        valor_metodo.value = metodo

    def abrir_puerta(e):
        if estado["bloqueado"]:
            agregar_registro("PANEL", "Apertura denegada: sistema bloqueado", "DENEGADO")
            return
        actualizar_estado_puerta(True, "MQTT / PANEL")
        agregar_registro("PANEL", "Apertura remota ejecutada", "AUTORIZADO")

    def cerrar_puerta(e):
        actualizar_estado_puerta(False, "MQTT / PANEL")
        agregar_registro("PANEL", "Cierre remoto ejecutado", "AUTORIZADO")

    def simular_rfid(e):
        if estado["bloqueado"]:
            agregar_registro("RFID", "Lectura ignorada por bloqueo", "DENEGADO")
            return
        estado["intentos_fallidos"] = 0
        valor_intentos.value = "0 / 3"
        valor_intentos.color = VERDE
        barra_intentos.value = 0.0
        barra_intentos.color = VERDE
        lbl_rango_intentos.value = "0% del umbral de bloqueo (0 / 3 intentos)"

        actualizar_estado_puerta(True, "RFID")
        agregar_registro("RFID", "Tarjeta autorizada (UID: A4F2)", "AUTORIZADO")

    def simular_error_teclado(e):
        if estado["bloqueado"]:
            agregar_registro("TECLADO", "Teclado bloqueado por seguridad", "DENEGADO")
            return

        estado["intentos_fallidos"] += 1
        intentos = estado["intentos_fallidos"]
        valor_intentos.value = f"{intentos} / 3"
        barra_intentos.value = intentos / 3
        lbl_rango_intentos.value = f"{int((intentos / 3) * 100)}% del umbral de bloqueo ({intentos} / 3 intentos)"

        if intentos >= 3 and switch_alarmas.value:
            estado["bloqueado"] = True
            valor_intentos.color = ROJO
            barra_intentos.color = ROJO
            actualizar_estado_puerta(False, "BLOQUEADO")
            agregar_registro("ALARMA", "3 intentos fallidos: sistema bloqueado", "DENEGADO")
        else:
            valor_intentos.color = AMARILLO
            barra_intentos.color = AMARILLO
            agregar_registro("TECLADO", f"PIN incorrecto ({intentos}/3)", "DENEGADO")

    def resetear_alarma(e):
        estado["bloqueado"] = False
        estado["intentos_fallidos"] = 0
        valor_intentos.value = "0 / 3"
        valor_intentos.color = VERDE
        barra_intentos.value = 0.0
        barra_intentos.color = VERDE
        lbl_rango_intentos.value = "0% del umbral de bloqueo (0 / 3 intentos)"
        agregar_registro("SISTEMA", "Bloqueo restablecido por administrador", "AUTORIZADO")

    def establecer_pin(e):
        nuevo_pin = txt_nuevo_pin.value.strip()
        if len(nuevo_pin) != 4 or not nuevo_pin.isdigit():
            txt_nuevo_pin.error_text = "Ingrese 4 dígitos numéricos"
            agregar_registro("SEGURIDAD", "Intento de cambio de PIN inválido", "DENEGADO")
            return

        txt_nuevo_pin.error_text = None
        estado["pin_actual"] = nuevo_pin
        txt_nuevo_pin.value = ""
        lbl_estado_pin.value = "PIN actual configurado: **** (Actualizado)"
        lbl_estado_pin.color = VERDE
        agregar_registro("SEGURIDAD", "Nuevo PIN maestro sincronizado", "AUTORIZADO")

    def cambiar_seccion(e):
        indice = e.control.selected_index
        area_principal.content = vistas[indice]

    # --- CONFIGURACIÓN DE VENTANA Y ASSETS ---
    ruta_logo = Path(__file__).parent/"assets"/"logo.png"
    logo = (
        ft.Image(src="logo.png", width=110, height=110, fit=ft.BoxFit.CONTAIN)
        if ruta_logo.exists()
        else ft.Icon(ft.Icons.SECURITY, color=VERDE, size=48)
    )

    ruta_icono = Path(__file__).parent/"assets"/"app.ico"
    if ruta_icono.exists():
        page.window.icon = str(ruta_icono)

    page.window.width = 1200
    page.window.height = 720
    page.bgcolor = FONDO
    page.window.min_height = 600
    page.window.min_width = 900
    page.title = "Cerradura Inteligente - Panel de Control"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ESTRUCTURA PRINCIPAL ---
    barra_lateral = ft.Container(
        width=230,
        bgcolor=PANEL,
        padding=20,
        border_radius=15,
    )

    area_principal = ft.Container(
        expand=True,
        padding=30,
    )

    page.add(
        ft.Row(
            expand=True,
            spacing=0,
            controls=[barra_lateral, area_principal],
        )
    )

    dashboard = ft.Column(
        expand=True,
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
    )
    area_principal.content = dashboard

    # --- ENCABEZADO DEL DASHBOARD ---
    btn_abrir = ft.Button(
        content="Abrir Puerta",
        icon=ft.Icons.LOCK_OPEN,
        bgcolor=VERDE,
        color=FONDO,
        on_click=abrir_puerta,
    )
    btn_cerrar = ft.Button(
        content="Cerrar Puerta",
        icon=ft.Icons.LOCK,
        bgcolor=ROJO,
        color=TEXTO,
        on_click=cerrar_puerta,
    )

    encabezado_dashboard = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Column(
                spacing=3,
                controls=[
                    ft.Text("Dashboard", size=30, weight=ft.FontWeight.BOLD, color=TEXTO),
                    ft.Text("Supervisión de accesos y control remoto por MQTT", size=13, color=TEXTO_SEC),
                ],
            ),
            ft.Row(spacing=10, controls=[btn_abrir, btn_cerrar]),
        ],
    )
    dashboard.controls.append(encabezado_dashboard)

    # --- TARJETAS KPI ---
    def crear_kpi(titulo, valor, icono):
        return ft.Container(
            expand=1,
            bgcolor=PANEL,
            padding=20,
            border_radius=16,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=5,
                        controls=[ft.Text(titulo, color=TEXTO_SEC), valor],
                    ),
                    icono,
                ],
            ),
        )

    valor_estado = ft.Text("CERRADA", size=26, weight=ft.FontWeight.BOLD, color=ROJO)
    icono_estado = ft.Icon(ft.Icons.LOCK, color=ROJO, size=32)

    valor_intentos = ft.Text("0 / 3", size=26, weight=ft.FontWeight.BOLD, color=VERDE)
    icono_intentos = ft.Icon(ft.Icons.SHIELD, color=VERDE, size=32)

    valor_metodo = ft.Text("SISTEMA", size=26, weight=ft.FontWeight.BOLD, color=TEXTO)
    icono_metodo = ft.Icon(ft.Icons.NFC, color=VERDE, size=32)

    tarjetas = ft.Row(
        spacing=15,
        controls=[
            crear_kpi("ESTADO PUERTA", valor_estado, icono_estado),
            crear_kpi("INTENTOS FALLIDOS", valor_intentos, icono_intentos),
            crear_kpi("ÚLTIMO ACCESO", valor_metodo, icono_metodo),
        ],
    )
    dashboard.controls.append(tarjetas)

    # --- BARRA DE SIMULACIÓN DE HARDWARE  ---
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
                        ft.OutlinedButton("Simular RFID Válido", icon=ft.Icons.NFC, on_click=simular_rfid),
                        ft.OutlinedButton("Simular PIN Erróneo", icon=ft.Icons.DIALPAD, on_click=simular_error_teclado),
                        ft.OutlinedButton("Resetear Alarma", icon=ft.Icons.RESTART_ALT, on_click=resetear_alarma),
                    ],
                ),
            ],
        ),
    )
    dashboard.controls.append(panel_simulacion)

    # --- TABLA DE REGISTROS EN DASHBOARD ---
    tabla_dashboard = crear_tabla(datos_registros)
    panel_tabla = crear_panel_tabla(tabla_dashboard)
    dashboard.controls.append(panel_tabla)

    # --- CONTROLES COMPARTIDOS CON LAS VISTAS SECUNDARIAS ---
    barra_intentos = ft.ProgressBar(value=0.0, color=VERDE, bgcolor=PANEL_2)
    lbl_rango_intentos = ft.Text("0% del umbral de bloqueo (0 / 3 intentos)", color=TEXTO_SEC)

    txt_nuevo_pin = ft.TextField(
        label="Nuevo PIN (4 dígitos)",
        password=True,
        can_reveal_password=True,
        max_length=4,
        border_color=BORDE,
        focused_border_color=VERDE,
        width=220,
    )
    btn_actualizar_pin = ft.Button(
        content="Establecer PIN",
        icon=ft.Icons.KEY,
        bgcolor=VERDE,
        color=FONDO,
        on_click=establecer_pin,
    )
    lbl_estado_pin = ft.Text("PIN actual configurado: ****", size=13, color=TEXTO_SEC)
    switch_alarmas = ft.Switch(label="Activar bloqueo automático por intentos fallidos", value=True, active_color=VERDE)

    # --- CONSTRUCCIÓN DE VISTAS Y NAVEGACIÓN ---
    hardware = crear_vista_hardware(barra_intentos, lbl_rango_intentos)
    tabla_completa, registros = crear_vista_registros(datos_registros)
    configuracion = crear_vista_configuracion(txt_nuevo_pin, btn_actualizar_pin, lbl_estado_pin, switch_alarmas)

    vistas = [dashboard, hardware, registros, configuracion]
    navegacion = crear_navegacion(cambiar_seccion, logo)
    barra_lateral.content = navegacion


ft.run(main, assets_dir="assets")