'''
Criado por: Paulo Ivar Peruzzo Filho
Desafio 2: Conta Bancária(funções)
Curso: Formação Python Developer
Instituição: Digital Innovation One
'''
import os

def depositar(saldo_deposito, valor_deposito, /):
    '''Deposita um valor na conta'''
    if valor_deposito <= 0:
        valor_deposito = float(input('Valor depósito deve ser positivo: '))
    saldo_deposito += valor_deposito
    extrato.append(valor_deposito)
    return saldo_deposito

def sacar(*, saldo_sacar, valor_sacar):
    '''Saca um valor da conta'''
    if saldo_sacar < valor_sacar:
        print(f'Valor de saque superior ao saldo(R$ {saldo_sacar:.2f})')
    else:
        if valor_sacar <= 0:
            valor_sacar = float(input('Valor saque deve ser positivo: '))
        saldo_sacar -= valor_sacar
        extrato.append(-valor_sacar)
    return saldo_sacar

def apresenta_extrato(saldo_extrato,/,*, extrato_apresentar):
    '''Apresenta o extrato da conta'''
    print('''
          Extrato
=============================
  Tipo            Valor 
------------   --------------
                  ''')
    for valor_movimentado in extrato_apresentar:
        if valor_movimentado > 0:
            print(f'depósito \tR$ {valor_movimentado:>9,.2f}')
        else: print(f'saque \t\tR$ {valor_movimentado:>9,.2f}')
    print(f'saldo \t\tR$ {saldo_extrato:>9,.2f}')

def cadastrar_usuario(cpf_cadastro, usuarios):
    '''Cadastra um novo usuário'''
    nome = input('Nome: ')
    data_nascimento = input('Data de nascimento (dd-mm-aaaa): ')
    print('Endereço: ')
    rua = input('Rua: ')
    numero = input('Número: ')
    endereco = rua + ', ' + numero
    bairro = input('Bairro: ')
    cidade = input('Cidade: ')
    estado = input('UF: ')

    usuarios.append({"cpf":cpf_cadastro,
                     "nome":nome,
                     "dataNascimento":data_nascimento,
                     "endereco":endereco,
                     "bairro":bairro,
                     "cidade":cidade,
                     "estado":estado
                     })
    print('Usuário cadastrado!')

def buscar_usuario(cpf_busca, usuarios):
    '''Busca um usuário pelo CPF'''
    for usuario_busca in usuarios:
        if usuario_busca["cpf"] == cpf_busca:
            return usuario_busca

def cadastrar_conta(usuario_cadastrar, contas):
    '''Cadastra uma nova conta'''
    prox_conta = len(contas)+1
    contas.append({"agencia":AGENCIA,
                   "conta":prox_conta,
                   "usuario":usuario_cadastrar,
                   })
    print('Conta cadastrada com sucesso!')

def listar_contas(contas):
    '''Lista as contas cadastradas'''
    for conta in contas:
        linha = f'''\
Agência:\t{conta['agencia']}
  Conta:\t{conta['conta']}
Titular:\t{conta['usuario']['nome']}
    CPF:\t{conta['usuario']['cpf']}'''
        print(50 * '=')
        print(linha)


MENU = '''
=========== MENU =============
Cód\tOpção
---\t----------------------
[d]\tDepositar
[s]\tSacar
[e]\tExtrato
[nu]\tCadastrar novo usuário
[nc]\tCadastrar nova conta
[lc]\tListar contas

[q]\tSair

=> '''

saldo = 0
LIMITE = 500
numero_saques = 0
LIMITE_SAQUES = 3
AGENCIA = '0001'
extrato = []
listaUsuarios = []
listaContas = []


while  True:

    opcao = input(MENU)

    if opcao == 'd':
        valor = float(input('Valor depósito: '))
        saldo = depositar(saldo, valor)

    elif opcao == 's':
        if numero_saques >= LIMITE_SAQUES:
            print(f'Número de saques excedido({LIMITE_SAQUES})')
        else:
            valor = float(input('Valor saque: '))
            saldo = sacar( saldo_sacar=saldo, valor_sacar=valor )
            numero_saques += 1

    elif opcao == 'e':
        if len(extrato) == 0:
            print('Não foram realizadas movimentações.')
        else:
            apresenta_extrato(saldo, extrato_apresentar = extrato)

    elif opcao == 'q':
        print('Obrigado por utilizar nossos serviços!')
        break

    elif opcao == 'nu':
        cpf = input('Informe o CPF: ')
        usuario = buscar_usuario(cpf, listaUsuarios)
        if usuario:
            print('Usuário já cadastrado!')
        else:
            cadastrar_usuario(cpf, listaUsuarios)

    elif opcao == 'nc':
        cpfNovaConta = input('Informe o CPF: ')
        usuario = buscar_usuario(cpfNovaConta, listaUsuarios)
        if not usuario:
            print('Usuário não cadastrado!')
        else:
            cadastrar_conta(usuario, listaContas)

    elif opcao == 'lc':
        listar_contas(listaContas)

    else: print('Opção inválida')

    wait = input('\nPressione <ENTER> para continuar...\n')

    os.system('cls' if os.name == 'nt' else 'clear')
