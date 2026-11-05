import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from banco.clientes import cadastrar_cliente  # noqa: E402
from banco.contas import cadastrar_conta  # noqa: E402
from banco.operacoes import depositar, sacar  # noqa: E402


class OperacoesTestCase(unittest.TestCase):
    def test_deposito_atualiza_saldo_e_extrato(self):
        saldo, extrato = depositar(0, 100, "")
        self.assertEqual(100, saldo)
        self.assertIn("Depósito: R$ 100.00", extrato)

    def test_saque_respeita_saldo(self):
        saldo, extrato = sacar(
            saldo=50,
            valor=100,
            extrato="",
            limite=500,
            numero_saques=0,
            limite_saques=3,
        )
        self.assertEqual(50, saldo)
        self.assertEqual("", extrato)

    def test_cliente_duplicado_nao_e_cadastrado(self):
        clientes = []
        dados = {
            "clientes": clientes,
            "nome": "Maria",
            "data_nascimento": "01/01/1990",
            "cpf": "123.456.789-00",
            "endereco": "Rua A, 10 - Centro - São Paulo/SP",
        }
        self.assertTrue(cadastrar_cliente(**dados))
        self.assertFalse(cadastrar_cliente(**dados))
        self.assertEqual(1, len(clientes))

    def test_conta_e_vinculada_ao_cliente(self):
        clientes = []
        contas = []
        cadastrar_cliente(
            clientes=clientes,
            nome="Maria",
            data_nascimento="01/01/1990",
            cpf="12345678900",
            endereco="Rua A, 10 - Centro - São Paulo/SP",
        )
        criada = cadastrar_conta(
            agencia="0001",
            numero_conta=1,
            cpf="12345678900",
            clientes=clientes,
            contas=contas,
        )
        self.assertTrue(criada)
        self.assertIs(contas[0]["cliente"], clientes[0])


if __name__ == "__main__":
    unittest.main()
