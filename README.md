# 🏠 WeHouse — Organização para Casas Compartilhadas

O **WeHouse** é um aplicativo desenvolvido em Python e Flet que ajuda quem divide moradia a organizar a rotina da casa em um só lugar: contas, tarefas, compras, votações, reservas e reuniões. O objetivo foi substituir o grupo de WhatsApp onde tudo se perde ("quem pagou o mercado?", "de quem é a vez de tirar o lixo?") por algo simples de usar e que deixe todo mundo na mesma página.

O layout foi desenhado antes no Figma e depois implementado tela por tela.

---

## 🚀 Funcionalidades

O app é dividido em áreas, todas ligadas à mesma casa e aos mesmos moradores:

* **Contas:** cadastra uma despesa e divide entre os moradores, de forma igual ou com valores personalizados. Mostra quanto você deve e quanto te devem, em duas abas separadas.
* **Pagamento com Pix:** ao pagar uma conta, o app gera o código "copia e cola" e o QR Code do Pix. Depois de pagar, quem devia avisa no app, e a conta fica como *Aguardando*. Ela só é quitada quando quem recebe confirma o recebimento (ou diz que não recebeu, e a conta volta a ficar pendente).
* **Tarefas:** lista do que precisa ser feito na casa, com responsável e horário. Ao marcar, a tarefa vai para a aba de concluídas.
* **Lista de compras:** compartilhada entre todos os moradores. Ao digitar algo como "Arroz 2kg", o app separa o nome da quantidade. Os itens marcados vão para uma seção de comprados, que pode ser aberta e fechada.
* **Votação:** propostas da casa, como comprar uma geladeira. Cada morador vota "concordo" ou "não concordo". Quando todos votam e a maioria concorda, a proposta é aprovada e a dívida de cada um é criada automaticamente em Contas.
* **Reservas:** grade semanal para reservar a máquina de lavar, a sala de visitas ou a churrasqueira, em horários de 2 horas. O app não deixa reservar um horário que já está ocupado.
* **Reunião mensal:** mostra a próxima reunião, quem já confirmou presença, permite sugerir outra data, definir um tema e registrar a ata com os combinados. As atas anteriores ficam guardadas no histórico.
* **Notificações:** um painel aberto pelo sino da tela inicial, que mostra o que está pendente para você (contas a pagar, votos que faltam, tarefas do dia, reunião para confirmar, pagamentos para confirmar). As notificações não são uma lista fixa: quando você resolve a pendência, ela some sozinha.
* **Convite:** cada casa tem um código de 4 caracteres que pode ser copiado e enviado aos colegas para que eles entrem.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Interface:** Flet
- **QR Code do Pix:** segno
- **Variáveis de ambiente:** python-dotenv
- **Design:** Figma

---

## 🗂️ Estrutura do Projeto

| Pasta                | O que tem dentro                                                           |
|----------------------|----------------------------------------------------------------------------|
| `src/main.py`        | Rotas do app e configuração da janela                                      |
| `src/theme.py`       | Cores usadas em todas as telas                                             |
| `src/components/`    | Peças reutilizáveis: botões, cards, menu "Mais" e painel de notificações   |
| `src/models/`        | As estruturas de dados: morador, dívida, tarefa, votação, reserva etc.     |
| `src/services/`      | Dados de exemplo e geração do código Pix                                   |
| `src/views/`         | Uma tela por arquivo                                                       |

---

## 🖱️ Interface e Usabilidade

* **Barra inferior** com Início, Contas, Tarefas e Mais.
* **Menu flutuante no "Mais":** ao tocar, o fundo escurece e aparecem os atalhos para Lista de Compras, Reservar, Votações e Reuniões. Tocar no "Mais" de novo, ou no fundo escuro, fecha o menu.
* **Selo no sino:** mostra quantas notificações ainda não foram lidas.
* **Atalhos na tela inicial:** nova conta, votação e reservas a um toque.

---

## 📦 Como Instalar e Rodar o Projeto

Siga os passos abaixo para rodar o WeHouse na sua máquina:

### 1. Clonar o repositório
```
git clone https://github.com/lais-ls/we-house.git
cd we-house
```

### 2. Criar o ambiente virtual
Certifique-se de ter o Python 3.10 ou mais novo instalado. No Windows:
```
python -m venv .venv
.venv\Scripts\activate
```

No Linux ou Mac:
```
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências
```
pip install -r requirements.txt
```

### 4. Executar a aplicação
```
flet run src/main.py
```

A janela abre no tamanho de um celular (390 x 700). Para entrar no app, qualquer e-mail com `@` e qualquer senha funcionam, porque o login ainda é de teste.

---

## 🧪 Dados de Exemplo

O WeHouse **ainda não usa banco de dados**. Tudo o que aparece nas telas vem do arquivo `src/services/dados_fake.py`, com uma casa de exemplo ("República Bela Vista") e quatro moradores. As ações funcionam de verdade enquanto o app está aberto: votar, reservar, marcar tarefa, confirmar pagamento. Mas tudo volta ao começo quando o app é fechado.

Os pontos onde o banco de dados entraria estão marcados com `TODO` no código, o que deixa o projeto preparado para conectar um banco depois.

---

## ⚠️ Limitações Conhecidas

**Sem banco de dados:** como os dados ficam só na memória, nada é salvo entre uma execução e outra.

**Login de teste:** a tela de login não confere e-mail e senha de verdade, e o app sempre age como a moradora "Bia", sem contas separadas para cada pessoa.

**Pix de exemplo:** o código Pix usa chaves fictícias, então serve para demonstrar o fluxo, mas não gera um pagamento real.

**Notificações só dentro do app:** não há aviso no celular quando o app está fechado.