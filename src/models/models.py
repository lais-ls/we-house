"""Data models. When the database is connected, these fields become the table columns."""

from dataclasses import dataclass, field


@dataclass
class Morador:
    id: int
    nome: str
    cor: str  # cor do avatar (hex)

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
    moradores: list[Morador] = field(default_factory=list)
