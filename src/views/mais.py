import flet as ft

import theme
from components.ui import abrir_convite, bottom_nav, logo
from services import dados_fake as db


def _item(icone, titulo, subtitulo, on_click) -> ft.Container:
    return ft.Container(
        on_click=on_click,
        ink=True,
        padding=14,
        border_radius=16,
        bgcolor=theme.SURFACE,
        border=ft.Border.all(1, theme.BORDER),
        content=ft.Row(
            [
                ft.Container(
                    width=40, height=40, border_radius=12, bgcolor=theme.ICON_BG,
                    alignment=ft.Alignment.CENTER, content=ft.Icon(icone, size=20, color=theme.TEXT),
                ),
                ft.Column(
                    [ft.Text(titulo, size=14, weight=ft.FontWeight.W_700, color=theme.TEXT),
                     ft.Text(subtitulo, size=11, color=theme.MUTED)],
                    spacing=0, expand=True,
                ),
                ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=theme.MUTED),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=12,
        ),
    )


def mais_view(page: ft.Page) -> ft.View:
    def ir(rota):
        async def handler(e):
            page.data["origem"] = "/mais"
            await page.push_route(rota)
        return handler

    def convidar(e):
        abrir_convite(page, db.CASA.nome, db.CASA.codigo)

    async def sair(e):
        await page.push_route("/")

    n_votos = sum(1 for v in db.votacoes(True) if db.EU.id not in v.votos)
    conteudo = ft.Column(
        [
            ft.Container(height=8),
            ft.Row([logo(28), ft.Text("Mais", size=24, weight=ft.FontWeight.W_700, color=theme.TEXT)], spacing=10),
            ft.Text(db.CASA.nome, size=11, color=theme.MUTED),
            ft.Container(height=6),
            _item(ft.Icons.HOW_TO_VOTE_OUTLINED, "Votação",
                  f"{n_votos} aguardando seu voto" if n_votos else "Decisões da casa", ir("/votacao")),
            _item(ft.Icons.EVENT_AVAILABLE_OUTLINED, "Reservar", "Máquina de lavar, sala e churrasqueira", ir("/reservas")),
            _item(ft.Icons.GROUPS_OUTLINED, "Reunião mensal", "Pauta, ata e combinados", ir("/reuniao")),
            _item(ft.Icons.PERSON_ADD_ALT_1_OUTLINED, "Convidar moradores",
                  f"Código da casa: {db.CASA.codigo}", convidar),
            ft.Container(expand=True),
            ft.Row([ft.TextButton(content=ft.Text("Sair", size=15, weight=ft.FontWeight.W_600, color="#C9C5BA"),
                                  on_click=sair)],
                   alignment=ft.MainAxisAlignment.CENTER),
        ],
        spacing=10,
        expand=True,
    )
    return ft.View(
        route="/mais",
        bgcolor=theme.BG,
        padding=ft.Padding.symmetric(horizontal=18),
        controls=[ft.SafeArea(conteudo, expand=True)],
        navigation_bar=bottom_nav(page, 3),
    )
