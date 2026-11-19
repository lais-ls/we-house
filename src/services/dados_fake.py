"""Sample data for the MVP. Replace these functions with database queries later."""

from models.models import Casa, Divida, Morador, Tarefa, Vencimento

EU = Morador(1, "Bia", "#F7C2B2")
LUCAS = Morador(2, "Lucas", "#C8C2EE")
ANA = Morador(3, "Ana", "#B8D3C2")
MARINA = Morador(4, "Marina", "#E2D08E")

CASA = Casa("República Bela Vista", [EU, LUCAS, ANA, MARINA])

DIVIDAS: list[Divida] = [
    # eu devo
    Divida(1, "Compras do mercado", 50.00, LUCAS.id, EU.id, "Vence amanhã"),
    Divida(2, "Internet", 35.00, MARINA.id, EU.id, "Vence em 5 dias"),
    Divida(3, "Produtos de limpeza", 22.50, LUCAS.id, EU.id, "Vence em 9 dias"),
    # me devem
    Divida(4, "Compras do mercado", 40.00, EU.id, ANA.id, "Vence amanhã"),
]

TAREFAS: list[Tarefa] = [
    Tarefa(1, "Limpar a cozinha", "Hoje", EU.id),
    Tarefa(2, "Comprar papel higiênico", "Amanhã", MARINA.id),
]

VENCIMENTOS: list[Vencimento] = [
    Vencimento("Energia", "Vence em 12/10", 80.00, "bolt"),
    Vencimento("Internet", "Vence em 15/10", 30.00, "wifi"),
]


def morador_por_id(id_: int) -> Morador:
    return next(m for m in CASA.moradores if m.id == id_)


def dividas_que_eu_devo() -> list[Divida]:
    return [d for d in DIVIDAS if d.devedor_id == EU.id]


def dividas_que_me_devem() -> list[Divida]:
    return [d for d in DIVIDAS if d.credor_id == EU.id]


def total_pendente(dividas: list[Divida]) -> float:
    return sum(d.valor for d in dividas if not d.pago)


def adicionar_conta(descricao: str, valor_total: float, pagador_id: int,
                    partes: dict[int, float], vencimento: str):
    """Cria uma dívida para cada morador (menos o pagador) com a parte dele."""
    prox = max((d.id for d in DIVIDAS), default=0) + 1
    for morador_id, parte in partes.items():
        if morador_id == pagador_id or parte <= 0:
            continue
        DIVIDAS.append(Divida(prox, descricao, round(parte, 2), pagador_id, morador_id, vencimento))
        prox += 1


def marcar_paga(divida_id: int):
    for d in DIVIDAS:
        if d.id == divida_id:
            d.pago = True


def get_divida(divida_id: int) -> Divida | None:
    return next((d for d in DIVIDAS if d.id == divida_id), None)
