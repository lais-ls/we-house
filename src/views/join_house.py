import flet as ft

import theme
from components.ui import back_header, primary_button, show_message

TAMANHO_CODIGO = 4


def join_house_view(page: ft.Page) -> ft.View:
    clipboard = ft.Clipboard()  # serviço para o botão "Colar código"

    def nova_caixa() -> ft.TextField:
        return ft.TextField(
            width=52,
            height=56,
            max_length=1,
            counter=ft.Text(""),  # esconde o contador "0/1"
            text_align=ft.TextAlign.CENTER,
            text_size=20,
            capitalization=ft.TextCapitalization.CHARACTERS,
            filled=True,
            fill_color=theme.SURFACE,
            border_radius=12,
            border_color=theme.BORDER,
            focused_border_color=theme.PRIMARY,
            content_padding=ft.Padding.all(0),
        )

    caixas = [nova_caixa() for _ in range(TAMANHO_CODIGO)]

    def ao_digitar(i: int):
        async def handler(e):
            e.control.value = (e.control.value or "").upper()
            page.update()
            if e.control.value and i < TAMANHO_CODIGO - 1:
                await caixas[i + 1].focus()
        return handler

    for i, c in enumerate(caixas):
        c.on_change = ao_digitar(i)

    def codigo() -> str:
        return "".join((c.value or "") for c in caixas)

    async def colar(e):
        texto = (await clipboard.get() or "").strip().upper()
        texto = "".join(ch for ch in texto if ch.isalnum())[:TAMANHO_CODIGO]
        for i, c in enumerate(caixas):
            c.value = texto[i] if i < len(texto) else ""
        page.update()

    async def voltar(e):
        await page.push_route("/opcoes")

    async def entrar(e):
        if len(codigo()) < TAMANHO_CODIGO:
            show_message(page, f"Digite os {TAMANHO_CODIGO} caracteres do código")
            return
        # TODO: validar o código no banco e entrar na casa
        await page.push_route("/inicio")

    conteudo = ft.Column(
        [
            ft.Text(
                "Digite o código de convite que seu colega compartilhou com você",
                size=12,
                color=theme.MUTED,
            ),
            ft.Container(height=24),
            ft.Container(
                width=56,
                height=56,
                border_radius=28,
                bgcolor=theme.ICON_BG,
                alignment=ft.Alignment.CENTER,
                content=ft.Icon(ft.Icons.VPN_KEY_OUTLINED, color=theme.MUTED, size=26),
            ),
            ft.Container(height=8),
            ft.Row(caixas, alignment=ft.MainAxisAlignment.CENTER, spacing=12),
            ft.TextButton(
                content=ft.Text("Colar código", size=12, weight=ft.FontWeight.W_600, color=theme.PRIMARY),
                icon=ft.Icons.CONTENT_PASTE,
                icon_color=theme.PRIMARY,
                on_click=colar,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    rodape = ft.Column(
        [
            primary_button("Entrar na casa", entrar),
            ft.Row(
                [
                    ft.Text("Não tem um código?", size=11, color=theme.MUTED),
                    ft.Text("Peça para quem criou a casa", size=11, weight=ft.FontWeight.W_600, color=theme.PRIMARY),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=4,
            ),
            ft.Container(height=4),
        ],
        spacing=10,
    )

    return ft.View(
        route="/entrar-casa",
        bgcolor=theme.BG,
        padding=ft.Padding.symmetric(horizontal=18),
        services=[clipboard],
        controls=[ft.SafeArea(ft.Column([back_header("Entrar em uma casa", voltar), conteudo, rodape], expand=True), expand=True)],
    )
