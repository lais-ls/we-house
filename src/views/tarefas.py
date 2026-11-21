import flet as ft

import theme
from components.ui import (
    app_field, avatar, bottom_nav, card, labeled, pill, segmented, show_message,
)
from services import dados_fake as db

HORAS = [f"{h}h" for h in range(7, 24)]


def _dropdown(opcoes: list[tuple[str, str]], valor: str) -> ft.Dropdown:
    return ft.Dropdown(
        value=valor,
        options=[ft.DropdownOption(key=k, text=t) for k, t in opcoes],
        filled=True, fill_color=theme.FIELD_BG, border_radius=10, border_color=theme.BORDER,
        text_size=13, content_padding=ft.Padding.symmetric(horizontal=12, vertical=0),
    )


def tarefas_view(page: ft.Page) -> ft.View:
    estado = {"aba": "pendentes"}
    lista = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    contador = ft.Text("", size=11, color=theme.MUTED)
    seletor = ft.Container()
    titulo_lista = ft.Text("Sua casa hoje", size=13, weight=ft.FontWeight.W_700, color=theme.TEXT)

    def alternar(tarefa_id: int):
        def handler(e):
            db.alternar_tarefa(tarefa_id, bool(e.control.value))
            montar()
        return handler

    def trocar_aba(chave: str):
        estado["aba"] = chave
        montar()

    def linha(t) -> ft.Container:
        resp = db.morador_por_id(t.responsavel_id)
        hoje = t.detalhe.lower().startswith("hoje") and not t.feita
        return card(
            ft.Row(
                [
                    ft.Checkbox(value=t.feita, active_color=theme.PRIMARY, on_change=alternar(t.id)),
                    ft.Column(
                        [
                            ft.Text(
                                t.titulo, size=14, weight=ft.FontWeight.W_700,
                                color=theme.MUTED if t.feita else theme.TEXT,
                                style=ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH if t.feita else None),
                            ),
                            ft.Row(
                                [
                                    pill(t.detalhe,
                                         theme.WARN_TEXT if hoje else theme.PRIMARY,
                                         theme.WARN_BG if hoje else theme.INFO_BG),
                                    ft.Text(resp.nome + (" (você)" if resp.id == db.EU.id else ""),
                                            size=11, color=theme.MUTED),
                                ],
                                spacing=8,
                            ),
                        ],
                        spacing=4, expand=True,
                    ),
                    avatar(resp.inicial, resp.cor, 36),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=4,
            ),
            padding=ft.Padding.symmetric(horizontal=10, vertical=12), radius=16,
        )

    def montar(update: bool = True):
        pendentes = estado["aba"] == "pendentes"
        itens = db.tarefas(not pendentes)
        seletor.content = segmented(
            [("pendentes", "Pendentes"), ("concluidas", "Concluídas")], estado["aba"], trocar_aba
        )
        titulo_lista.value = "Sua casa hoje" if pendentes else "Já resolvidas"
        n = len(itens)
        contador.value = f"{n} pendente{'s' if n != 1 else ''}" if pendentes else f"{n} concluída{'s' if n != 1 else ''}"
        lista.controls = [linha(t) for t in itens] or [
            ft.Container(
                padding=30, alignment=ft.Alignment.CENTER,
                content=ft.Text("Tudo em dia 🎉" if pendentes else "Nenhuma tarefa concluída ainda",
                                size=13, color=theme.MUTED),
            )
        ]
        if update:
            page.update()

    def abrir_nova(e):
        titulo = app_field("Ex.: Passar pano na sala")
        resp = _dropdown(
            [(str(m.id), "Você" if m.id == db.EU.id else m.nome) for m in db.CASA.moradores], str(db.EU.id)
        )
        dia = _dropdown([("Hoje", "Hoje"), ("Amanhã", "Amanhã")], "Hoje")
        hora = _dropdown([(h, h) for h in HORAS], "18h")

        def salvar(ev):
            if not (titulo.value or "").strip():
                titulo.error_text = "Dê um nome para a tarefa"
                page.update()
                return
            db.adicionar_tarefa(titulo.value.strip(), int(resp.value), f"{dia.value} · {hora.value}")
            page.pop_dialog()
            estado["aba"] = "pendentes"
            show_message(page, "Tarefa criada!")
            montar()

        page.show_dialog(
            ft.AlertDialog(
                title=ft.Text("Nova tarefa", size=16, weight=ft.FontWeight.W_700),
                bgcolor=theme.SURFACE,
                content=ft.Column(
                    [
                        labeled("O que precisa ser feito?", titulo),
                        labeled("Responsável", resp),
                        ft.Row([ft.Column([ft.Text("Dia", size=12, weight=ft.FontWeight.W_600, color=theme.TEXT), dia],
                                          spacing=6, expand=True),
                                ft.Column([ft.Text("Hora", size=12, weight=ft.FontWeight.W_600, color=theme.TEXT), hora],
                                          spacing=6, expand=True)], spacing=10),
                    ],
                    tight=True, spacing=12, width=320,
                ),
                actions=[
                    ft.TextButton(content=ft.Text("Cancelar", color=theme.MUTED), on_click=lambda ev: page.pop_dialog()),
                    ft.TextButton(content=ft.Text("Criar", color=theme.PRIMARY, weight=ft.FontWeight.W_700),
                                  on_click=salvar),
                ],
            )
        )

    topo = ft.Column(
        [ft.Text("Tarefas", size=24, weight=ft.FontWeight.W_700, color=theme.TEXT),
         ft.Text(db.CASA.nome, size=11, color=theme.MUTED)],
        spacing=0,
    )

    montar(update=False)
    return ft.View(
        route="/tarefas",
        bgcolor=theme.BG,
        padding=ft.Padding.symmetric(horizontal=18),
        controls=[
            ft.SafeArea(
                ft.Column(
                    [
                        topo, seletor,
                        ft.Row([titulo_lista, contador], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        lista,
                    ],
                    spacing=12, expand=True,
                ),
                expand=True,
            )
        ],
        floating_action_button=ft.FloatingActionButton(
            icon=ft.Icons.ADD, bgcolor=theme.PRIMARY, foreground_color=ft.Colors.WHITE,
            shape=ft.CircleBorder(), on_click=abrir_nova,
        ),
        navigation_bar=bottom_nav(page, 2),
    )
