import flet as ft

import theme
from components.ui import app_field, back_header, card, labeled, primary_button, show_message


def create_house_view(page: ft.Page) -> ft.View:
    nome = app_field("Ex.: República Bela Vista")
    endereco = app_field("Ex.: Bela Vista, São Paulo")
    pix = app_field("Digite sua chave Pix")

    estado = {"cor": 0}  # índice da cor escolhida
    nome_cor = ft.Text(theme.HOUSE_COLORS[0][0], size=12, color=theme.MUTED)
    linha_cores = ft.Row(spacing=8, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def escolher_cor(i: int):
        def handler(e):
            estado["cor"] = i
            nome_cor.value = theme.HOUSE_COLORS[i][0]
            montar_cores()
            page.update()
        return handler

    def montar_cores():
        linha_cores.controls = [
            ft.Container(
                width=40,
                height=40,
                border_radius=20,
                border=ft.Border.all(2, hex_ if i == estado["cor"] else ft.Colors.TRANSPARENT),
                alignment=ft.Alignment.CENTER,
                on_click=escolher_cor(i),
                content=ft.Container(
                    width=30,
                    height=30,
                    border_radius=15,
                    bgcolor=hex_,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.CHECK, size=16, color=ft.Colors.WHITE)
                    if i == estado["cor"]
                    else None,
                ),
            )
            for i, (_, hex_) in enumerate(theme.HOUSE_COLORS)
        ]

    montar_cores()

    async def voltar(e):
        await page.push_route("/opcoes")

    async def criar(e):
        nome.error_text = None if (nome.value or "").strip() else "Dê um nome para a casa"
        page.update()
        if nome.error_text:
            return
        # TODO: salvar no banco: nome, endereco, pix e cor
        await page.push_route("/inicio")

    formulario = card(
        ft.Column(
            [
                labeled("Nome da casa", nome),
                labeled("Endereço ou bairro (opcional)", endereco),
                labeled("Sua chave Pix (opcional)", pix, helper="Usada para receber pagamentos dos moradores"),
            ],
            spacing=14,
        ),
        padding=16,
        radius=18,
    )

    conteudo = ft.Column(
        [
            ft.Container(
                content=ft.Icon(ft.Icons.HOME_OUTLINED, size=64, color="#D8D2C4"),
                alignment=ft.Alignment.CENTER,
                padding=ft.Padding.symmetric(vertical=8),
            ),
            formulario,
            ft.Container(height=4),
            ft.Row(
                [ft.Text("Cor da casa", size=12, weight=ft.FontWeight.W_600, color=theme.TEXT), nome_cor],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            linha_cores,
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.View(
        route="/criar-casa",
        bgcolor=theme.BG,
        padding=ft.Padding.symmetric(horizontal=18),
        controls=[
            ft.SafeArea(
                ft.Column(
                    [back_header("Criar nova casa", voltar), conteudo, primary_button("Criar casa", criar), ft.Container(height=8)],
                    expand=True,
                ),
                expand=True,
            )
        ],
    )
