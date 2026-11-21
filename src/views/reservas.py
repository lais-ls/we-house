from datetime import date, datetime, timedelta

import flet as ft

import theme
from components.ui import screen_header, show_message
from services import dados_fake as db

DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
DIAS_LONGOS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

CELULA_W = 40
CELULA_H = 38


def _intervalo_semana(seg: date) -> str:
    dom = seg + timedelta(days=6)
    return f"{seg.day} {MESES[seg.month - 1]} – {dom.day} {MESES[dom.month - 1]}"


def reservas_view(page: ft.Page) -> ft.View:
    estado = {
        "recurso": db.RECURSOS[0],
        "semana": db.segunda_da_semana(date.today()),
        "sel": None,  # (dia, hora) escolhido, ainda não reservado
    }
    chips = ft.Row(spacing=8, scroll=ft.ScrollMode.AUTO)
    titulo_semana = ft.Text("", size=13, weight=ft.FontWeight.W_700, color=theme.TEXT)
    grade = ft.Column(spacing=6)
    resumo = ft.Text("", size=13, weight=ft.FontWeight.W_700, color=theme.TEXT)
    recurso_txt = ft.Text("", size=11, color=theme.MUTED)
    botao_texto = ft.Text("Reservar horário", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
    botao = ft.Container(
        height=48, border_radius=24, bgcolor=theme.PRIMARY, ink=True,
        alignment=ft.Alignment.CENTER,
        shadow=ft.BoxShadow(blur_radius=14, color=ft.Colors.with_opacity(0.25, theme.PRIMARY), offset=ft.Offset(0, 4)),
        content=ft.Row(
            [ft.Icon(ft.Icons.CALENDAR_TODAY_OUTLINED, size=16, color=ft.Colors.WHITE), botao_texto],
            alignment=ft.MainAxisAlignment.CENTER, spacing=8,
        ),
    )

    async def voltar(e):
        await page.push_route(page.data.get("origem") or "/inicio")

    def passado(dia: date, hora: int) -> bool:
        return datetime(dia.year, dia.month, dia.day, hora + 2) <= datetime.now()

    def escolher_recurso(nome: str):
        def handler(e):
            estado["recurso"] = nome
            estado["sel"] = None
            montar()
        return handler

    def mudar_semana(delta: int):
        def handler(e):
            estado["semana"] += timedelta(weeks=delta)
            estado["sel"] = None
            montar()
        return handler

    def tocar_celula(dia: date, hora: int):
        def handler(e):
            r = db.reserva_em(estado["recurso"], dia, hora)
            if r and r.morador_id == db.EU.id:
                db.cancelar_reserva(estado["recurso"], dia, hora, db.EU.id)
                show_message(page, "Reserva cancelada")
            elif r is None and not passado(dia, hora):
                estado["sel"] = None if estado["sel"] == (dia, hora) else (dia, hora)
            montar()
        return handler

    def reservar(e):
        if not estado["sel"]:
            show_message(page, "Escolha um horário livre na grade")
            return
        dia, hora = estado["sel"]
        if db.reservar(estado["recurso"], dia, hora, db.EU.id):
            show_message(page, f"{estado['recurso']} reservada!")
        estado["sel"] = None
        montar()

    botao.on_click = reservar

    def celula(dia: date, hora: int) -> ft.Container:
        r = db.reserva_em(estado["recurso"], dia, hora)
        selecionada = estado["sel"] == (dia, hora)
        eu = r is not None and r.morador_id == db.EU.id
        if r and not eu:
            bg, borda, cor, txt = theme.BUSY_BG, theme.BUSY_BG, theme.PRIMARY, db.morador_por_id(r.morador_id).nome
        elif eu or selecionada:
            bg, borda, cor, txt = theme.PRIMARY, theme.PRIMARY, ft.Colors.WHITE, db.EU.nome
        else:
            bg, borda, cor, txt = theme.SURFACE, theme.BORDER, theme.PRIMARY, ""
        return ft.Container(
            width=CELULA_W, height=CELULA_H, border_radius=8, bgcolor=bg,
            border=ft.Border.all(1, borda), alignment=ft.Alignment.CENTER,
            opacity=0.4 if passado(dia, hora) and r is None else 1,
            on_click=tocar_celula(dia, hora),
            content=ft.Text(txt, size=9, weight=ft.FontWeight.W_600, color=cor, max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS),
        )

    def montar(update: bool = True):
        chips.controls = [
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                border_radius=18,
                bgcolor=theme.PRIMARY if n == estado["recurso"] else ft.Colors.TRANSPARENT,
                border=ft.Border.all(1, theme.PRIMARY if n == estado["recurso"] else theme.BORDER),
                on_click=escolher_recurso(n),
                content=ft.Text(n, size=12, weight=ft.FontWeight.W_600,
                                color=ft.Colors.WHITE if n == estado["recurso"] else theme.TEXT),
            )
            for n in db.RECURSOS
        ]
        seg = estado["semana"]
        titulo_semana.value = _intervalo_semana(seg)
        dias = [seg + timedelta(days=i) for i in range(7)]

        cab = ft.Row(
            [ft.Container(width=26)]
            + [
                ft.Container(
                    width=CELULA_W, padding=ft.Padding.symmetric(vertical=3), border_radius=8,
                    bgcolor=theme.BUSY_BG if d == date.today() else ft.Colors.TRANSPARENT,
                    content=ft.Column(
                        [ft.Text(DIAS[i], size=9, color=theme.MUTED),
                         ft.Text(str(d.day), size=11, weight=ft.FontWeight.W_700, color=theme.TEXT)],
                        spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
                for i, d in enumerate(dias)
            ],
            spacing=4, alignment=ft.MainAxisAlignment.CENTER,
        )
        linhas = [
            ft.Row(
                [ft.Container(width=26, content=ft.Text(f"{h}h", size=9, color=theme.MUTED))]
                + [celula(d, h) for d in dias],
                spacing=4, alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            for h in db.HORARIOS
        ]
        grade.controls = [cab, *linhas]

        if estado["sel"]:
            dia, hora = estado["sel"]
            resumo.value = f"{DIAS_LONGOS[dia.weekday()]}, {dia.day} · {hora}h às {hora + 2}h"
            botao.bgcolor = theme.PRIMARY
        else:
            resumo.value = "Escolha um horário livre"
            botao.bgcolor = "#A9B1C2"
        recurso_txt.value = estado["recurso"]
        if update:
            page.update()

    def legenda(cor_fundo, cor_borda, texto):
        return ft.Row(
            [ft.Container(width=14, height=14, border_radius=4, bgcolor=cor_fundo, border=ft.Border.all(1, cor_borda)),
             ft.Text(texto, size=10, color=theme.MUTED)],
            spacing=5,
        )

    legendas = ft.Row(
        [legenda(theme.SURFACE, theme.BORDER, "Livre"),
         legenda(theme.BUSY_BG, theme.BUSY_BG, "Ocupado"),
         legenda(theme.PRIMARY, theme.PRIMARY, "Sua reserva")],
        spacing=16, alignment=ft.MainAxisAlignment.CENTER,
    )

    def seta(icone, handler):
        return ft.IconButton(icone, icon_size=18, icon_color=theme.TEXT, on_click=handler,
                             style=ft.ButtonStyle(shape=ft.CircleBorder(), side=ft.BorderSide(1, theme.BORDER)))

    navegacao = ft.Row(
        [seta(ft.Icons.CHEVRON_LEFT, mudar_semana(-1)), titulo_semana, seta(ft.Icons.CHEVRON_RIGHT, mudar_semana(1))],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    conteudo = ft.Column(
        [chips, navegacao, grade, legendas],
        spacing=14, scroll=ft.ScrollMode.AUTO, expand=True,
    )

    montar(update=False)
    return ft.View(
        route="/reservas",
        bgcolor=theme.BG,
        padding=ft.Padding.symmetric(horizontal=18),
        controls=[
            ft.SafeArea(
                ft.Column(
                    [
                        screen_header("Reservar", db.CASA.nome, voltar),
                        conteudo,
                        ft.Row([resumo, recurso_txt], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        botao,
                        ft.Container(height=8),
                    ],
                    expand=True, spacing=12,
                ),
                expand=True,
            )
        ],
    )
