"""Componentes reutilizáveis entre as telas."""

import flet as ft

import theme


def show_message(page: ft.Page, text: str):
    page.show_dialog(ft.SnackBar(ft.Text(text)))


def logo(size: int = 44) -> ft.Container:
    """Quadradinho com gradiente + ícone de casa."""
    return ft.Container(
        width=size,
        height=size,
        border_radius=size * 0.28,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=["#F7C2B2", "#C8C2EE", "#B8D3C2"],
        ),
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(ft.Icons.HOME_ROUNDED, color=ft.Colors.WHITE, size=size * 0.55),
    )


def primary_button(text: str, on_click=None) -> ft.Row:
    """Botão azul acinzentado que ocupa a largura toda."""
    return ft.Row(
        [
            ft.Button(
                content=ft.Text(text, size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                bgcolor=theme.PRIMARY,
                height=48,
                expand=True,
                on_click=on_click,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    elevation=0,
                ),
            )
        ]
    )


def app_field(hint: str, icon=None, password: bool = False, **kwargs) -> ft.TextField:
    """Campo de texto no estilo do app."""
    return ft.TextField(
        hint_text=hint,
        prefix_icon=icon,
        password=password,
        can_reveal_password=password,
        filled=True,
        fill_color=theme.FIELD_BG,
        border_radius=10,
        border_color=theme.BORDER,
        focused_border_color=theme.PRIMARY,
        border_width=1,
        height=46,
        text_size=13,
        hint_style=ft.TextStyle(size=13, color=theme.MUTED),
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=0),
        **kwargs,
    )


def labeled(label: str, field: ft.Control, helper: str | None = None) -> ft.Column:
    """Rótulo em cima do campo (e um texto de ajuda opcional embaixo)."""
    controls = [
        ft.Text(label, size=12, weight=ft.FontWeight.W_600, color=theme.TEXT),
        field,
    ]
    if helper:
        controls.append(ft.Text(helper, size=10, color=theme.MUTED))
    return ft.Column(controls, spacing=6)


def back_header(title: str, on_back) -> ft.Row:
    """Seta de voltar + título da tela."""
    return ft.Row(
        [
            ft.IconButton(ft.Icons.ARROW_BACK, icon_size=20, icon_color=theme.TEXT, on_click=on_back),
            ft.Text(title, size=17, weight=ft.FontWeight.W_600, color=theme.TEXT),
        ],
        spacing=4,
    )


def card(content: ft.Control, padding: int = 20, radius: int = 20) -> ft.Container:
    return ft.Container(
        content=content,
        padding=padding,
        bgcolor=theme.SURFACE,
        border_radius=radius,
        shadow=ft.BoxShadow(
            blur_radius=18,
            color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
        ),
    )


def brl(valor: float) -> str:
    """85 -> 'R$ 85,00'  |  1234.5 -> 'R$ 1.234,50'"""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def avatar(inicial: str, cor: str, size: int = 28) -> ft.Container:
    return ft.Container(
        width=size,
        height=size,
        border_radius=size / 2,
        bgcolor=cor,
        alignment=ft.Alignment.CENTER,
        content=ft.Text(inicial, size=size * 0.42, weight=ft.FontWeight.W_700, color=theme.TEXT),
    )


def section_title(titulo: str, acao: str | None = None, on_click=None) -> ft.Row:
    itens = [ft.Text(titulo, size=14, weight=ft.FontWeight.W_700, color=theme.TEXT)]
    if acao:
        itens.append(
            ft.TextButton(content=ft.Text(acao, size=11, color=theme.PRIMARY), on_click=on_click)
        )
    return ft.Row(itens, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)


def small_button(text: str, on_click=None) -> ft.Button:
    """Botão pequeno (ex.: 'Pagar')."""
    return ft.Button(
        content=ft.Text(text, size=11, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
        bgcolor=theme.PRIMARY,
        height=30,
        on_click=on_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.Padding.symmetric(horizontal=14),
            elevation=0,
        ),
    )


def outline_button(text: str, icon=None, on_click=None) -> ft.Row:
    return ft.Row(
        [
            ft.OutlinedButton(
                content=ft.Text(text, size=13, weight=ft.FontWeight.W_600, color=theme.TEXT),
                icon=icon,
                icon_color=theme.TEXT,
                height=44,
                expand=True,
                on_click=on_click,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    side=ft.BorderSide(1, theme.BORDER),
                ),
            )
        ]
    )


def screen_header(titulo: str, subtitulo: str, on_back) -> ft.Row:
    """Cabeçalho das telas novas: botão redondo de voltar + título + nome da casa."""
    return ft.Row(
        [
            ft.IconButton(
                ft.Icons.CHEVRON_LEFT,
                icon_size=20,
                icon_color=theme.TEXT,
                bgcolor=theme.SURFACE,
                on_click=on_back,
                style=ft.ButtonStyle(shape=ft.CircleBorder(), side=ft.BorderSide(1, theme.BORDER)),
            ),
            ft.Column(
                [
                    ft.Text(titulo, size=18, weight=ft.FontWeight.W_700, color=theme.TEXT),
                    ft.Text(subtitulo, size=11, color=theme.MUTED),
                ],
                spacing=0,
            ),
        ],
        spacing=8,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def segmented(opcoes: list[tuple[str, str]], ativa: str, on_select) -> ft.Container:
    """Controle segmentado (ex.: Abertas | Encerradas). `on_select(chave)` é chamado ao tocar."""
    return ft.Container(
        bgcolor="#EDE9DF",
        padding=3,
        border_radius=12,
        content=ft.Row(
            [
                ft.Container(
                    expand=True,
                    height=36,
                    border_radius=10,
                    bgcolor=theme.SURFACE if chave == ativa else ft.Colors.TRANSPARENT,
                    alignment=ft.Alignment.CENTER,
                    on_click=lambda e, c=chave: on_select(c),
                    content=ft.Text(
                        texto, size=12, weight=ft.FontWeight.W_600,
                        color=theme.TEXT if chave == ativa else theme.MUTED,
                    ),
                )
                for chave, texto in opcoes
            ],
            spacing=0,
        ),
    )


def pill(texto: str, cor_texto: str, cor_fundo: str, size: int = 10) -> ft.Container:
    """Etiqueta arredondada (ex.: 'Proposta', 'Confirmado', 'Pendente')."""
    return ft.Container(
        content=ft.Text(texto, size=size, weight=ft.FontWeight.W_600, color=cor_texto),
        bgcolor=cor_fundo,
        padding=ft.Padding.symmetric(horizontal=8, vertical=2),
        border_radius=8,
    )


# ---------------------------------------------------------------------------
# Barra inferior (telas internas do app, depois de entrar numa casa).
# ---------------------------------------------------------------------------
NAV_ITEMS = [
    ("Início", ft.Icons.HOME_OUTLINED, ft.Icons.HOME, "/inicio"),
    ("Contas", ft.Icons.RECEIPT_LONG_OUTLINED, ft.Icons.RECEIPT_LONG, "/contas"),
    ("Tarefas", ft.Icons.TASK_ALT, ft.Icons.TASK_ALT, "/tarefas"),
    ("Mais", ft.Icons.MORE_HORIZ, ft.Icons.MORE_HORIZ, "/mais"),
]


def bottom_nav(page: ft.Page, selected: int = 0) -> ft.NavigationBar:
    async def on_change(e):
        await page.push_route(NAV_ITEMS[e.control.selected_index][3])

    return ft.NavigationBar(
        selected_index=selected,
        bgcolor=theme.SURFACE,
        indicator_color="#E4E8EF",
        on_change=on_change,
        destinations=[
            ft.NavigationBarDestination(icon=icon, selected_icon=sel, label=label)
            for label, icon, sel, _ in NAV_ITEMS
        ],
    )
