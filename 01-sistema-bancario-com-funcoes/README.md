# Otimizando o Sistema Bancário com Funções Python

05/11/2026

## Visão geral

Este projeto implementa a segunda versão de um sistema bancário executado pelo terminal. A solução refatora as operações bancárias em funções e acrescenta o gerenciamento de clientes e contas-correntes.

Os dados são mantidos em memória durante a execução, utilizando listas e dicionários, sem dependências externas.

## Funcionalidades implementadas

- realização de depósitos;
- realização de saques;
- consulta de extrato e saldo;
- validação e normalização de CPF;
- cadastro de clientes;
- validação da data de nascimento;
- validação da estrutura do endereço;
- criação de contas para clientes existentes;
- geração sequencial do número das contas;
- listagem das contas cadastradas;
- prevenção de clientes duplicados pelo CPF.

## Operações bancárias

### Depósito

A função `depositar` recebe `saldo`, `valor` e `extrato` exclusivamente como argumentos posicionais (*positional-only*).

```python
def depositar(saldo: float, valor: float, extrato: str, /):
    ...
```

O depósito é registrado somente quando o valor informado é maior que zero. A função retorna o saldo e o extrato atualizados.

### Saque

A função `sacar` recebe todos os argumentos exclusivamente por nome (*keyword-only*).

```python
def sacar(
    *,
    saldo: float,
    valor: float,
    extrato: str,
    limite: float,
    numero_saques: int,
    limite_saques: int,
):
    ...
```

Antes de concluir a operação, são verificados:

- o saldo disponível;
- o limite de R$ 500,00 por saque;
- o limite de três saques;
- a validade do valor informado.

O contador de saques é incrementado somente quando o saldo é alterado, indicando que a operação foi concluída.

### Extrato

A função `exibir_extrato` recebe o saldo por posição e o extrato por nome.

```python
def exibir_extrato(saldo: float, /, *, extrato: str):
    ...
```

Ela apresenta as movimentações registradas e o saldo atual. Quando não existem movimentações, uma mensagem informativa é exibida.

## Gerenciamento de clientes

### Normalização e validação do CPF

A função `normalizar_cpf` remove pontos, hífen e espaços. Em seguida, `validar_cpf` verifica:

- se o CPF possui 11 dígitos;
- se os números não são todos iguais;
- se os dois dígitos verificadores são válidos.

### Validação da data de nascimento

A função `validar_data_nascimento` espera uma data no formato `dd-mm-aaaa` e valida os intervalos básicos de dia, mês e ano.

### Validação do endereço

A função `validar_endereco` espera o formato:

```text
logradouro, número - bairro - cidade/sigla do estado
```

A estrutura deve possuir três partes não vazias, separadas por hífen.

### Cadastro

A função `criar_cliente` solicita e valida os dados antes de adicionar o cliente à lista. Cada registro possui:

```python
{
    "nome": "Nome do cliente",
    "data_nascimento": "dd-mm-aaaa",
    "cpf": "00000000000",
    "endereco": "logradouro, número - bairro - cidade/UF",
}
```

Um CPF inválido ou já cadastrado impede a criação do cliente.

## Gerenciamento de contas

A função `criar_conta` procura o cliente pelo CPF antes de cadastrar uma nova conta. Não é possível criar uma conta para um cliente inexistente.

Cada conta contém:

```python
{
    "agencia": "0001",
    "numero_conta": "1",
    "cliente": {...},
}
```

Regras implementadas:

- a agência possui o código fixo `0001`;
- o número da conta é sequencial e começa em `1`;
- uma conta pertence a um único cliente;
- um cliente pode possuir mais de uma conta.

A função `listar_contas` apresenta agência, número da conta, titular e CPF das contas cadastradas.

## Menu da aplicação

| Opção | Operação |
|---|---|
| `d` | Depositar |
| `s` | Sacar |
| `e` | Exibir extrato |
| `nu` | Cadastrar novo usuário |
| `nc` | Criar nova conta |
| `lc` | Listar contas cadastradas |
| `q` | Encerrar a aplicação |

## Estrutura do projeto

```text
01-sistema-bancario-com-funcoes/
├── README.md
└── src/
    └── main.py
```

O arquivo `main.py` concentra o estado da aplicação, as funções de negócio e o laço responsável pelo menu interativo.

## Fluxo da aplicação

```text
Início
  └── Exibição do menu
        ├── Operação bancária
        ├── Cadastro de cliente
        ├── Cadastro de conta
        ├── Listagem de contas
        └── Encerramento
```

As listas `clientes` e `contas`, além do saldo e do extrato, existem apenas enquanto o programa está em execução.

## Como executar

### Pré-requisito

- Python 3.10 ou superior, devido ao uso de anotações de tipo com o operador `|`.

Na raiz deste desafio, execute:

```bash
python src/main.py
```

## Tecnologias e conceitos

- Python 3;
- funções;
- argumentos *positional-only* e *keyword-only*;
- listas e dicionários;
- anotações de tipos;
- validação de dados;
- modularização de responsabilidades por funções.
