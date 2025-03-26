"""    Projeto: Conta Bancária
    Objetivo: Implementar um sistema de conta bancária com as seguintes funcionalidades:
        - Depositar
        - Sacar
        - Extrato
        - Cadastrar novo usuário
        - Cadastrar nova conta
        - Listar contas
        - Sair
    Restrições:
        - O sistema deve permitir a realização de depósitos e saques em uma conta corrente,
            limitadas a 10 transações por dia;
        - O sistema deve permitir a visualização do extrato da conta corrente,
            contendo DATA, HORA, TIPO e VALOR da transação;
        - O sistema deve permitir a Cadastro de novos clientes;
        - O sistema deve permitir a criação de novas contas correntes;
        - O sistema deve permitir a listagem de todas as contas correntes cadastradas;
    Observações:
        - 
"""
from abc import ABC, abstractmethod
from datetime import datetime
import os
import textwrap
import time

class Cliente:
    '''Classe Cliente '''
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        ''' Método para realizar transações '''
        transacoes = conta.historico.transacoes_do_dia(datetime.today())
        if len(transacoes) >= 10:
            print("\n@@@@@@@ Você excedeu o número de transações permitidas para hoje! @@@@@@@")
        else:
            transacao.registrar(conta)

    def adicionar_conta(self, conta):
        ''' Método para adicionar contas ao cliente '''
        self.contas.append(conta)

class PessoaFisica(Cliente):
    ''' Classe Pessoa Física '''
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    ''' Classe Conta '''
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        ''' Método para criar nova conta '''
        return cls(numero, cliente)

    @property
    def saldo(self):
        ''' Método para retornar saldo '''
        return self._saldo

    @property
    def numero(self):
        ''' Método para retornar número da conta '''
        return self._numero

    @property
    def agencia(self):
        ''' Método para retornar agência '''
        return self._agencia

    @property
    def cliente(self):
        ''' Método para retornar cliente '''
        return self._cliente

    @property
    def historico(self):
        ''' Método para retornar histórico '''
        return self._historico

    def sacar(self, valor):
        ''' Método para realizar saque '''
        if valor <= 0:
            print('\tValor de saque inválido')
            return False
        if self._saldo < valor:
            print('\tSaldo insuficiente')
            return False
        self._saldo -= valor
        return True

    def depositar(self, valor):
        ''' Método para realizar depósito '''
        if valor <= 0:
            print('\tValor de depósito inválido')
            return False
        self._saldo += valor
        return True

class ContaCorrente(Conta):
    ''' Classe Conta Corrente '''
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        ''' Método para realizar saque '''
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
        ''' Método para retornar representação em string '''
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
    def transacoes_do_dia(self, day):
        ''' Método para retornar transações do dia '''
        lista = []
        date_format = '%d/%m/%Y %H:%M:%S'
        for transacao in self._transacoes:
            dia_transacao = datetime.strptime(transacao["data"], date_format)
            if dia_transacao.date() == day.date():
                lista.append(transacao)
        return lista

class Transacao(ABC):
    ''' Classe Abstrata Transações '''
    @property
    @abstractmethod
    def valor(self):
        ''' Método para retornar valor '''

    @abstractmethod
    def registrar(self, conta):
        ''' Método para registrar transações '''

class Saque(Transacao):
    ''' Classe Saque '''
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        ''' Método para retornar valor '''
        return self._valor

    def registrar(self, conta):
        ''' Método para registrar transações '''
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacoes(self)

class Deposito(Transacao):
    ''' Classe Depósito '''
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        ''' Método para retornar valor '''
        return self._valor

    def registrar(self, conta):
        ''' Método para registrar transações '''
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacoes(self)

def log_transacao(func):
    ''' Decorator para log de transações '''
    def envelope(*args, **kwargs):
        ''' Método envelope '''
        resultado = func(*args, **kwargs)
        print(f'\t[{datetime.now()}] {func.__name__.upper()}')
        return resultado
    return envelope

def filtrar_cliente(cpf, clientes):
    ''' Método para filtrar cliente '''
    return next((cliente for cliente in clientes if cliente.cpf == cpf), None)

def recuperar_conta_cliente(cliente):
    ''' Método para recuperar conta do cliente '''
    if not cliente.contas:
        print('Cliente não possui conta')
        return None
    if len(cliente.contas) == 1:
        return cliente.contas[0]
    for conta in cliente.contas:
        print(f'{conta.numero} : {conta.__class__.__name__}')
    numero_conta = int(input('Informe o número da conta: '))
    return next((conta for conta in cliente.contas if conta.numero == numero_conta), None)

def movimentar_conta(clientes, tipo_transacao):
    ''' Método para movimentar conta '''
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

@log_transacao
def exibir_extrato(clientes):
    ''' Método para exibir extrato '''
    cpf = input('\n\tInforme o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print('\n\tCliente não encontrado')
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    transacoes = conta.historico.transacoes

    print('\t' + ('=' * 56))
    print('''                            Extrato Bancário
        ===========|=========|================|================|
            Data      Hora          Tipo            Valor 
        ----------- --------- ---------------- ---------------- ''')

    if not transacoes:
        print('\tNão foram realizadas movimentações')
    else:
        for transacao in transacoes:
            tabs = "\t" if transacao["tipo"] == "Deposito" else "\t\t"
            print(f'\t {transacao['data']}\t{transacao["tipo"]}{tabs}R${transacao["valor"]:>12,.2f}')
    print('\t'+ ('=') * 56)
    print(f'\tSaldo:{('\t')*5}R$ {conta.saldo:>12,.2f}')

@log_transacao
def criar_cliente(clientes):
    ''' Método para criar cliente '''
    cpf = input('Informe o CPF do cliente: ')
    if filtrar_cliente(cpf, clientes):
        print('Cliente já cadastrado')
        return

    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereço: ')
    clientes.append(PessoaFisica(nome, data_nascimento, cpf, endereco))
    print('Cliente cadastrado com sucesso')

@log_transacao
def criar_conta(numero_conta, clientes, contas):
    ''' Método para criar conta '''
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
    ''' Método para listar contas '''
    for conta in contas:
        print('=' * 38)
        print(textwrap.dedent(str(conta)))

def menu():
    ''' Método para exibir menu '''
    funcoes = '''
        =========== MENU =============
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [nu] Cadastrar novo usuário
        [nc] Cadastrar nova conta
        [lc] Listar contas
        [q] Sair
        => '''
    return input(funcoes)

def main():
    ''' Método principal '''
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

        input('\n\tPressione <ENTER> para continuar...\n')

        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
