"""Floating notifications panel (opened from the bell on the home screen)."""

import flet as ft

import theme
from services import dados_fake as db

_ESTILO = {
    "conta": (ft.Icons.PAYMENTS_OUTLINED, theme.WARN_TEXT, theme.WARN_BG),
    "receber": (ft.Icons.SAVINGS_OUTLINED, theme.OK_TEXT, theme.OK_BG),
    "voto": (ft.Icons.HOW_TO_VOTE_OUTLINED, theme.PRIMARY, theme.INFO_BG),
    "tarefa": (ft.Icons.TASK_ALT, theme.PRIMARY, theme.INFO_BG),
    "reuniao": (ft.Icons.GROUPS_OUTLINED, theme.PRIMARY, theme.INFO_BG),
}


def abrir_notificacoes(page: ft.Page, ao_mudar=None):
    """Opens the panel over a dimmed background. `ao_mudar()` runs whenever it closes
    (so the home screen can refresh the bell badge)."""
    ref: list[ft.Control] = []
    corpo = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO)
    cabecalho_acao = ft.TextButton(content=ft.Text("Marcar como lidas", size=11, color=theme.PRIMARY))

    def fechar():
        if ref and ref[0] in page.overlay:
            page.overlay.remove(ref[0])
        page.data.pop("fechar_notificacoes", None)
        if ao_mudar:
            ao_mudar()
        page.update()

    def fechar_click(e):
        fechar()

    def abrir_item(n):
        async def handler(e):
            db.marcar_lida(n.chave)
            fechar()
            page.data["origem"] = "/inicio"
            await page.push_route(n.rota)
        return handler

    def marcar_todas(e):
        db.marcar_todas_lidas()
        montar()

    def linha(n) -> ft.Container:
        icone, cor, fundo = _ESTILO[n.tipo]
        return ft.Container(
            on_click=abrir_item(n),
            ink=True,
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            bgcolor=None if n.lida else "#FBF8F1",
            content=ft.Row(
                [
                    ft.Container(
                        width=34, height=34, border_radius=17, bgcolor=fundo, alignment=ft.Alignment.CENTER,
                        content=ft.Icon(icone, size=17, color=cor),
                    ),
                    ft.Column(
                        [
                            ft.Text(n.titulo, size=12, color=theme.TEXT,
                                    weight=ft.FontWeight.W_500 if n.lida else ft.FontWeight.W_700),
                            ft.Text(n.detalhe, size=10, color=theme.MUTED),
                        ],
                        spacing=1, expand=True,
                    ),
                    ft.Container(width=8, height=8, border_radius=4,
                                 bgcolor=ft.Colors.TRANSPARENT if n.lida else theme.ACCENT),
                ],
                spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def montar(update: bool = True):
        itens = db.notificacoes()
        corpo.controls = [linha(n) for n in itens] or [
            ft.Container(padding=30, alignment=ft.Alignment.CENTER,
                         content=ft.Text("Tudo em dia 🎉", size=13, color=theme.MUTED))
        ]
        corpo.height = min(max(len(itens), 1) * 62, 340)
        cabecalho_acao.visible = any(not n.lida for n in itens)
        if update:
            page.update()

    cabecalho_acao.on_click = marcar_todas
    montar(update=False)

    painel = ft.Container(
        width=330,
        right=14,
        top=64,
        bgcolor=theme.SURFACE,
        border_radius=20,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        shadow=ft.BoxShadow(blur_radius=24, color=ft.Colors.with_opacity(0.22, ft.Colors.BLACK), offset=ft.Offset(0, 8)),
        content=ft.Column(
            [
                ft.Container(
                    padding=ft.Padding.only(left=14, right=6, top=6, bottom=0),
                    content=ft.Row(
                        [ft.Text("Notificações", size=14, weight=ft.FontWeight.W_700, color=theme.TEXT),
                         cabecalho_acao],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ),
                ft.Divider(height=1, color=theme.BORDER),
                corpo,
            ],
            spacing=0, tight=True,
        ),
    )
    overlay = ft.Stack(
        [ft.Container(expand=True, bgcolor=ft.Colors.with_opacity(0.55, ft.Colors.BLACK), on_click=fechar_click), painel],
        expand=True,
    )
    ref.append(overlay)
    page.overlay.append(overlay)
    page.data["fechar_notificacoes"] = fechar
    page.update()
