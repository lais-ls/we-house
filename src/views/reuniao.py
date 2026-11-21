from datetime import datetime, time

import flet as ft

import theme
from components.ui import (
    app_field, avatar, card, labeled, pill, screen_header, segmented, show_message,
)
from services import dados_fake as db

DIAS_ABREV = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
MESES_ABREV = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro",
         "outubro", "novembro", "dezembro"]


def _data_extenso(d: datetime) -> str:
    return f"{DIAS_ABREV[d.weekday()]}, {d.day} de {MESES[d.month - 1]}"


def reuniao_view(page: ft.Page) -> ft.View:
    r = db.REUNIAO
    estado = {"aba": "ata"}
    corpo = ft.Column(spacing=14, scroll=ft.ScrollMode.AUTO, expand=True)

    tema = app_field("Ex.: Divisão da limpeza e contas de dezembro", value=r.tema)
    botao_tema = ft.Button(
        content=ft.Text("Salvar tema", size=12, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
        bgcolor=theme.PRIMARY, height=34, disabled=not r.tema,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=0),
    )
    anotacoes = ft.TextField(
        hint_text="Registre aqui o que foi conversado na reunião...",
        value=r.anotacoes, multiline=True, min_lines=3, max_lines=6,
        filled=True, fill_color=theme.FIELD_BG, border_radius=10, border_color=theme.BORDER,
        focused_border_color=theme.PRIMARY, text_size=13,
        hint_style=ft.TextStyle(size=13, color=theme.MUTED),
    )

    async def voltar(e):
        await page.push_route(page.data.get("origem") or "/inicio")

    # --- próxima reunião -----------------------------------------------------
    def confirmar(e):
        db.confirmar_presenca(db.EU.id)
        show_message(page, "Presença confirmada!")
        montar()

    def ao_escolher_data(e):
        v = e.control.value
        if not v:
            return
        nova = datetime.combine(v.date() if isinstance(v, datetime) else v, time(r.data.hour, r.data.minute))
        db.propor_nova_data(nova, db.EU.id)
        show_message(page, "Nova data sugerida para os moradores")
        montar()

    def escolher_outra(e):
        page.show_dialog(
            ft.DatePicker(
                value=r.data, first_date=datetime.now(), last_date=datetime(2035, 12, 31),
                on_change=ao_escolher_data,
            )
        )

    def card_proxima() -> ft.Container:
        confirmados = len(r.confirmados)
        total = len(db.CASA.moradores)
        eu_confirmei = db.EU.id in r.confirmados

        def morador(m):
            ok = m.id in r.confirmados
            return ft.Column(
                [
                    avatar(m.inicial, m.cor, 36),
                    ft.Text(m.nome, size=10, color=theme.TEXT),
                    pill("Confirmado" if ok else "Pendente",
                         theme.OK_TEXT if ok else theme.WARN_TEXT,
                         theme.OK_BG if ok else theme.WARN_BG, size=9),
                ],
                spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True,
            )

        botoes = [
            ft.Button(
                content=ft.Text("Data confirmada" if eu_confirmei else "Confirmar data", size=12,
                                weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                bgcolor=theme.PRIMARY, height=40, expand=True, disabled=eu_confirmei, on_click=confirmar,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), elevation=0),
            ),
            ft.OutlinedButton(
                content=ft.Text("Escolher outra data", size=12, weight=ft.FontWeight.W_600, color=theme.TEXT),
                height=40, expand=True, on_click=escolher_outra,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), side=ft.BorderSide(1, theme.TEXT)),
            ),
        ]
        return card(
            ft.Column(
                [
                    ft.Row(
                        [ft.Text("Próxima reunião", size=13, weight=ft.FontWeight.W_700, color=theme.TEXT),
                         pill("Data confirmada" if r.confirmada else "Data sugerida",
                              theme.OK_TEXT if r.confirmada else theme.PRIMARY,
                              theme.OK_BG if r.confirmada else theme.INFO_BG)],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                width=52, height=56, border_radius=12, bgcolor=theme.PRIMARY,
                                alignment=ft.Alignment.CENTER,
                                content=ft.Column(
                                    [ft.Text(MESES_ABREV[r.data.month - 1], size=9, color="#D5DAE6"),
                                     ft.Text(str(r.data.day), size=20, weight=ft.FontWeight.W_700, color=ft.Colors.WHITE)],
                                    spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ),
                            ft.Column(
                                [ft.Text(_data_extenso(r.data), size=15, weight=ft.FontWeight.W_700, color=theme.TEXT),
                                 ft.Text(f"às {r.data.hour}h · {r.local}", size=11, color=theme.MUTED)],
                                spacing=0,
                            ),
                        ],
                        spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=14, color=theme.OK_TEXT),
                         ft.Text(f"Todos os {total} moradores estão disponíveis", size=11, color=theme.OK_TEXT)],
                        spacing=6,
                    ),
                    ft.Row([morador(m) for m in db.CASA.moradores], spacing=4),
                    ft.Text(f"{confirmados} de {total} confirmaram", size=10, color=theme.MUTED),
                    ft.Row(botoes, spacing=10),
                ],
                spacing=10,
            ),
            padding=16, radius=18,
        )

    # --- tema ------------------------------------------------------------------
    def ao_digitar_tema(e):
        botao_tema.disabled = not (tema.value or "").strip()
        page.update()

    def salvar_tema(e):
        r.tema = tema.value.strip()
        show_message(page, "Tema salvo")

    tema.on_change = ao_digitar_tema
    botao_tema.on_click = salvar_tema

    def card_tema() -> ft.Container:
        return card(
            ft.Column(
                [
                    ft.Text("Tema da reunião", size=13, weight=ft.FontWeight.W_700, color=theme.TEXT),
                    tema,
                    ft.Row([botao_tema], alignment=ft.MainAxisAlignment.END),
                ],
                spacing=10,
            ),
            padding=16, radius=18,
        )

    # --- ata -------------------------------------------------------------------
    def alternar(c):
        def handler(e):
            c.feito = bool(e.control.value)
        return handler

    def linha_combinado(c) -> ft.Control:
        resp = db.morador_por_id(c.responsavel_id)
        return ft.Container(
            padding=ft.Padding.symmetric(vertical=8),
            border=ft.Border(bottom=ft.BorderSide(1, theme.BORDER)),
            content=ft.Row(
                [
                    ft.Checkbox(value=c.feito, active_color=theme.PRIMARY, on_change=alternar(c)),
                    ft.Text(c.texto, size=12, color=theme.TEXT, expand=True),
                    ft.Column(
                        [avatar(resp.inicial, resp.cor, 28), ft.Text(c.prazo, size=9, color=theme.MUTED)],
                        spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=4,
            ),
        )

    def novo_combinado(e):
        texto = app_field("Ex.: Lavar a louça em dupla")
        resp = ft.Dropdown(
            value=str(db.EU.id),
            options=[ft.DropdownOption(key=str(m.id), text="Você" if m.id == db.EU.id else m.nome)
                     for m in db.CASA.moradores],
            filled=True, fill_color=theme.FIELD_BG, border_radius=10, border_color=theme.BORDER,
            text_size=13, content_padding=ft.Padding.symmetric(horizontal=12, vertical=0),
        )
        prazo = app_field("Ex.: Dia 15, Toda sem., Sempre")

        def salvar(ev):
            if not (texto.value or "").strip():
                texto.error_text = "Descreva o combinado"
                page.update()
                return
            r.combinados.append(
                db.Combinado(texto.value.strip(), int(resp.value), (prazo.value or "").strip() or "Sempre")
            )
            page.pop_dialog()
            montar()

        page.show_dialog(
            ft.AlertDialog(
                title=ft.Text("Novo combinado", size=16, weight=ft.FontWeight.W_700),
                bgcolor=theme.SURFACE,
                content=ft.Column(
                    [labeled("O que ficou combinado?", texto), labeled("Responsável", resp), labeled("Prazo", prazo)],
                    tight=True, spacing=12, width=320,
                ),
                actions=[
                    ft.TextButton(content=ft.Text("Cancelar", color=theme.MUTED), on_click=lambda ev: page.pop_dialog()),
                    ft.TextButton(content=ft.Text("Adicionar", color=theme.PRIMARY, weight=ft.FontWeight.W_700),
                                  on_click=salvar),
                ],
            )
        )

    def salvar_ata(e):
        if not (anotacoes.value or "").strip() and not r.combinados:
            show_message(page, "Escreva as anotações ou adicione um combinado")
            return
        db.salvar_ata(anotacoes.value or "")
        anotacoes.value = ""
        tema.value = ""
        botao_tema.disabled = True
        estado["aba"] = "historico"
        show_message(page, "Ata salva no histórico!")
        montar()

    def card_ata() -> ft.Container:
        return card(
            ft.Column(
                [
                    ft.Text("Anotações da reunião", size=13, weight=ft.FontWeight.W_700, color=theme.TEXT),
                    anotacoes,
                    ft.Container(height=2),
                    ft.Text("Combinados", size=13, weight=ft.FontWeight.W_700, color=theme.TEXT),
                    ft.Column([linha_combinado(c) for c in r.combinados], spacing=0),
                    ft.Container(
                        height=40, border_radius=12, alignment=ft.Alignment.CENTER,
                        border=ft.Border.all(1, theme.MUTED), on_click=novo_combinado, ink=True,
                        content=ft.Row(
                            [ft.Icon(ft.Icons.ADD, size=16, color=theme.TEXT),
                             ft.Text("Adicionar combinado", size=12, color=theme.TEXT)],
                            alignment=ft.MainAxisAlignment.CENTER, spacing=6,
                        ),
                    ),
                    ft.Row(
                        [ft.Button(
                            content=ft.Text("Salvar ata", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                            bgcolor=theme.PRIMARY, height=46, expand=True, on_click=salvar_ata,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), elevation=0),
                        )]
                    ),
                ],
                spacing=10,
            ),
            padding=16, radius=18,
        )

    # --- histórico --------------------------------------------------------------
    def card_historico(item) -> ft.Container:
        data, titulo, texto, combinados = item
        return card(
            ft.Column(
                [
                    ft.Row([ft.Text(titulo, size=14, weight=ft.FontWeight.W_700, color=theme.TEXT),
                            ft.Text(data.strftime("%d/%m/%Y"), size=10, color=theme.MUTED)],
                           alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(texto or "Sem anotações.", size=12, color=theme.TEXT),
                    *[
                        ft.Row(
                            [ft.Icon(ft.Icons.CHECK_BOX if c.feito else ft.Icons.CHECK_BOX_OUTLINE_BLANK,
                                     size=16, color=theme.PRIMARY),
                             ft.Text(c.texto, size=11, color=theme.MUTED, expand=True),
                             avatar(db.morador_por_id(c.responsavel_id).inicial,
                                    db.morador_por_id(c.responsavel_id).cor, 20)],
                            spacing=6,
                        )
                        for c in combinados
                    ],
                ],
                spacing=8,
            ),
            padding=16, radius=18,
        )

    def trocar_aba(chave: str):
        estado["aba"] = chave
        montar()

    def montar(update: bool = True):
        seletor = segmented([("ata", "Ata"), ("historico", "Histórico")], estado["aba"], trocar_aba)
        if estado["aba"] == "ata":
            corpo.controls = [card_proxima(), card_tema(), seletor, card_ata(), ft.Container(height=8)]
        else:
            itens = [card_historico(i) for i in db.HISTORICO_REUNIOES] or [
                ft.Container(padding=30, alignment=ft.Alignment.CENTER,
                             content=ft.Text("Nenhuma ata salva ainda", size=13, color=theme.MUTED))
            ]
            corpo.controls = [card_proxima(), seletor, *itens, ft.Container(height=8)]
        if update:
            page.update()

    montar(update=False)
    return ft.View(
        route="/reuniao",
        bgcolor=theme.BG,
        padding=ft.Padding.symmetric(horizontal=18),
        controls=[
            ft.SafeArea(
                ft.Column([screen_header("Reunião mensal", db.CASA.nome, voltar), corpo], expand=True, spacing=12),
                expand=True,
            )
        ],
    )
