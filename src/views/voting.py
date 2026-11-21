import flet as ft

import theme
from components.ui import (
    app_field, avatar, brl, card, labeled, pill, screen_header, segmented, show_message,
)
from services import dados_fake as db
from views.new_bill import _para_float


def _cartao_votacao(v, on_vote) -> ft.Container:
    eu = db.EU
    total = len(db.CASA.moradores)
    n_votos = len(v.votos)
    pct = n_votos / total
    aberta = v.status == "aberta"
    ja_votei = eu.id in v.votos

    # avatares: quem já votou colorido, quem falta tracejado
    avatares = [
        avatar(m.inicial, m.cor, 28) for m in db.CASA.moradores if m.id in v.votos and m.id != eu.id
    ]
    if not ja_votei:
        avatares.append(
            ft.Container(
                width=28, height=28, border_radius=14,
                border=ft.Border.all(1, theme.MUTED),
                alignment=ft.Alignment.CENTER,
                content=ft.Text("?", size=11, color=theme.MUTED),
            )
        )
    else:
        avatares.append(avatar(eu.inicial, eu.cor, 28))

    votaram = [m.nome for m in db.CASA.moradores if m.id in v.votos and m.id != eu.id]
    if len(votaram) > 1:
        quem = ", ".join(votaram[:-1]) + " e " + votaram[-1] + " já votaram"
    elif votaram:
        quem = f"{votaram[0]} já votou"
    else:
        quem = "Ninguém votou ainda"
    faltam = [m.nome for m in db.CASA.moradores if m.id not in v.votos]
    sub = "Falta seu voto" if not ja_votei else (f"Falta: {', '.join(faltam)}" if faltam else "Todos votaram")

    if aberta:
        d = db.dias_restantes(v)
        prazo = ft.Row(
            [ft.Icon(ft.Icons.SCHEDULE, size=13, color=theme.MUTED),
             ft.Text("Encerra hoje" if d == 0 else f"Encerra em {d} dia{'s' if d != 1 else ''}",
                     size=10, color=theme.MUTED)],
            spacing=4,
        )
        etiqueta = pill("Proposta", theme.PRIMARY, theme.INFO_BG)
    else:
        aprovada = v.status == "aprovada"
        prazo = ft.Text(v.encerra_em.strftime("%d/%m/%Y"), size=10, color=theme.MUTED)
        etiqueta = pill("Aprovada" if aprovada else "Rejeitada",
                        theme.OK_TEXT if aprovada else theme.WARN_TEXT,
                        theme.OK_BG if aprovada else theme.WARN_BG)

    corpo = [
        ft.Row([etiqueta, prazo], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Text(v.titulo, size=17, weight=ft.FontWeight.W_700, color=theme.TEXT),
    ]
    if v.valor > 0:
        corpo += [
            ft.Text(brl(v.valor), size=26, weight=ft.FontWeight.W_700, color=theme.PRIMARY),
            ft.Row(
                [ft.Text("Cada um paga ", size=11, color=theme.TEXT),
                 ft.Text(brl(v.valor / total), size=11, weight=ft.FontWeight.W_700, color=theme.TEXT)],
                spacing=0,
            ),
        ]
    corpo += [
        ft.Container(height=2),
        ft.Row(
            [ft.Text(f"{n_votos} de {total} votos", size=11, weight=ft.FontWeight.W_600, color=theme.TEXT),
             ft.Text(f"{round(pct * 100)}%", size=11, color=theme.MUTED)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        ft.ProgressBar(value=pct, color=theme.PRIMARY, bgcolor="#E6E2D3", bar_height=7, border_radius=4),
        ft.Row(
            [
                ft.Row(avatares, spacing=-6),
                ft.Column(
                    [ft.Text(quem, size=11, weight=ft.FontWeight.W_600, color=theme.TEXT),
                     ft.Text(sub, size=10, color=theme.WARN_TEXT if not ja_votei and aberta else theme.MUTED)],
                    spacing=0, expand=True,
                ),
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    ]

    if aberta and not ja_votei:
        corpo.append(
            ft.Row(
                [
                    ft.Button(
                        content=ft.Row([ft.Icon(ft.Icons.CHECK, size=16, color=ft.Colors.WHITE),
                                        ft.Text("Concordo", size=13, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)],
                                       alignment=ft.MainAxisAlignment.CENTER, spacing=6),
                        bgcolor=theme.PRIMARY, height=44, expand=True,
                        on_click=lambda e: on_vote(v.id, True),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=22), elevation=0),
                    ),
                    ft.OutlinedButton(
                        content=ft.Row([ft.Icon(ft.Icons.CLOSE, size=16, color=theme.TEXT),
                                        ft.Text("Não concordo", size=13, weight=ft.FontWeight.W_600, color=theme.TEXT)],
                                       alignment=ft.MainAxisAlignment.CENTER, spacing=6),
                        height=44, expand=True,
                        on_click=lambda e: on_vote(v.id, False),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=22),
                                             side=ft.BorderSide(1, theme.TEXT)),
                    ),
                ],
                spacing=10,
            )
        )
    elif ja_votei:
        concordei = v.votos[eu.id]
        corpo.append(
            pill("Você concordou" if concordei else "Você não concordou",
                 theme.OK_TEXT if concordei else theme.WARN_TEXT,
                 theme.OK_BG if concordei else theme.WARN_BG, size=11)
        )
    return card(ft.Column(corpo, spacing=8), padding=16, radius=20)


def voting_view(page: ft.Page) -> ft.View:
    estado = {"aba": "abertas"}
    conteudo = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)

    async def voltar(e):
        await page.push_route(page.data.get("origem") or "/inicio")

    def votar(votacao_id: int, concorda: bool):
        db.votar(votacao_id, db.EU.id, concorda)
        show_message(page, "Voto registrado!")
        montar()

    def trocar_aba(chave: str):
        estado["aba"] = chave
        montar()

    def abrir_nova(e):
        titulo = app_field("Ex.: Comprar um sofá novo")
        valor = app_field("R$ 0,00 (opcional)", keyboard_type=ft.KeyboardType.NUMBER)
        prazo = ft.Dropdown(
            value="3",
            options=[ft.DropdownOption(key=k, text=t) for k, t in
                     [("1", "1 dia"), ("3", "3 dias"), ("7", "7 dias")]],
            filled=True, fill_color=theme.FIELD_BG, border_radius=10, border_color=theme.BORDER,
            text_size=13, content_padding=ft.Padding.symmetric(horizontal=12, vertical=0),
        )

        def salvar(ev):
            if not (titulo.value or "").strip():
                titulo.error_text = "Descreva a proposta"
                page.update()
                return
            db.adicionar_votacao(titulo.value.strip(), _para_float(valor.value), int(prazo.value))
            page.pop_dialog()
            estado["aba"] = "abertas"
            show_message(page, "Votação criada!")
            montar()

        page.show_dialog(
            ft.AlertDialog(
                title=ft.Text("Nova votação", size=16, weight=ft.FontWeight.W_700),
                bgcolor=theme.SURFACE,
                content=ft.Column(
                    [labeled("O que vai ser votado?", titulo), labeled("Valor total", valor),
                     labeled("Encerra em", prazo)],
                    tight=True, spacing=12, width=320,
                ),
                actions=[
                    ft.TextButton(content=ft.Text("Cancelar", color=theme.MUTED), on_click=lambda ev: page.pop_dialog()),
                    ft.TextButton(content=ft.Text("Criar", color=theme.PRIMARY, weight=ft.FontWeight.W_700),
                                  on_click=salvar),
                ],
            )
        )

    def montar(update: bool = True):
        abertas = estado["aba"] == "abertas"
        lista = db.votacoes(abertas)
        itens: list[ft.Control] = [
            segmented([("abertas", "Abertas"), ("encerradas", "Encerradas")], estado["aba"], trocar_aba)
        ]
        itens += [_cartao_votacao(v, votar) for v in lista] or [
            ft.Container(padding=30, alignment=ft.Alignment.CENTER,
                         content=ft.Text("Nenhuma votação por aqui", size=13, color=theme.MUTED))
        ]
        if abertas:
            itens.append(
                ft.Container(
                    padding=12, border_radius=12, bgcolor=theme.BUSY_BG,
                    content=ft.Row(
                        [ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color=theme.TEXT),
                         ft.Text("Se aprovada, a dívida será feita automaticamente.", size=11,
                                 color=theme.TEXT, expand=True)],
                        spacing=8,
                    ),
                )
            )
        conteudo.controls = itens
        if update:
            page.update()

    adicionar = ft.Container(
        padding=ft.Padding.only(left=16, right=8, top=8, bottom=8),
        border_radius=14,
        bgcolor=theme.SURFACE,
        border=ft.Border.all(1, theme.BORDER),
        on_click=abrir_nova,
        content=ft.Row(
            [
                ft.Text("Adicionar votação", size=13, color=theme.MUTED),
                ft.Container(
                    width=36, height=36, border_radius=10, bgcolor=theme.PRIMARY,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.ADD, size=20, color=ft.Colors.WHITE),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    view = ft.View(
        route="/votacao",
        bgcolor=theme.BG,
        padding=ft.Padding.symmetric(horizontal=18),
        controls=[
            ft.SafeArea(
                ft.Column(
                    [screen_header("Votação", db.CASA.nome, voltar), conteudo, adicionar, ft.Container(height=8)],
                    expand=True, spacing=12,
                ),
                expand=True,
            )
        ],
    )
    montar(update=False)  # a view ainda não está na página
    return view
