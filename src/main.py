import flet as ft

import theme
from views.create_house import create_house_view
from views.join_house import join_house_view
from views.login import login_view
from views.options import options_view

# rota -> função que monta a tela
ROUTES = {
    "/": login_view,
    "/opcoes": options_view,
    "/criar-casa": create_house_view,
    "/entrar-casa": join_house_view,
    # Adicione as próximas telas aqui:
    # "/inicio": home_view,
}

# De qual tela cada rota "volta" (o que fica embaixo na pilha). Sem pai = tela raiz.
PARENT = {
    "/criar-casa": "/opcoes",
    "/entrar-casa": "/opcoes",
}


def main(page: ft.Page):
    page.title = "We House"
    page.bgcolor = theme.BG
    page.padding = 0

    # Tamanho de celular só para visualizar no computador
    page.window.width = 390
    page.window.height = 844

    def route_change(e: ft.RouteChangeEvent):
        route = e.route if e.route in ROUTES else "/"
        pilha = []
        pai = PARENT.get(route)
        if pai:
            pilha.append(ROUTES[pai](page))
        pilha.append(ROUTES[route](page))
        page.views = pilha
        page.update()

    async def view_pop(e: ft.ViewPopEvent):
        # botão "voltar" do Android / gesto de voltar
        pai = PARENT.get(page.route)
        await page.push_route(pai or "/")

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change(ft.RouteChangeEvent(name="route_change", data="/", control=page, route="/"))


ft.run(main)
