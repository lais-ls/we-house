import flet as ft

import theme
from components.ui import app_field, card, labeled, logo, primary_button, show_message


def _option_card(icon, icon_bg, icon_color, title, subtitle, on_click) -> ft.Container:
    return ft.Container(
        on_click=on_click,
        ink=True,
        padding=18,
        border_radius=18,
        bgcolor=ft.Colors.with_opacity(0.7, theme.SURFACE),
        border=ft.Border.all(1, theme.BORDER),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            width=44,
                            height=44,
                            border_radius=12,
                            bgcolor=icon_bg,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(icon, color=icon_color, size=22),
                        ),
                        ft.Icon(ft.Icons.ARROW_FORWARD, size=18, color=theme.MUTED),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=4),
                ft.Text(title, size=16, weight=ft.FontWeight.W_700, color=theme.TEXT),
                ft.Text(subtitle, size=12, color=theme.MUTED),
            ],
            spacing=6,
        ),
    )


def options_view(page: ft.Page, nome: str = "Bia") -> ft.View:
    # TODO: Fetch logged-in user's name from database

    async def criar(e):
        await page.push_route("/criar-casa")

    async def entrar(e):
        await page.push_route("/entrar-casa")

    async def sair(e):
        await page.push_route("/")

    conteudo = ft.Column(
        [
            ft.Container(height=24),
            ft.Row([logo(32), ft.Text("WeHouse", size=18, weight=ft.FontWeight.W_700, color=theme.TEXT)], spacing=8),
            ft.Container(height=20),
            ft.Text(f"Olá, {nome}! 👋", size=26, weight=ft.FontWeight.W_700, color=theme.TEXT),
            ft.Text("Como você quer começar?", size=13, color=theme.MUTED),
            ft.Container(height=14),
            _option_card(
                ft.Icons.HOME_WORK_OUTLINED,
                theme.ICON_BG,
                theme.TEXT,
                "Criar uma nova casa",
                "Monte o espaço da sua casa e convide seus colegas",
                criar,
            ),
            _option_card(
                ft.Icons.VPN_KEY_OUTLINED,
                theme.SAGE,
                theme.SAGE_DARK,
                "Entrar em uma casa",
                "Já recebeu um código de convite? Entre agora",
                entrar,
            ),
        ],
        spacing=14,
        expand=True,
    )

    rodape = ft.Row(
        [ft.TextButton(content=ft.Text("Sair", size=15, weight=ft.FontWeight.W_600, color="#C9C5BA"), on_click=sair)],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    return ft.View(
        route="/opcoes",
        bgcolor=theme.BG,
        padding=ft.Padding.symmetric(horizontal=18),
        controls=[ft.SafeArea(ft.Column([conteudo, rodape], expand=True), expand=True)],
    )
