import flet as ft

import theme
from components.ui import app_field, card, labeled, logo, primary_button, show_message


def login_view(page: ft.Page) -> ft.View:
    email = app_field("voce@universidade.edu.br", icon=ft.Icons.MAIL_OUTLINE,
                      keyboard_type=ft.KeyboardType.EMAIL)
    senha = app_field("Digite sua senha", icon=ft.Icons.LOCK_OUTLINE, password=True)

    async def entrar(e):
        # TODO: Replace with real database authentication
        email.error_text = None if "@" in (email.value or "") else "Informe um e-mail válido"
        senha.error_text = None if senha.value else "Informe sua senha"
        page.update()
        if email.error_text or senha.error_text:
            return
        await page.push_route("/opcoes")

    def esqueceu(e):
        show_message(page, "Recuperação de senha: em breve")

    def criar_conta(e):
        show_message(page, "Criar conta: em breve")

    formulario = card(
        ft.Column(
            [
                ft.Text("Bom ter você aqui!", size=18, weight=ft.FontWeight.W_700, color=theme.TEXT),
                ft.Text("Entre com sua conta para continuar.", size=12, color=theme.MUTED),
                ft.Container(height=4),
                labeled("E-mail", email),
                labeled("Senha", senha),
                ft.Row(
                    [ft.TextButton(
                        content=ft.Text("Esqueceu a senha?", size=11, color=theme.PRIMARY),
                        on_click=esqueceu,
                    )],
                    alignment=ft.MainAxisAlignment.END,
                ),
                primary_button("Entrar", entrar),
            ],
            spacing=10,
        ),
        padding=22,
        radius=24,
    )

    conteudo = ft.Column(
        [
            ft.Container(height=60),
            ft.Row(
                [logo(40), ft.Text("WeHouse", size=26, weight=ft.FontWeight.W_700, color=theme.TEXT)],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            ft.Container(height=6),
            ft.Text(
                "A casa organizada, a\nconvivência em paz",
                size=20,
                weight=ft.FontWeight.W_700,
                color=theme.TEXT,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=14),
            formulario,
            ft.Row(
                [
                    ft.Text("Ainda não tem conta?", size=12, color=theme.MUTED),
                    ft.TextButton(
                        content=ft.Text("Criar conta", size=12, weight=ft.FontWeight.W_700, color=theme.PRIMARY),
                        on_click=criar_conta,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=0,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        scroll=ft.ScrollMode.AUTO,
        spacing=6,
    )

    return ft.View(
        route="/",
        bgcolor=theme.BG,
        padding=ft.Padding.symmetric(horizontal=18),
        controls=[ft.SafeArea(conteudo, expand=True)],
    )
