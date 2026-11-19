from datetime import date, datetime

import flet as ft

import theme
from components.ui import app_field, avatar, brl, card, labeled, primary_button, show_message
from services import dados_fake as db


def _para_float(texto: str | None) -> float:
    """'R$ 240,00' / '240,5' / '1.200,00' -> float (0 se inválido)."""
    limpo = "".join(c for c in (texto or "") if c.isdigit() or c in ",.")
    if "," in limpo:
        limpo = limpo.replace(".", "").replace(",", ".")
    try:
        return float(limpo)
    except ValueError:
        return 0.0


def new_bill_view(page: ft.Page) -> ft.View:
    moradores = db.CASA.moradores
    selecionados = {m.id: True for m in moradores}
    valores_custom: dict[int, ft.TextField] = {}
    estado = {"modo": "igual", "data": date.today()}

    descricao = app_field("Ex.: Compras do mercado")
    valor = app_field("R$ 0,00", keyboard_type=ft.KeyboardType.NUMBER)
    pagador = ft.Dropdown(
        value=str(db.EU.id),
        options=[ft.DropdownOption(key=str(m.id), text="Você" if m.id == db.EU.id else m.nome) for m in moradores],
        filled=True,
        fill_color=theme.FIELD_BG,
        border_radius=10,
        border_color=theme.BORDER,
        text_size=13,
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=0),
        expand=True,
    )
    venc_texto = ft.Text(estado["data"].strftime("%d/%m/%Y"), size=13, color=theme.TEXT)
    lista = ft.Column(spacing=8)
    contador = ft.Text("", size=11, color=theme.MUTED)
    rodape_info = ft.Text("", size=11, color=theme.MUTED)
    segmentado = ft.Row(spacing=0)

    def total() -> float:
        return _para_float(valor.value)

    def parte_igual() -> float:
        n = sum(selecionados.values())
        return total() / n if n else 0.0

    def partes() -> dict[int, float]:
        if estado["modo"] == "igual":
            p = round(parte_igual(), 2)
            return {mid: p for mid, ativo in selecionados.items() if ativo}
        return {mid: _para_float(valores_custom[mid].value) for mid, ativo in selecionados.items() if ativo}

    def redesenhar(update: bool = True):
        n = sum(selecionados.values())
        contador.value = f"{n} de {len(moradores)} moradores"
        segmentado.controls = [
            _segmento("Dividir igualmente", "igual", estado["modo"] == "igual", tocar_modo),
            _segmento("Personalizado", "custom", estado["modo"] == "custom", tocar_modo),
        ]
        linhas = []
        for m in moradores:
            ativo = selecionados[m.id]
            if estado["modo"] == "igual":
                lado = ft.Text(
                    brl(parte_igual()) if ativo else "—",
                    size=13, weight=ft.FontWeight.W_700, color=theme.TEXT if ativo else theme.MUTED,
                )
            else:
                campo = valores_custom[m.id]
                campo.disabled = not ativo
                lado = campo
            linhas.append(
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                    border_radius=12,
                    bgcolor=theme.SURFACE,
                    border=ft.Border.all(1, theme.BORDER),
                    content=ft.Row(
                        [
                            ft.Checkbox(value=ativo, active_color=theme.PRIMARY, on_change=tocar_morador(m.id)),
                            avatar(m.inicial, m.cor, 26),
                            ft.Text(
                                m.nome + (" (você)" if m.id == db.EU.id else ""),
                                size=13, color=theme.TEXT, expand=True,
                            ),
                            lado,
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                )
            )
        lista.controls = linhas

        if estado["modo"] == "igual":
            rodape_info.value = f"{brl(total())} ÷ {n} = {brl(parte_igual())} por pessoa" if n else "Selecione alguém"
            rodape_info.color = theme.MUTED
        else:
            soma = sum(partes().values())
            falta = round(total() - soma, 2)
            rodape_info.value = (
                f"Soma das partes: {brl(soma)} de {brl(total())}"
                + ("" if falta == 0 else f"  (faltam {brl(falta)})" if falta > 0 else f"  (passou {brl(-falta)})")
            )
            rodape_info.color = theme.MUTED if falta == 0 else theme.ACCENT
        if update:
            page.update()

    def tocar_modo(modo: str):
        estado["modo"] = modo
        if modo == "custom":
            for mid, campo in valores_custom.items():
                campo.value = f"{parte_igual():.2f}".replace(".", ",") if selecionados[mid] else ""
        redesenhar()

    def tocar_morador(mid: int):
        def handler(e):
            selecionados[mid] = bool(e.control.value)
            redesenhar()
        return handler

    def ao_digitar_valor(e):
        redesenhar()

    valor.on_change = ao_digitar_valor

    for m in moradores:
        valores_custom[m.id] = ft.TextField(
            width=92, height=34, text_size=12, text_align=ft.TextAlign.RIGHT,
            filled=True, fill_color=theme.FIELD_BG, border_radius=8, border_color=theme.BORDER,
            content_padding=ft.Padding.symmetric(horizontal=8, vertical=0),
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=lambda e: redesenhar(),
        )

    def ao_escolher_data(e):
        if e.control.value:
            v = e.control.value
            estado["data"] = v.date() if isinstance(v, datetime) else v
            venc_texto.value = estado["data"].strftime("%d/%m/%Y")
            page.update()

    def abrir_calendario(e):
        page.show_dialog(
            ft.DatePicker(
                value=datetime.combine(estado["data"], datetime.min.time()),
                first_date=datetime(2024, 1, 1),
                last_date=datetime(2035, 12, 31),
                on_change=ao_escolher_data,
            )
        )

    async def voltar(e):
        await page.push_route(page.data.get("anterior") or "/contas")

    async def salvar(e):
        descricao.error_text = None if (descricao.value or "").strip() else "Informe uma descrição"
        valor.error_text = None if total() > 0 else "Informe um valor maior que zero"
        page.update()
        if descricao.error_text or valor.error_text:
            return
        p = partes()
        if not p:
            show_message(page, "Selecione pelo menos um morador")
            return
        if estado["modo"] == "custom" and abs(sum(p.values()) - total()) > 0.01:
            show_message(page, "A soma das partes precisa ser igual ao valor total")
            return
        # TODO: salvar no banco
        db.adicionar_conta(
            descricao.value.strip(), total(), int(pagador.value), p, estado["data"].strftime("%d/%m/%Y")
        )
        show_message(page, "Conta salva!")
        await page.push_route("/contas")

    data_campo = ft.Container(
        height=46,
        padding=ft.Padding.symmetric(horizontal=12),
        border_radius=10,
        bgcolor=theme.FIELD_BG,
        border=ft.Border.all(1, theme.BORDER),
        on_click=abrir_calendario,
        expand=True,
        content=ft.Row(
            [venc_texto, ft.Icon(ft.Icons.CALENDAR_TODAY_OUTLINED, size=16, color=theme.MUTED)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    formulario = card(
        ft.Column(
            [
                labeled("Descrição", descricao),
                labeled("Valor total", valor),
                ft.Row(
                    [
                        ft.Column([ft.Text("Quem pagou", size=12, weight=ft.FontWeight.W_600, color=theme.TEXT), pagador],
                                  spacing=6, expand=True),
                        ft.Column([ft.Text("Vencimento", size=12, weight=ft.FontWeight.W_600, color=theme.TEXT), data_campo],
                                  spacing=6, expand=True),
                    ],
                    spacing=12,
                ),
            ],
            spacing=12,
        ),
        padding=16,
        radius=18,
    )

    redesenhar(update=False)

    conteudo = ft.Column(
        [
            formulario,
            ft.Row(
                [ft.Text("Dividir entre", size=14, weight=ft.FontWeight.W_700, color=theme.TEXT), contador],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Container(content=segmentado, bgcolor="#EDE9DF", padding=3, border_radius=12),
            lista,
            rodape_info,
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    cabecalho = ft.Row(
        [
            ft.IconButton(ft.Icons.ARROW_BACK, icon_size=20, icon_color=theme.TEXT, on_click=voltar),
            ft.Column(
                [
                    ft.Text("Nova conta", size=17, weight=ft.FontWeight.W_600, color=theme.TEXT),
                    ft.Text(db.CASA.nome, size=11, color=theme.MUTED),
                ],
                spacing=0,
            ),
        ],
        spacing=4,
    )

    return ft.View(
        route="/nova-conta",
        bgcolor=theme.BG,
        padding=ft.Padding.symmetric(horizontal=18),
        controls=[
            ft.SafeArea(
                ft.Column([cabecalho, conteudo, primary_button("Salvar conta", salvar), ft.Container(height=8)], expand=True),
                expand=True,
            )
        ],
    )


def _segmento(texto: str, chave: str, ativo: bool, on_tap) -> ft.Container:
    return ft.Container(
        expand=True,
        height=36,
        border_radius=10,
        bgcolor=theme.SURFACE if ativo else ft.Colors.TRANSPARENT,
        alignment=ft.Alignment.CENTER,
        on_click=lambda e: on_tap(chave),
        content=ft.Text(texto, size=12, weight=ft.FontWeight.W_600, color=theme.TEXT if ativo else theme.MUTED),
    )
