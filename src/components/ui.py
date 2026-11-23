"""Reusable components shared across screens."""

import flet as ft

import theme


def show_message(page: ft.Page, text: str):
    page.show_dialog(ft.SnackBar(ft.Text(text)))


def logo(size: int = 44) -> ft.Container:
    """Small gradient square with a house icon."""
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
    """Full-width slate-blue button."""
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
    """Text field styled to match the app."""
    return ft.TextField(
        hint_text=hint,
        prefix_icon=icon,
        password=password,
        can_reveal_password=password,
        filled=True,
        fill_color=theme.FIELD_BG,
        color=theme.TEXT,
        cursor_color=theme.PRIMARY,
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
    """Label above the field (plus optional helper text below)."""
    controls = [
        ft.Text(label, size=12, weight=ft.FontWeight.W_600, color=theme.TEXT),
        field,
    ]
    if helper:
        controls.append(ft.Text(helper, size=10, color=theme.MUTED))
    return ft.Column(controls, spacing=6)


def back_header(title: str, on_back) -> ft.Row:
    """Back arrow + screen title."""
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
    """Small button (e.g. 'Pagar')."""
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


def abrir_convite(page: ft.Page, nome_casa: str, codigo: str):
    """Dialog with the house invite code + a button to copy a ready-made message."""
    clipboard = ft.Clipboard()

    async def copiar(e):
        await clipboard.set(f"Entre na {nome_casa} no WeHouse! Use o código de convite: {codigo}")
        show_message(page, "Convite copiado! Cole no WhatsApp 😊")

    def fechar(e):
        page.pop_dialog()

    caixas = ft.Row(
        [
            ft.Container(
                width=52, height=60, border_radius=12, bgcolor=theme.FIELD_BG,
                border=ft.Border.all(1, theme.BORDER), alignment=ft.Alignment.CENTER,
                content=ft.Text(c, size=24, weight=ft.FontWeight.W_700, color=theme.TEXT),
            )
            for c in codigo
        ],
        alignment=ft.MainAxisAlignment.CENTER, spacing=10,
    )
    page.show_dialog(
        ft.AlertDialog(
            bgcolor=theme.SURFACE,
            title=ft.Text("Convidar para a casa", size=16, weight=ft.FontWeight.W_700, color=theme.TEXT),
            content=ft.Column(
                [
                    ft.Text(
                        f"Passe este código para seus colegas. Eles escolhem “Entrar em uma casa” no WeHouse "
                        f"e entram na {nome_casa}.",
                        size=12, color=theme.MUTED,
                    ),
                    ft.Container(height=4),
                    caixas,
                    ft.Container(height=4),
                    ft.Button(
                        content=ft.Row(
                            [ft.Icon(ft.Icons.CONTENT_COPY, size=16, color=ft.Colors.WHITE),
                             ft.Text("Copiar convite", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)],
                            alignment=ft.MainAxisAlignment.CENTER, spacing=8,
                        ),
                        bgcolor=theme.PRIMARY, height=44, on_click=copiar,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), elevation=0),
                    ),
                ],
                tight=True, spacing=8, width=320,
            ),
            actions=[ft.TextButton(content=ft.Text("Fechar", color=theme.MUTED), on_click=fechar)],
        )
    )


def screen_header(titulo: str, subtitulo: str, on_back) -> ft.Row:
    """Header for the newer screens: round back button + title + house name."""
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
    """Segmented control (e.g. Abertas | Encerradas). `on_select(key)` is called on tap."""
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
    """Rounded label (e.g. 'Proposta', 'Confirmado', 'Pendente')."""
    return ft.Container(
        content=ft.Text(texto, size=size, weight=ft.FontWeight.W_600, color=cor_texto),
        bgcolor=cor_fundo,
        padding=ft.Padding.symmetric(horizontal=8, vertical=2),
        border_radius=8,
    )


NAV_ITEMS = [
    ("Início", ft.Icons.HOME_OUTLINED, ft.Icons.HOME, "/inicio"),
    ("Contas", ft.Icons.RECEIPT_LONG_OUTLINED, ft.Icons.RECEIPT_LONG, "/contas"),
    ("Tarefas", ft.Icons.TASK_ALT, ft.Icons.TASK_ALT, "/tarefas"),
    ("Mais", ft.Icons.MORE_HORIZ, ft.Icons.MORE_HORIZ, "/mais"),
]


MAIS_INDEX = 3


def abrir_menu_mais(page: ft.Page, nav: ft.NavigationBar, selected: int):
    """Floating menu above the "Mais" tab, with a dimmed background to focus on it."""
    overlay_ref: list[ft.Control] = []

    def fechar():
        if overlay_ref and overlay_ref[0] in page.overlay:
            page.overlay.remove(overlay_ref[0])
        page.data.pop("fechar_menu_mais", None)
        nav.selected_index = selected
        page.update()

    def fechar_click(e):
        fechar()

    def ir(rota: str):
        async def handler(e):
            fechar()
            page.data["origem"] = page.route
            await page.push_route(rota)
        return handler

    def item(icone, texto, on_click) -> ft.Container:
        return ft.Container(
            on_click=on_click,
            ink=True,
            padding=ft.Padding.symmetric(horizontal=16, vertical=10),
            border_radius=22,
            bgcolor=theme.SURFACE,
            shadow=ft.BoxShadow(
                blur_radius=16, color=ft.Colors.with_opacity(0.18, ft.Colors.BLACK), offset=ft.Offset(0, 4)
            ),
            content=ft.Row(
                [ft.Icon(icone, size=18, color=theme.TEXT),
                 ft.Text(texto, size=13, weight=ft.FontWeight.W_600, color=theme.TEXT)],
                spacing=8, tight=True,
            ),
        )

    menu = ft.Column(
        [
            item(ft.Icons.SHOPPING_BAG_OUTLINED, "Lista de Compras", ir("/compras")),
            item(ft.Icons.EVENT_AVAILABLE_OUTLINED, "Reservar", ir("/reservas")),
            item(ft.Icons.HOW_TO_VOTE_OUTLINED, "Votações", ir("/votacao")),
            item(ft.Icons.GROUPS_OUTLINED, "Reuniões", ir("/reuniao")),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.END,
        tight=True,
        right=14,
        bottom=96,
    )
    overlay = ft.Stack(
        [
            ft.Container(expand=True, bgcolor=ft.Colors.with_opacity(0.55, ft.Colors.BLACK), on_click=fechar_click),
            menu,
        ],
        expand=True,
    )
    overlay_ref.append(overlay)
    page.overlay.append(overlay)
    page.data["fechar_menu_mais"] = fechar
    page.update()


def bottom_nav(page: ft.Page, selected: int = 0) -> ft.NavigationBar:
    async def on_change(e):
        indice = e.control.selected_index
        if indice == MAIS_INDEX:
            fechar_menu = page.data.get("fechar_menu_mais")
            if fechar_menu:
                fechar_menu()
            else:
                abrir_menu_mais(page, e.control, selected)
            return
        await page.push_route(NAV_ITEMS[indice][3])

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