import flet as ft
from estilos import *


def crear_tabla(datos):
    filas = []
    for fila in datos:
        color_estado = VERDE if fila[3] == "AUTORIZADO" else ROJO
        filas.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(fila[0], color=TEXTO)),
                    ft.DataCell(ft.Text(fila[1], color=TEXTO_SEC, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(fila[2], color=TEXTO)),
                    ft.DataCell(ft.Text(fila[3], color=color_estado, weight=ft.FontWeight.BOLD)),
                ]
            )
        )

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
        rows=filas,
    )


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