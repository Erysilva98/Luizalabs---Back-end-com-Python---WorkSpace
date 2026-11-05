# Otimizando o Sistema Bancário com Funções Python

## Visão geral

Este projeto propõe a evolução de um sistema bancário procedural. A aplicação deve ser refatorada para separar suas responsabilidades em funções reutilizáveis e receber recursos para cadastro de clientes e contas-correntes.

A modularização busca tornar o código mais legível, manutenível e preparado para futuras evoluções.

## Objetivo

Refatorar as operações de depósito, saque e exibição de extrato em funções específicas e implementar duas novas operações:

- cadastro de cliente;
- cadastro de conta-corrente vinculada a um cliente.

## Requisitos funcionais

### Depósito

A função de depósito deve:

- receber `saldo`, `valor` e `extrato` exclusivamente como argumentos posicionais (*positional-only*);
- aceitar apenas valores positivos;
- registrar no extrato os depósitos válidos;
- retornar o saldo e o extrato atualizados.

Assinatura esperada:

```python
def depositar(saldo, valor, extrato, /):
    ...
```

### Saque

A função de saque deve:

- receber todos os argumentos exclusivamente por nome (*keyword-only*);
- validar o saldo disponível, o limite por operação e a quantidade diária de saques;
- aceitar apenas valores positivos;
- registrar no extrato os saques válidos;
- retornar o saldo e o extrato atualizados.

Argumentos esperados: `saldo`, `valor`, `extrato`, `limite`, `numero_saques` e `limite_saques`.

Assinatura esperada:

```python
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    ...
```

### Extrato

A função de extrato deve:

- receber `saldo` como argumento posicional;
- receber `extrato` como argumento nomeado;
- exibir todas as movimentações realizadas;
- informar que não houve movimentações quando o histórico estiver vazio;
- exibir o saldo atual.

Assinatura esperada:

```python
def exibir_extrato(saldo, /, *, extrato):
    ...
```

### Cadastro de cliente

O sistema deve armazenar os clientes em uma lista. Cada cliente deve conter:

- nome;
- data de nascimento;
- CPF;
- endereço.

Regras:

- o CPF deve ser armazenado somente com números;
- não é permitido cadastrar dois clientes com o mesmo CPF;
- o endereço deve seguir o formato `logradouro, número - bairro - cidade/sigla do estado`.

### Cadastro de conta-corrente

O sistema deve armazenar as contas em uma lista. Cada conta deve conter:

- agência;
- número da conta;
- cliente vinculado.

Regras:

- a agência é fixa e possui o código `0001`;
- a numeração das contas é sequencial e começa em `1`;
- uma conta pertence a somente um cliente;
- um cliente pode possuir mais de uma conta;
- o cliente deve ser localizado pelo CPF antes da criação da conta.

## Regras das operações bancárias

- O limite por saque é de R$ 500,00.
- São permitidos, no máximo, três saques por dia.
- Depósitos e saques devem possuir valores maiores que zero.
- Todas as movimentações válidas devem ser registradas no extrato.

## Estrutura do projeto

```text
01-sistema-bancario-com-funcoes/
├── README.md
├── src/
│   ├── banco/
│   │   ├── __init__.py
│   │   ├── clientes.py
│   │   ├── configuracoes.py
│   │   ├── contas.py
│   │   ├── interface.py
│   │   ├── operacoes.py
│   │   └── sistema.py
│   └── main.py
└── tests/
    └── test_operacoes.py
```

## Arquitetura

O projeto utiliza uma **arquitetura modular em camadas leves**. Cada módulo possui uma responsabilidade específica:

| Módulo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada da aplicação. |
| `sistema.py` | Controla o fluxo e mantém o estado da aplicação em memória. |
| `operacoes.py` | Implementa depósito, saque e extrato. |
| `clientes.py` | Normaliza CPF, consulta e cadastra clientes. |
| `contas.py` | Cadastra e lista contas-correntes. |
| `interface.py` | Centraliza o menu e a leitura de dados do terminal. |
| `configuracoes.py` | Armazena constantes e regras configuráveis. |

### Padrão de projeto

A classe `SistemaBancario` funciona como uma **Facade (fachada)**: ela oferece um ponto central para coordenar a interface, as operações bancárias e os cadastros. As regras permanecem em funções independentes, conforme solicitado pelo desafio.

O fluxo principal é:

```text
main.py → SistemaBancario → interface e módulos de domínio
```

Essa separação permite alterar o menu sem modificar as regras bancárias e testar cada função isoladamente.

## Execução

### Pré-requisito

- Python 3 instalado e disponível no terminal.

Na raiz deste desafio, execute:

```bash
python src/main.py
```

## Testes

Na raiz deste desafio, execute:

```bash
python -m unittest discover -s tests -v
```

## Decisões técnicas

- Os dados são armazenados em listas durante a execução, conforme definido pelo enunciado.
- Clientes e contas são representados por dicionários para manter a solução compatível com o nível do desafio.
- O CPF é normalizado antes da consulta ou persistência em memória.
- A numeração da conta é calculada de forma sequencial a partir da lista de contas.
- Nenhuma dependência externa é necessária.
