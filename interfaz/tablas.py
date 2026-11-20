import flet as ft
from estilos import *


def crear_fila_datos(registro):
    hora, metodo, detalle, estado_evento = registro
    color_estado = VERDE if estado_evento == "AUTORIZADO" else ROJO
    return ft.DataRow(
        cells=[
            ft.DataCell(ft.Text(hora, color=TEXTO)),
            ft.DataCell(ft.Text(metodo, color=TEXTO_SEC, weight=ft.FontWeight.BOLD)),
            ft.DataCell(ft.Text(detalle, color=TEXTO)),
            ft.DataCell(ft.Text(estado_evento, color=color_estado, weight=ft.FontWeight.BOLD)),
        ]
    )


def crear_tabla(datos):
    return ft.DataTable(
        heading_row_color=PANEL_2,
        border=ft.Border.all(1, BORDE),
        border_radius=12,
        columns=[
            ft.DataColumn(ft.Text("Hora", weight=ft.FontWeight.BOLD, color=TEXTO_SEC)),
            ft.DataColumn(ft.Text("Método", weight=ft.FontWeight.BOLD, color=TEXTO_SEC)),
            ft.DataColumn(ft.Text("Detalle del Evento", weight=ft.FontWeight.BOLD, color=TEXTO_SEC)),
            ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD, color=TEXTO_SEC)),
        ],
        rows=[crear_fila_datos(fila) for fila in datos],
    )


def agregar_fila_tabla(tabla, registro, limite=None):
    tabla.rows.insert(0, crear_fila_datos(registro))
    if limite and len(tabla.rows) > limite:
        tabla.rows.pop()


def crear_panel_tabla(tabla):
    return ft.Container(
        bgcolor=PANEL,
        padding=20,
        border_radius=16,
        border=ft.Border.all(1, BORDE),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("Últimos Eventos de Acceso", size=18, weight=ft.FontWeight.BOLD, color=TEXTO),
                ft.Row(scroll=ft.ScrollMode.AUTO, controls=[tabla]),
            ],
        ),
    )