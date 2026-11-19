import flet as ft

import theme
from components.ui import avatar, bottom_nav, brl, card, small_button, show_message
from services import dados_fake as db


def bills_view(page: ft.Page) -> ft.View:
    estado = {"aba": "devo"}  # "devo" | "devem"
    lista = ft.Column(spacing=10)
    resumo = ft.Container()
    abas = ft.Row(spacing=0)

    async def ir_nova_conta(e):
        await page.push_route("/nova-conta")

    def pagar(divida_id: int):
        async def handler(e):
            page.data["divida_id"] = divida_id
            await page.push_route("/pix")
        return handler

    def receber(divida_id: int):
        def handler(e):
            db.marcar_paga(divida_id)  # TODO: confirmar recebimento no banco
            show_message(page, "Marcado como recebido")
            atualizar()
        return handler

    def trocar_aba(aba: str):
        def handler(e):
            estado["aba"] = aba
            atualizar()
        return handler

    def aba(texto: str, chave: str) -> ft.Container:
        ativa = estado["aba"] == chave
        return ft.Container(
            expand=True,
            height=38,
            border_radius=10,
            bgcolor=theme.SURFACE if ativa else ft.Colors.TRANSPARENT,
            alignment=ft.Alignment.CENTER,
            on_click=trocar_aba(chave),
            border=ft.Border.all(1, theme.ACCENT) if ativa else None,
            content=ft.Text(
                texto, size=12, weight=ft.FontWeight.W_600,
                color=theme.ACCENT if ativa else theme.MUTED,
            ),
        )

    def linha(d) -> ft.Container:
        eu_devo = estado["aba"] == "devo"
        outro = db.morador_por_id(d.credor_id if eu_devo else d.devedor_id)
        return card(
            ft.Row(
                [
                    avatar(outro.inicial, outro.cor, 34),
                    ft.Column(
                        [
                            ft.Text(outro.nome, size=13, weight=ft.FontWeight.W_700, color=theme.TEXT),
                            ft.Text(d.descricao, size=11, color=theme.MUTED),
                            ft.Container(
                                content=ft.Text(d.vencimento or "Pendente", size=9, color="#B5651D"),
                                bgcolor="#FCEBD3",
                                padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                                border_radius=8,
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Column(
                        [
                            ft.Text(brl(d.valor), size=13, weight=ft.FontWeight.W_700, color=theme.TEXT),
                            small_button("Pagar", pagar(d.id)) if eu_devo else small_button("Recebido", receber(d.id)),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        spacing=6,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=12,
            radius=16,
        )

    def atualizar(redesenhar: bool = True):
        eu_devo = estado["aba"] == "devo"
        todas = db.dividas_que_eu_devo() if eu_devo else db.dividas_que_me_devem()
        pendentes = [d for d in todas if not d.pago]
        total = db.total_pendente(todas)
        n = len(pendentes)

        abas.controls = [aba("Eu devo", "devo"), aba("Me devem", "devem")]

        resumo.content = ft.Container(
            padding=16,
            border_radius=16,
            bgcolor="#FFF1EA" if eu_devo else "#EAF4EE",
            border=ft.Border.all(1, "#FBD9C9" if eu_devo else "#CFE3D7"),
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Total que devo" if eu_devo else "Total a receber", size=11, color=theme.MUTED),
                            ft.Text(brl(total), size=24, weight=ft.FontWeight.W_700,
                                    color=theme.ACCENT if eu_devo else theme.SAGE_DARK),
                        ],
                        spacing=0,
                    ),
                    ft.Text(f"{n} conta{'s' if n != 1 else ''} pendente{'s' if n != 1 else ''}",
                            size=11, color=theme.MUTED),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.END,
            ),
        )

        lista.controls = [linha(d) for d in pendentes] or [
            ft.Container(
                padding=30,
                alignment=ft.Alignment.CENTER,
                content=ft.Text("Nenhuma conta pendente 🎉", size=13, color=theme.MUTED),
            )
        ]
        if redesenhar:
            page.update()

    topo = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Contas", size=24, weight=ft.FontWeight.W_700, color=theme.TEXT),
                    ft.Text(db.CASA.nome, size=11, color=theme.MUTED),
                ],
                spacing=0,
            ),
            ft.IconButton(
                ft.Icons.ADD,
                icon_color=ft.Colors.WHITE,
                bgcolor=theme.PRIMARY,
                on_click=ir_nova_conta,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    conteudo = ft.Column(
        [
            topo,
            ft.Container(content=abas, bgcolor="#EDE9DF", padding=3, border_radius=12),
            resumo,
            ft.Text("Suas contas", size=14, weight=ft.FontWeight.W_700, color=theme.TEXT),
            lista,
            ft.Container(height=8),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    view = ft.View(
        route="/contas",
        bgcolor=theme.BG,
        padding=ft.Padding.symmetric(horizontal=18),
        controls=[ft.SafeArea(conteudo, expand=True)],
        navigation_bar=bottom_nav(page, 1),
    )
    atualizar(redesenhar=False)  # monta o conteúdo inicial
    return view
