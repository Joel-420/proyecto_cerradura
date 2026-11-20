from pathlib import Path
import flet as ft
from estilos import *
from controlador import ControladorCerradura
from tablas import crear_tabla, agregar_fila_tabla
from vistas import crear_vista_dashboard,crear_vista_hardware,crear_vista_registros,crear_vista_configuracion
from navegacion import crear_navegacion


def main(page: ft.Page):
    ctrl = ControladorCerradura(max_intentos=3)

    def cambiar_seccion(e):
        indice = e.control.selected_index
        area_principal.content = vistas[indice]
    # --- elementos en constante cambio ---
    controles_kpi = {
        "valor_estado": ft.Text("CERRADA", size=26, weight=ft.FontWeight.BOLD, color=ROJO),
        "icono_estado": ft.Icon(ft.Icons.LOCK, color=ROJO, size=32),
        "valor_intentos": ft.Text("0 / 3", size=26, weight=ft.FontWeight.BOLD, color=VERDE),
        "icono_intentos": ft.Icon(ft.Icons.SHIELD, color=VERDE, size=32),
        "valor_metodo": ft.Text("SISTEMA", size=26, weight=ft.FontWeight.BOLD, color=TEXTO),
        "icono_metodo": ft.Icon(ft.Icons.NFC, color=VERDE, size=32),
    }

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
    lbl_estado_pin = ft.Text("PIN actual configurado: ****", size=13, color=TEXTO_SEC)
    switch_alarmas = ft.Switch(label="Activar bloqueo automático por intentos fallidos", value=True, active_color=VERDE)

    tabla_dashboard = crear_tabla(ctrl.registros)
    tabla_completa, vista_registros = crear_vista_registros(ctrl.registros)

    # --- sincronizar o actualizar las vistas ---
    def sincronizar_vista(registro):
        agregar_fila_tabla(tabla_dashboard, registro, limite=6)
        agregar_fila_tabla(tabla_completa, registro)

        # Estado puerta
        abierta = ctrl.puerta_abierta
        controles_kpi["valor_estado"].value = "ABIERTA" if abierta else "CERRADA"
        controles_kpi["valor_estado"].color = VERDE if abierta else ROJO
        controles_kpi["icono_estado"].name = ft.Icons.LOCK_OPEN if abierta else ft.Icons.LOCK
        controles_kpi["icono_estado"].color = VERDE if abierta else ROJO
        controles_kpi["valor_metodo"].value = ctrl.ultimo_metodo

        # Intentos y seguridad
        intentos = ctrl.intentos_fallidos
        max_int = ctrl.max_intentos
        color_seg = ROJO if ctrl.bloqueado else (AMARILLO if intentos > 0 else VERDE)

        controles_kpi["valor_intentos"].value = f"{intentos} / {max_int}"
        controles_kpi["valor_intentos"].color = color_seg
        barra_intentos.value = intentos / max_int
        barra_intentos.color = color_seg
        lbl_rango_intentos.value = f"{int((intentos / max_int) * 100)}% del umbral de bloqueo ({intentos} / {max_int} intentos)"

    # --- MANEJADORES DE EVENTOS ---
    def on_abrir(e):
        _, reg = ctrl.abrir_puerta()
        sincronizar_vista(reg)

    def on_cerrar(e):
        _, reg = ctrl.cerrar_puerta()
        sincronizar_vista(reg)

    def on_rfid(e):
        _, reg = ctrl.simular_rfid_valido()
        sincronizar_vista(reg)

    def on_error_pin(e):
        reg = ctrl.registrar_intento_fallido(activar_alarma=switch_alarmas.value)
        sincronizar_vista(reg)

    def on_reset(e):
        reg = ctrl.resetear_alarma()
        sincronizar_vista(reg)

    def on_establecer_pin(e):
        valido, msg_error, reg = ctrl.cambiar_pin(txt_nuevo_pin.value)
        txt_nuevo_pin.error_text = msg_error if not valido else None
        if valido:
            txt_nuevo_pin.value = ""
            lbl_estado_pin.value = "PIN actual configurado: **** (Actualizado)"
            lbl_estado_pin.color = VERDE
        sincronizar_vista(reg)

    # --- VENTANA Y NAVEGACIÓN ---
    page.window.width = 1200
    page.window.height = 720
    page.bgcolor = FONDO
    page.window.min_height = 600
    page.window.min_width = 900
    page.title = "Cerradura Inteligente - Panel de Control"
    page.theme_mode = ft.ThemeMode.DARK

    ruta_logo = Path(__file__).parent / "assets" / "logo.png"
    logo = ft.Image(src="logo.png", width=110, height=110, fit=ft.BoxFit.CONTAIN) if ruta_logo.exists() else ft.Icon(ft.Icons.SECURITY, color=VERDE, size=48)

    callbacks = {"abrir": on_abrir, "cerrar": on_cerrar, "rfid": on_rfid, "error_pin": on_error_pin, "reset": on_reset}
    btn_pin = ft.Button(content="Establecer PIN", icon=ft.Icons.KEY, bgcolor=VERDE, color=FONDO, on_click=on_establecer_pin)

    vistas = [
        crear_vista_dashboard(controles_kpi, callbacks, tabla_dashboard),
        crear_vista_hardware(barra_intentos, lbl_rango_intentos),
        vista_registros,
        crear_vista_configuracion(txt_nuevo_pin, btn_pin, lbl_estado_pin, switch_alarmas),
    ]

    area_principal = ft.Container(
        expand=True,
        padding=30,
        content=vistas[0],
    )

    navegacion = crear_navegacion(cambiar_seccion, logo)

    barra_lateral = ft.Container(
        width=230,
        bgcolor=PANEL,
        padding=20,
        border_radius=15,
        content=navegacion,
    )

    page.add(
        ft.Row(
            expand=True,
            spacing=0,
            controls=[barra_lateral, area_principal],
        )
    )


ft.run(main, assets_dir="assets")