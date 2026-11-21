"""Data models. When the database is connected, these fields become the table columns."""

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class Morador:
    id: int
    nome: str
    cor: str

    @property
    def inicial(self) -> str:
        return self.nome[:1].upper()


@dataclass
class Divida:
    """A balance between two residents: `debtor` owes `amount` to `creditor`."""
    id: int
    descricao: str
    valor: float
    credor_id: int
    devedor_id: int
    vencimento: str = ""
    pago: bool = False


@dataclass
class Tarefa:
    id: int
    titulo: str
    detalhe: str
    responsavel_id: int
    feita: bool = False


@dataclass
class Vencimento:
    titulo: str
    detalhe: str
    valor: float
    icone: str = "bolt"


@dataclass
class Casa:
    nome: str
    codigo: str = ""  # código de convite (4 caracteres)
    moradores: list[Morador] = field(default_factory=list)

@dataclass
class Votacao:
    """A proposal the house votes on. `votos` maps resident id -> True (agrees) / False (disagrees)."""
    id: int
    titulo: str
    valor: float
    criador_id: int
    encerra_em: date
    votos: dict[int, bool] = field(default_factory=dict)
    status: str = "aberta" 


@dataclass
class Reserva:
    recurso: str
    dia: date
    hora: int 
    morador_id: int


@dataclass
class Combinado:
    texto: str
    responsavel_id: int
    prazo: str 
    feito: bool = False


@dataclass
class Reuniao:
    data: datetime
    local: str = "no salão"
    confirmados: set[int] = field(default_factory=set)
    confirmada: bool = False
    tema: str = ""
    anotacoes: str = ""
    combinados: list[Combinado] = field(default_factory=list)

@dataclass
class ItemCompra:
    id: int
    nome: str
    quantidade: str
    adicionado_por_id: int
    comprado: bool = False