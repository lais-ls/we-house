import flet as ft

import theme
from components.ui import abrir_convite, avatar, bottom_nav, brl, card, logo, section_title, show_message
from services import dados_fake as db


def _resumo_card(titulo, valor, subtitulo, cor_valor, bg, borda) -> ft.Container:
    return ft.Container(
        expand=True,
        padding=14,
        border_radius=16,
        bgcolor=bg,
        border=ft.Border.all(1, borda),
        content=ft.Column(
            [
                ft.Text(titulo, size=11, color=theme.MUTED),
                ft.Text(valor, size=20, weight=ft.FontWeight.W_700, color=cor_valor),
                ft.Text(subtitulo, size=10, color=theme.MUTED),
            ],
            spacing=2,
        ),
    )


def _acao(icone, texto, on_click) -> ft.Container:
    return ft.Container(
        expand=True,
        on_click=on_click,
        ink=True,
        padding=ft.Padding.symmetric(vertical=14),
        border_radius=14,
        bgcolor=theme.SURFACE,
        border=ft.Border.all(1, theme.BORDER),
        content=ft.Column(
            [ft.Icon(icone, size=22, color=theme.TEXT), ft.Text(texto, size=11, color=theme.TEXT)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        ),
    )


def _linha_tarefa(tarefa) -> ft.Row:
    resp = db.morador_por_id(tarefa.responsavel_id)
    return ft.Row(
        [
            ft.Checkbox(value=tarefa.feita, active_color=theme.PRIMARY),
            ft.Column(
                [
                    ft.Text(tarefa.titulo, size=13, weight=ft.FontWeight.W_600, color=theme.TEXT),
                    ft.Text(tarefa.detalhe, size=10, color=theme.MUTED),
                ],
                spacing=0,
                expand=True,
            ),
            avatar(resp.inicial, resp.cor, 24),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def _linha_vencimento(v) -> ft.Container:
    icone = ft.Icons.WIFI if v.icone == "wifi" else ft.Icons.BOLT
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=12, vertical=10),
        border_radius=12,
        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
        content=ft.Row(
            [
                ft.Icon(icone, size=18, color=ft.Colors.WHITE),
                ft.Column(
                    [
                        ft.Text(v.titulo, size=12, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                        ft.Text(v.detalhe, size=10, color="#C9D0DE"),
                    ],
                    spacing=0,
                    expand=True,
                ),
                ft.Text(brl(v.valor), size=13, weight=ft.FontWeight.W_700, color=ft.Colors.WHITE),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )


def home_view(page: ft.Page) -> ft.View:
    async def ir(rota):
        await page.push_route(rota)

    async def ir_nova_conta(e):
        await ir("/nova-conta")

    async def ir_contas(e):
        await ir("/contas")

    async def ir_tarefas(e):
        await ir("/tarefas")

    def ir_origem_home(rota):
        async def handler(e):
            page.data["origem"] = "/inicio"
            await page.push_route(rota)
        return handler

    def convidar(e):
        abrir_convite(page, db.CASA.nome, db.CASA.codigo)

    def em_breve(e):
        show_message(page, "Em breve")

    eu = db.EU
    devo = db.total_pendente(db.dividas_que_eu_devo())
    recebo = db.total_pendente(db.dividas_que_me_devem())
    n_devo = len([d for d in db.dividas_que_eu_devo() if not d.pago])
    n_recebo = len([d for d in db.dividas_que_me_devem() if not d.pago])
    total_mes = sum(v.valor for v in db.VENCIMENTOS) + 15.0  # exemplo: parte da pessoa no mês

    topo = ft.Row(
        [
            ft.Row([logo(28), ft.Text("WeHouse", size=15, weight=ft.FontWeight.W_700, color=theme.TEXT)], spacing=8),
            ft.IconButton(ft.Icons.NOTIFICATIONS_NONE, icon_size=22, icon_color=theme.TEXT, on_click=em_breve),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    casa = card(
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(db.CASA.nome, size=13, weight=ft.FontWeight.W_700, color=theme.TEXT),
                        ft.Row(
                            [avatar(m.inicial, m.cor, 22) for m in db.CASA.moradores]
                            + [ft.Text(f"{len(db.CASA.moradores)} moradores", size=10, color=theme.MUTED)],
                            spacing=4,
                        ),
                    ],
                    spacing=6,
                    expand=True,
                ),
                ft.Container(
                    on_click=convidar,
                    ink=True,
                    padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                    border_radius=10,
                    bgcolor=theme.INFO_BG,
                    content=ft.Row(
                        [ft.Icon(ft.Icons.PERSON_ADD_ALT_1_OUTLINED, size=15, color=theme.PRIMARY),
                         ft.Text("Convidar", size=11, weight=ft.FontWeight.W_600, color=theme.PRIMARY)],
                        spacing=4,
                    ),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=14,
        radius=16,
    )

    resumo = ft.Row(
        [
            _resumo_card("Você deve", brl(devo), f"{n_devo} contas", theme.ACCENT, "#FFF1EA", "#FBD9C9"),
            _resumo_card("Você recebe", brl(recebo), f"{n_recebo} conta{'s' if n_recebo != 1 else ''}",
                         theme.SAGE_DARK, "#EAF4EE", "#CFE3D7"),
        ],
        spacing=12,
    )

    acoes = ft.Row(
        [
            _acao(ft.Icons.ADD_CARD_OUTLINED, "Nova conta", ir_nova_conta),
            _acao(ft.Icons.HOW_TO_VOTE_OUTLINED, "Votação", ir_origem_home("/votacao")),
            _acao(ft.Icons.EVENT_AVAILABLE_OUTLINED, "Reservar", ir_origem_home("/reservas")),
        ],
        spacing=10,
    )

    tarefas = card(
        ft.Column([_linha_tarefa(t) for t in db.tarefas(False)[:3]], spacing=6),
        padding=12,
        radius=16,
    )

    vencimentos = ft.Container(
        padding=16,
        border_radius=18,
        bgcolor=theme.PRIMARY,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Sua parte em outubro", size=11, color="#D5DAE6"),
                                ft.Text("Contas pendentes", size=10, color="#B8C0D2"),
                            ],
                            spacing=0,
                        ),
                        ft.Text(brl(total_mes), size=20, weight=ft.FontWeight.W_700, color=ft.Colors.WHITE),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                *[_linha_vencimento(v) for v in db.VENCIMENTOS],
            ],
            spacing=8,
        ),
    )

    conteudo = ft.Column(
        [
            topo,
            ft.Text(f"Bom dia, {eu.nome} 😊", size=22, weight=ft.FontWeight.W_700, color=theme.TEXT),
            ft.Text("Casa em dia, mais tempo pra viver.", size=12, color=theme.MUTED),
            casa,
            section_title("Resumo financeiro"),
            resumo,
            section_title("Ações rápidas"),
            acoes,
            section_title("Tarefas pendentes", "Ver todas", ir_tarefas),
            tarefas,
            section_title("Próximos vencimentos", "Ver mais", ir_contas),
            vencimentos,
            ft.Container(height=8),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.View(
        route="/inicio",
        bgcolor=theme.BG,
        padding=ft.Padding.symmetric(horizontal=18),
        controls=[ft.SafeArea(conteudo, expand=True)],
        navigation_bar=bottom_nav(page, 0),
    )
