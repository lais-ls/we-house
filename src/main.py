import flet as ft

import theme
from views.bills import bills_view
from views.create_house import create_house_view
from views.home import home_view
from views.join_house import join_house_view
from views.login import login_view
from views.mais import mais_view
from views.new_bill import new_bill_view
from views.options import options_view
from views.pix import pix_view
from views.reservas import reservas_view
from views.reuniao import reuniao_view
from views.tarefas import tarefas_view
from views.voting import voting_view
from views.compras import compras_view

ROUTES = {
    "/": login_view,
    "/opcoes": options_view,
    "/criar-casa": create_house_view,
    "/entrar-casa": join_house_view,
    "/inicio": home_view,
    "/contas": bills_view,
    "/nova-conta": new_bill_view,
    "/pix": pix_view,
    "/tarefas": tarefas_view,
    "/mais": mais_view,
    "/votacao": voting_view,
    "/reservas": reservas_view,
    "/reuniao": reuniao_view,
    "/compras": compras_view,
}

PARENT = {
    "/criar-casa": "/opcoes",
    "/entrar-casa": "/opcoes",
}


def main(page: ft.Page):
    page.title = "We House"
    page.bgcolor = theme.BG
    page.padding = 0
    page.data = {} 

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
        pai = PARENT.get(page.route) or page.data.get("origem")
        await page.push_route(pai or "/")

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change(ft.RouteChangeEvent(name="route_change", data="/", control=page, route="/"))


ft.run(main)
