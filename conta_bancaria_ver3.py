from abc import ABC, abstractmethod
from datetime import datetime
import os
import textwrap
import time

''' CLASSES '''
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print('\tValor de saque inválido')
            return False
        if self._saldo < valor:
            print('\tSaldo insuficiente')
            return False
        self._saldo -= valor
        return True

    def depositar(self, valor):
        if valor <= 0:
            print('\tValor de depósito inválido')
            return False
        self._saldo += valor
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if isinstance(transacao, Saque)]
        )
        if valor > self.limite:
            print('Valor excede o limite de saque')
            return False
        if numero_saques >= self.limite_saques:
            print('Limite de saques diários excedido')
            return False
        return super().sacar(valor)

    def __str__(self):
        return f"""
        Agência: 	{self.agencia}
        C/C: 		{self.numero}
        Titular: 	{self.cliente.nome}
        """

class Historico:
    '''Classe Histórico'''
    def __init__(self):
        '''Construtor da classe Histórico'''
        self._transacoes = []

    @property
    def transacoes(self):
        '''Método para retornar transações'''
        return self._transacoes

    def adicionar_transacoes(self, transacao):
        '''Método para adicionar transações'''
        if transacao not in self._transacoes:
            self._transacoes.append(
                {
                    "tipo": transacao.__class__.__name__,
                    "valor": transacao.valor,
                    "data": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                }
            )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacoes(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacoes(self)

''' MÉTODOS AUXILIARES '''
def filtrar_cliente(cpf, clientes):
    return next((cliente for cliente in clientes if cliente.cpf == cpf), None)

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('Cliente não possui conta')
        return None
    if len(cliente.contas) == 1:
        return cliente.contas[0]
    for conta in cliente.contas:
        print(f'{conta.numero} : {conta.__class__.__name__}')
    numero_conta = int(input('Informe o número da conta: '))
    return next((conta for conta in cliente.contas if conta.numero == numero_conta), None)

''' FUNÇÕES DE CONTA '''
def movimentar_conta(clientes, tipo_transacao):
    cpf = input('\tInforme o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print('\tCliente não encontrado')
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    if tipo_transacao == 'd':
        valor = float(input('\tInforme o valor do depósito: '))
        transacao = Deposito(valor)
    elif tipo_transacao == 's':
        valor = float(input('\tInforme o valor do saque: '))
        transacao = Saque(valor)
    else:
        print('\tOperação inválida')
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input('\n\tInforme o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print('\n\tCliente não encontrado')
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print('\t' + ('=' * 38))
    print('''
              Extrato
        =============================
            Tipo            Valor 
        ------------   --------------''')

    transacoes = conta.historico.transacoes
    if not transacoes:
        print('\tNão foram realizadas movimentações')
    else:
        for transacao in transacoes:
            tabs = "\t" if transacao["tipo"] == "Deposito" else "\t\t"
            print(f'\t{transacao["tipo"]}{tabs}R$ {transacao["valor"]:>9,.2f}')
    print('\t'+ ('=') * 30)
    print(f'\tSaldo:\t\tR$ {conta.saldo:>9,.2f}')

def criar_cliente(clientes):
    cpf = input('Informe o CPF do cliente: ')
    if filtrar_cliente(cpf, clientes):
        print('Cliente já cadastrado')
        return

    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereço: ')
    clientes.append(PessoaFisica(nome, data_nascimento, cpf, endereco))
    print('Cliente cadastrado com sucesso')

def criar_conta(numero_conta, clientes, contas):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print('Cliente não encontrado')
        return

    conta = ContaCorrente(numero_conta, cliente)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print('Conta cadastrada com sucesso')

def listar_contas(contas):
    for conta in contas:
        print('=' * 38)
        print(textwrap.dedent(str(conta)))

''' FUNÇÕES DE INICIALIZAÇÃO '''
def menu():
    MENU = '''
        =========== MENU =============
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [nu] Cadastrar novo usuário
        [nc] Cadastrar nova conta
        [lc] Listar contas
        [q] Sair
        => '''
    return input(MENU)

def main():
    clientes = []
    contas = []
    while True:
        opcao = menu()
        if opcao == 'd':
            movimentar_conta(clientes, opcao)
        elif opcao == 's':
            movimentar_conta(clientes, opcao)

        elif opcao == 'e':
            exibir_extrato(clientes)

        elif opcao == 'nu':
            criar_cliente(clientes)

        elif opcao == 'nc':
           numero_conta = len(contas) + 1
           criar_conta(numero_conta, clientes, contas)

        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'q':
            print(('\t' + '=' * 38) + '\n')
            print('\tObrigado por utilizar nossos serviços!\n')
            print(('\t' + '=' * 38) + '\n')
            time.sleep(5)
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        else: print('\tOpção inválida')

        wait = input('\n\tPressione <ENTER> para continuar...\n')

        os.system('cls' if os.name == 'nt' else 'clear')

''' INICIALIZAÇÃO '''
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
