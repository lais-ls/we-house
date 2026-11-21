"""Sample data for the MVP. Replace these functions with database queries later."""

from datetime import date, datetime, timedelta

from models.models import (
    Casa, Combinado, Divida, Morador, Reserva, Reuniao, Tarefa, Vencimento, Votacao,
)

EU = Morador(1, "Bia", "#F7C2B2")
LUCAS = Morador(2, "Lucas", "#C8C2EE")
ANA = Morador(3, "Ana", "#B8D3C2")
MARINA = Morador(4, "Marina", "#E2D08E")

CASA = Casa("República Bela Vista", "BV42", [EU, LUCAS, ANA, MARINA])  # TODO: gerar o código no banco

DIVIDAS: list[Divida] = [
    # eu devo
    Divida(1, "Compras do mercado", 50.00, LUCAS.id, EU.id, "Vence amanhã"),
    Divida(2, "Internet", 35.00, MARINA.id, EU.id, "Vence em 5 dias"),
    Divida(3, "Produtos de limpeza", 22.50, LUCAS.id, EU.id, "Vence em 9 dias"),
    # me devem
    Divida(4, "Compras do mercado", 40.00, EU.id, ANA.id, "Vence amanhã"),
]

TAREFAS: list[Tarefa] = [
    Tarefa(1, "Tirar o lixo", "Hoje · 18h", LUCAS.id),
    Tarefa(2, "Limpar a cozinha", "Hoje · 19h", EU.id),
    Tarefa(3, "Lavar louça", "Hoje · 20h", ANA.id),
    Tarefa(4, "Limpar banheiro", "Amanhã · 10h", MARINA.id),
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

VOTACOES: list[Votacao] = [
    Votacao(1, "Comprar geladeira nova", 2400.00, LUCAS.id, date.today() + timedelta(days=3),
            {LUCAS.id: True, ANA.id: True, MARINA.id: True}),
    Votacao(2, "Trocar o chuveiro do banheiro", 180.00, ANA.id, date.today() - timedelta(days=6),
            {EU.id: True, LUCAS.id: True, ANA.id: True, MARINA.id: False}, "aprovada"),
]


def votacoes(status_aberta: bool) -> list[Votacao]:
    return [v for v in VOTACOES if (v.status == "aberta") == status_aberta]


def dias_restantes(v: Votacao) -> int:
    return max((v.encerra_em - date.today()).days, 0)


def _fechar_se_completa(v: Votacao):
    """Fecha quando todos votaram. Aprovada = mais "concordo" que "não concordo"; gera a dívida."""
    if len(v.votos) < len(CASA.moradores):
        return
    concordam = sum(1 for x in v.votos.values() if x)
    v.status = "aprovada" if concordam > len(v.votos) - concordam else "rejeitada"
    if v.status == "aprovada" and v.valor > 0:
        parte = v.valor / len(CASA.moradores)
        adicionar_conta(v.titulo, v.valor, v.criador_id,
                        {m.id: parte for m in CASA.moradores}, v.encerra_em.strftime("%d/%m/%Y"))


def votar(votacao_id: int, morador_id: int, concorda: bool):
    v = next((x for x in VOTACOES if x.id == votacao_id), None)
    if v and v.status == "aberta":
        v.votos[morador_id] = concorda
        _fechar_se_completa(v)


def adicionar_votacao(titulo: str, valor: float, dias: int):
    prox = max((v.id for v in VOTACOES), default=0) + 1
    VOTACOES.append(Votacao(prox, titulo, valor, EU.id, date.today() + timedelta(days=dias),
                            {EU.id: True}))  # quem propõe já concorda


RECURSOS = ["Máquina de lavar", "Sala de visitas", "Churrasqueira"]
HORARIOS = [8, 10, 12, 14, 16, 18, 20]


def segunda_da_semana(d: date) -> date:
    return d - timedelta(days=d.weekday())


def _semear_reservas() -> list[Reserva]:
    padrao = {
        "Máquina de lavar": [(2, 8, ANA), (5, 8, LUCAS), (0, 10, ANA), (3, 10, LUCAS), (6, 10, EU),
                             (1, 12, MARINA), (5, 12, ANA), (4, 14, ANA), (0, 16, LUCAS), (3, 16, MARINA),
                             (5, 16, MARINA), (1, 18, LUCAS), (6, 18, LUCAS), (4, 20, MARINA)],
        "Sala de visitas": [(4, 18, LUCAS), (5, 20, ANA), (2, 16, MARINA)],
        "Churrasqueira": [(5, 12, LUCAS), (6, 12, ANA)],
    }
    base = segunda_da_semana(date.today())
    reservas = []
    for semana in range(-1, 5):
        for recurso, itens in padrao.items():
            for dia_sem, hora, m in itens:
                reservas.append(Reserva(recurso, base + timedelta(weeks=semana, days=dia_sem), hora, m.id))
    return reservas


RESERVAS: list[Reserva] = _semear_reservas()


def reserva_em(recurso: str, dia: date, hora: int) -> Reserva | None:
    return next((r for r in RESERVAS if r.recurso == recurso and r.dia == dia and r.hora == hora), None)


def reservar(recurso: str, dia: date, hora: int, morador_id: int) -> bool:
    if reserva_em(recurso, dia, hora):
        return False
    RESERVAS.append(Reserva(recurso, dia, hora, morador_id))
    return True


def cancelar_reserva(recurso: str, dia: date, hora: int, morador_id: int):
    r = reserva_em(recurso, dia, hora)
    if r and r.morador_id == morador_id:
        RESERVAS.remove(r)


def _proximo_sabado() -> datetime:
    d = date.today() + timedelta(days=7)
    d += timedelta(days=(5 - d.weekday()) % 7)
    return datetime(d.year, d.month, d.day, 19, 0)


REUNIAO = Reuniao(
    data=_proximo_sabado(),
    confirmados={LUCAS.id, ANA.id},
    combinados=[
        Combinado("Revezar a limpeza do banheiro toda semana", LUCAS.id, "Toda sem."),
        Combinado("Pagar a internet até o dia 15", EU.id, "Dia 15"),
        Combinado("Avisar com antecedência quando receber visitas", MARINA.id, "Sempre"),
    ],
)

HISTORICO_REUNIOES: list[tuple[datetime, str, str, list[Combinado]]] = [
    (datetime.now().replace(hour=19, minute=0) - timedelta(days=30), "Divisão da limpeza",
     "Ficou decidido revezar a limpeza das áreas comuns.",
     [Combinado("Escala de limpeza semanal", ANA.id, "Toda sem.", True)]),
]


def confirmar_presenca(morador_id: int):
    REUNIAO.confirmados.add(morador_id)
    REUNIAO.confirmada = len(REUNIAO.confirmados) >= len(CASA.moradores)


def propor_nova_data(nova: datetime, morador_id: int):
    REUNIAO.data = nova
    REUNIAO.confirmados = {morador_id} 
    REUNIAO.confirmada = False


def salvar_ata(anotacoes: str):
    """Guarda a ata no histórico e agenda a próxima reunião para 1 mês depois."""
    HISTORICO_REUNIOES.insert(0, (REUNIAO.data, REUNIAO.tema or "Reunião mensal", anotacoes,
                                  list(REUNIAO.combinados)))
    REUNIAO.anotacoes = ""
    REUNIAO.tema = ""
    REUNIAO.combinados = []
    REUNIAO.confirmados = set()
    REUNIAO.confirmada = False
    REUNIAO.data = REUNIAO.data + timedelta(days=28)


def tarefas(feitas: bool) -> list[Tarefa]:
    return [t for t in TAREFAS if t.feita == feitas]


def alternar_tarefa(tarefa_id: int, feita: bool):
    for t in TAREFAS:
        if t.id == tarefa_id:
            t.feita = feita


def adicionar_tarefa(titulo: str, responsavel_id: int, quando: str):
    prox = max((t.id for t in TAREFAS), default=0) + 1
    TAREFAS.append(Tarefa(prox, titulo, quando, responsavel_id))
