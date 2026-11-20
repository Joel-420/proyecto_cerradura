import flet as ft
from estilos import *


def crear_navegacion(cambiar_seccion, logo=None):
    return ft.NavigationRail(
        selected_index=0,
        extended=True,
        min_extended_width=210,
        bgcolor=PANEL,
        leading=logo,
        on_change=cambiar_seccion,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DASHBOARD_OUTLINED,
                selected_icon=ft.Icons.DASHBOARD,
                label="Dashboard",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SENSORS,
                label="Hardware / Módulos",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.TABLE_CHART,
                label="Registros",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS,
                label="Configuración",
            ),
        ],
    )