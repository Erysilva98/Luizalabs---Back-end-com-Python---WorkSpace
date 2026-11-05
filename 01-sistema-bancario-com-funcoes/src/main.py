saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
clientes: list[dict[str, str]] = []
contas: list[dict[str, str | dict[str, str]]] = []
AGENCIA = "0001"

def depositar(saldo: float, valor: float, extrato: str, /):
    if valor > 0:
        saldo +=valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato

def sacar(*, saldo: float, valor: float, extrato: str, limite: float, numero_saques: int, limite_saques: int):
    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

def exibir_extrato(saldo: float, /, *, extrato: str):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")
    
def normalizar_cpf(cpf: str) -> str:
    """Remove caracteres não numéricos do CPF."""
    return cpf.replace(".", "").replace("-", "").strip()

def validar_cpf(cpf: str) -> bool:
    """Valida o CPF com base em seu formato e dígitos verificadores."""
    cpf_normalizado = normalizar_cpf(cpf)

    # Verifica se o CPF tem 11 dígitos
    if len(cpf_normalizado) != 11:
        return False

    # Verifica se todos os dígitos são iguais (ex: 111.111.111-11)
    if cpf_normalizado == cpf_normalizado[0] * 11:
        return False

    # Cálculo do primeiro dígito verificador
    soma = sum(int(cpf_normalizado[i]) * (10 - i) for i in range(9))
    primeiro_digito = (soma * 10 % 11) % 10

    # Cálculo do segundo dígito verificador
    soma = sum(int(cpf_normalizado[i]) * (11 - i) for i in range(10))
    segundo_digito = (soma * 10 % 11) % 10

    return (int(cpf_normalizado[9]) == primeiro_digito and
            int(cpf_normalizado[10]) == segundo_digito)
    
def validar_data_nascimento(data_nascimento: str) -> bool:
    """Valida a data de nascimento no formato dd-mm-aaaa."""
    try:
        dia, mes, ano = map(int, data_nascimento.split('-'))
        if not (1 <= dia <= 31 and 1 <= mes <= 12 and ano > 0):
            return False
        return True
    except ValueError:
        return False
    
def validar_endereco(endereco: str) -> bool:
    """Valida o endereço no formato logradouro, nro - bairro - cidade/sigla estado."""
    partes = endereco.split('-')
    if len(partes) != 3:
        return False
    logradouro_nro, bairro, cidade_estado = partes
    if not logradouro_nro.strip() or not bairro.strip() or not cidade_estado.strip():
        return False
    return True

def filtrar_cliente(cpf: str, clientes: list[dict[str, str]]) -> dict[str, str] | None:
    """Filtra um cliente pelo CPF."""
    cpf_normalizado = normalizar_cpf(cpf)
    for cliente in clientes:
        if normalizar_cpf(cliente["cpf"]) == cpf_normalizado:
            return cliente
    return None

def criar_cliente(clientes: list[dict[str, str]]) -> None:
    """Cria um novo cliente e adiciona à lista de clientes."""
    cpf = input("Informe o CPF (somente números): ")
    
    if not validar_cpf(cpf):
        print("CPF inválido. Tente novamente.")
        return
    
    cliente_existente = filtrar_cliente(cpf, clientes)
    if cliente_existente:
        print("Já existe um cliente com esse CPF.")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    if not validar_data_nascimento(data_nascimento):
        print("Data de nascimento inválida. Tente novamente.")
        return

    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    if not validar_endereco(endereco):
        print("Endereço inválido. Tente novamente.")
        return

    cliente = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }
    clientes.append(cliente)
    print("Cliente criado com sucesso!")

def criar_conta(agencia: str, numero_conta: str, clientes: list[dict[str, str]], contas: list[dict[str, str | dict[str, str]]]) -> None:
    """Cria uma nova conta para um cliente existente."""
    cpf = input("Informe o CPF do cliente para criar a conta: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado. Crie o cliente antes de criar a conta.")
        return
    
    conta: dict[str, str | dict[str, str]] = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "cliente": cliente
    }
    contas.append(conta)
    print("Conta criada com sucesso!")

def listar_contas(contas: list[dict[str, str | dict[str, str]]]) -> None:
    """Lista todas as contas cadastradas."""
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    
    for conta in contas:
        cliente = conta["cliente"]
        if not isinstance(cliente, dict):
            continue
        print("\n================ CONTA ================")
        print(f"Agência: {conta['agencia']}")
        print(f"Número da conta: {conta['numero_conta']}")
        print(f"Titular: {cliente['nome']}")
        print(f"CPF: {cliente['cpf']}")
        print("=======================================")
        
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo usuário
[nc] Nova conta
[q] Sair

=> """

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        saldo, extrato = depositar(saldo, valor, extrato)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        
        saldo_anterior = saldo  # Armazena o saldo antes do saque para verificar se houve alteração

        saldo, extrato = sacar(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            limite=limite,
            numero_saques=numero_saques,
            limite_saques=LIMITE_SAQUES,
        )

        # Verifica se o saldo foi alterado após a tentativa de saque
        if saldo != saldo_anterior:
            numero_saques += 1  # Incrementa o número de saques apenas se o saque foi bem-sucedido
            print("Saque realizado com sucesso!")
            
    elif opcao == "e":
        exibir_extrato(saldo, extrato=extrato)
        
    elif opcao == "nu":
        criar_cliente(clientes=clientes)

    elif opcao == "nc":
        numero_conta = str(len(contas) + 1)
        criar_conta(agencia=AGENCIA, numero_conta=numero_conta, clientes=clientes, contas=contas)

    elif opcao == "lc":
        if not contas:
            print("Nenhuma conta cadastrada.")
        else:
            for conta in contas:
                cliente = conta["cliente"]
                if not isinstance(cliente, dict):
                    continue
                print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, Cliente: {cliente['nome']}, CPF: {cliente['cpf']}")
    
    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")