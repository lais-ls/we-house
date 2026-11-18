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


# ---------------------------------------------------------------------------
# Barra inferior (para as telas internas do app, depois do login).
# Ajuste os rótulos/ícones/rotas conforme o seu Figma.
# ---------------------------------------------------------------------------
NAV_ITEMS = [
    ("Início", ft.Icons.HOME_OUTLINED, ft.Icons.HOME, "/inicio"),
    ("Tarefas", ft.Icons.CHECK_CIRCLE_OUTLINE, ft.Icons.CHECK_CIRCLE, "/tarefas"),
    ("Despesas", ft.Icons.RECEIPT_LONG_OUTLINED, ft.Icons.RECEIPT_LONG, "/despesas"),
    ("Perfil", ft.Icons.PERSON_OUTLINE, ft.Icons.PERSON, "/perfil"),
]


def bottom_nav(page: ft.Page, selected: int = 0) -> ft.NavigationBar:
    async def on_change(e):
        await page.push_route(NAV_ITEMS[int(e.data)][3])

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
