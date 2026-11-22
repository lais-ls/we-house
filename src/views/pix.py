import flet as ft

import theme
from components.ui import avatar, back_header, brl, card, outline_button, primary_button, show_message
from services import dados_fake as db
from services.pix import gerar_pix, qr_png

# TODO: a chave Pix de cada morador virá do banco (campo "Sua chave Pix" da tela Criar casa)
CHAVES_PIX = {
    "Lucas": "lucas@email.com",
    "Marina": "marina@email.com",
    "Ana": "ana@email.com",
    "Bia": "bia@email.com",
}


def pix_view(page: ft.Page) -> ft.View:
    clipboard = ft.Clipboard()
    divida = db.get_divida(page.data.get("divida_id", -1))

    async def voltar(e):
        await page.push_route(page.data.get("anterior") or "/contas")

    if divida is None:  # abriu /pix sem escolher uma conta (ex.: recarregou a página)
        async def ir_contas(e):
            await page.push_route("/contas")

        return ft.View(
            route="/pix",
            bgcolor=theme.BG,
            padding=ft.Padding.symmetric(horizontal=18),
            controls=[
                ft.SafeArea(
                    ft.Column(
                        [
                            back_header("Pagar com Pix", voltar),
                            ft.Container(height=40),
                            ft.Text("Nenhuma conta selecionada.", color=theme.MUTED),
                            primary_button("Ir para Contas", ir_contas),
                        ]
                    )
                )
            ],
        )

    credor = db.morador_por_id(divida.credor_id)
    codigo = gerar_pix(
        chave=CHAVES_PIX.get(credor.nome, "chave@pix.com"),
        nome=credor.nome,
        cidade="Sao Paulo",
        valor=divida.valor,
    )

    async def copiar(e):
        await clipboard.set(codigo)
        show_message(page, "Código Pix copiado!")

    async def ja_paguei(e):
        db.informar_pagamento(divida.id)
        show_message(page, f"Aviso enviado! {credor.nome} vai confirmar o recebimento")
        await page.push_route("/contas")

    qr = card(
        ft.Column(
            [
                ft.Text("Escaneie com o app do seu banco", size=11, color=theme.MUTED),
                ft.Container(
                    padding=8,
                    border_radius=12,
                    border=ft.Border.all(1, theme.BORDER),
                    content=ft.Image(src=qr_png(codigo), width=200, height=200, fit=ft.BoxFit.CONTAIN),
                ),
                ft.Row(
                    [
                        avatar(credor.inicial, credor.cor, 24),
                        ft.Text(credor.nome, size=12, weight=ft.FontWeight.W_600, color=theme.TEXT),
                        ft.Text(brl(divida.valor), size=12, weight=ft.FontWeight.W_700, color=theme.ACCENT),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        ),
        padding=18,
        radius=20,
    )

    copia_e_cola = ft.Column(
        [
            ft.Text("Pix copia e cola", size=12, weight=ft.FontWeight.W_600, color=theme.TEXT),
            ft.Container(
                padding=12,
                border_radius=10,
                bgcolor="#ECE9E1",
                content=ft.Text(codigo, size=10, color=theme.MUTED, selectable=True, max_lines=3,
                                overflow=ft.TextOverflow.ELLIPSIS),
            ),
            outline_button("Copiar código", ft.Icons.CONTENT_COPY, copiar),
        ],
        spacing=8,
    )

    cabecalho = ft.Row(
        [
            ft.IconButton(ft.Icons.ARROW_BACK, icon_size=20, icon_color=theme.TEXT, on_click=voltar),
            ft.Column(
                [
                    ft.Text(f"Pagar {brl(divida.valor)} para {credor.nome}", size=15,
                            weight=ft.FontWeight.W_600, color=theme.TEXT),
                    ft.Text(divida.descricao, size=11, color=theme.MUTED),
                ],
                spacing=0,
                expand=True,
            ),
        ],
        spacing=4,
    )

    rodape = ft.Column(
        [
            primary_button("Já paguei", ja_paguei),
            ft.Text(f"Depois de pagar, toque para avisar {credor.nome}", size=10, color=theme.MUTED,
                    text_align=ft.TextAlign.CENTER),
            ft.Container(height=4),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
    )

    return ft.View(
        route="/pix",
        bgcolor=theme.BG,
        padding=ft.Padding.symmetric(horizontal=18),
        services=[clipboard],
        controls=[
            ft.SafeArea(
                ft.Column(
                    [
                        cabecalho,
                        ft.Column([qr, copia_e_cola], spacing=14, scroll=ft.ScrollMode.AUTO, expand=True),
                        rodape,
                    ],
                    expand=True,
                ),
                expand=True,
            )
        ],
    )
