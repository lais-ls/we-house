import re

import flet as ft

import theme
from components.ui import avatar, card, screen_header, show_message
from services import dados_fake as db

_PADRAO_QTD = re.compile(r"^(.*?)\s+(\d+(?:[.,]\d+)?\s?(?:kg|g|un|l|ml|pct|cx))$", re.IGNORECASE)


def _separar_quantidade(texto: str) -> tuple[str, str]:
    m = _PADRAO_QTD.match(texto.strip())
    return (m.group(1).strip(), m.group(2).replace(" ", "")) if m else (texto.strip(), "")


def compras_view(page: ft.Page) -> ft.View:
    estado = {"comprados_abertos": False}
    lista = ft.Column(spacing=0)
    comprados = ft.Column(spacing=10)
    contador = ft.Text("", size=11, color=theme.MUTED)

    campo = ft.TextField(
        hint_text="Adicionar item (ex.: Arroz 2kg)",
        border=ft.InputBorder.NONE,
        text_size=13,
        hint_style=ft.TextStyle(size=13, color=theme.MUTED),
        content_padding=ft.Padding.symmetric(horizontal=4, vertical=0),
        expand=True,
    )

    async def voltar(e):
        await page.push_route(page.data.get("origem") or "/inicio")

    def alternar(item_id: int):
        def handler(e):
            db.alternar_item(item_id, bool(e.control.value))
            montar()
        return handler

    def adicionar(e):
        nome, qtd = _separar_quantidade(campo.value or "")
        if not nome:
            show_message(page, "Digite o nome do item")
            return
        db.adicionar_item(nome, qtd, db.EU.id)
        campo.value = ""
        montar()

    campo.on_submit = adicionar

    def quem(item) -> str:
        return "você" if item.adicionado_por_id == db.EU.id else db.morador_por_id(item.adicionado_por_id).nome

    def linha(item, ultima: bool) -> ft.Container:
        quem_add = db.morador_por_id(item.adicionado_por_id)
        riscado = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH) if item.comprado else None
        nome = [ft.Text(item.nome, size=14, weight=ft.FontWeight.W_700,
                        color=theme.MUTED if item.comprado else theme.TEXT, style=riscado)]
        if item.quantidade:
            nome.append(
                ft.Container(
                    content=ft.Text(item.quantidade, size=10, weight=ft.FontWeight.W_600, color=theme.TEXT),
                    bgcolor="#E9E5D3", padding=ft.Padding.symmetric(horizontal=7, vertical=1), border_radius=7,
                )
            )
        return ft.Container(
            padding=ft.Padding.symmetric(vertical=10),
            border=None if ultima else ft.Border(bottom=ft.BorderSide(1, theme.BORDER)),
            content=ft.Row(
                [
                    ft.Checkbox(value=item.comprado, active_color=theme.PRIMARY, on_change=alternar(item.id)),
                    ft.Column(
                        [ft.Row(nome, spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                         ft.Text(f"Adicionado por {quem(item)}", size=11, color=theme.MUTED)],
                        spacing=2, expand=True,
                    ),
                    avatar(quem_add.inicial, quem_add.cor, 30),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=4,
            ),
        )

    def alternar_comprados(e):
        estado["comprados_abertos"] = not estado["comprados_abertos"]
        montar()

    def montar(update: bool = True):
        pendentes = db.itens_compra(False)
        feitos = db.itens_compra(True)
        n = len(pendentes)
        contador.value = f"{n} {'item' if n == 1 else 'itens'}"
        lista.controls = [linha(i, k == n - 1) for k, i in enumerate(pendentes)] or [
            ft.Container(padding=20, alignment=ft.Alignment.CENTER,
                         content=ft.Text("Lista vazia 🎉", size=13, color=theme.MUTED))
        ]
        aberto = estado["comprados_abertos"]
        nf = len(feitos)
        comprados.controls = [
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=14, vertical=12),
                border_radius=14, bgcolor=theme.BUSY_BG, on_click=alternar_comprados, ink=True,
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=18, color=theme.TEXT),
                        ft.Text("Comprados", size=13, weight=ft.FontWeight.W_700, color=theme.TEXT, expand=True),
                        ft.Text(f"{nf} {'item' if nf == 1 else 'itens'}", size=11, color=theme.TEXT),
                        ft.Icon(ft.Icons.KEYBOARD_ARROW_UP if aberto else ft.Icons.KEYBOARD_ARROW_DOWN,
                                size=20, color=theme.TEXT),
                    ],
                    spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        ]
        if aberto and feitos:
            comprados.controls.append(
                card(ft.Column([linha(i, k == nf - 1) for k, i in enumerate(feitos)], spacing=0),
                     padding=ft.Padding.symmetric(horizontal=12, vertical=2), radius=18)
            )
        if update:
            page.update()

    adicionar_barra = ft.Container(
        padding=ft.Padding.only(left=12, right=8, top=8, bottom=8),
        border_radius=14, bgcolor=theme.SURFACE, border=ft.Border.all(1, theme.BORDER),
        content=ft.Row(
            [
                campo,
                ft.Container(
                    width=40, height=40, border_radius=12, bgcolor=theme.PRIMARY, ink=True,
                    alignment=ft.Alignment.CENTER, on_click=adicionar,
                    content=ft.Icon(ft.Icons.ADD, size=22, color=ft.Colors.WHITE),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    conteudo = ft.Column(
        [
            adicionar_barra,
            ft.Row([ft.Text("Para comprar", size=13, weight=ft.FontWeight.W_700, color=theme.TEXT), contador],
                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            card(lista, padding=ft.Padding.symmetric(horizontal=12, vertical=2), radius=18),
            comprados,
            ft.Text("Marque o item ao comprar. A lista é compartilhada e todos os moradores veem na hora.",
                    size=11, color=theme.MUTED, text_align=ft.TextAlign.CENTER),
            ft.Container(height=8),
        ],
        spacing=14, scroll=ft.ScrollMode.AUTO, expand=True,
    )

    montar(update=False)
    return ft.View(
        route="/compras",
        bgcolor=theme.BG,
        padding=ft.Padding.symmetric(horizontal=18),
        controls=[
            ft.SafeArea(
                ft.Column([screen_header("Lista de compras", f"{db.CASA.nome} · compartilhada", voltar), conteudo],
                          expand=True, spacing=12),
                expand=True,
            )
        ],
    )
