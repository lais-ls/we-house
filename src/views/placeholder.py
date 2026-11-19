import flet as ft

import theme
from components.ui import bottom_nav, NAV_ITEMS


def placeholder_view(page: ft.Page, rota: str, titulo: str) -> ft.View:
    """Tela provisória para abas que ainda não foram feitas (Tarefas, Mais)."""
    indice = next((i for i, item in enumerate(NAV_ITEMS) if item[3] == rota), 0)
    return ft.View(
        route=rota,
        bgcolor=theme.BG,
        padding=ft.Padding.symmetric(horizontal=18),
        controls=[
            ft.SafeArea(
                ft.Column(
                    [
                        ft.Text(titulo, size=24, weight=ft.FontWeight.W_700, color=theme.TEXT),
                        ft.Text("Tela em construção", size=12, color=theme.MUTED),
                    ]
                ),
                expand=True,
            )
        ],
        navigation_bar=bottom_nav(page, indice),
    )
