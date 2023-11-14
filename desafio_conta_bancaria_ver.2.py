def depositar(saldo, valor, /):
    if valor <= 0:
        valor = float(input('Valor depósito deve ser positivo: '))
    saldo += valor
    extrato.append(valor)
    return saldo

def sacar(*, saldo, valor):
    if saldo < valor:
        print(f'Valor de saque superior ao saldo(R$ {saldo:.2f})')
    else:
        if valor <= 0:
            valor = float(input('Valor saque deve ser positivo: '))
        saldo -= valor
        extrato.append(-valor)
    return saldo

def apresentaExtrato(saldo,/,*, extrato):
    print('''
          Extrato
=============================
  Tipo            Valor 
------------   --------------
                  ''')
    for valor in extrato:
        if valor > 0:
            print(f'depósito \tR$ {valor:>9,.2f}')
        else: print(f'saque \t\tR$ {valor:>9,.2f}')
    print(f'saldo \t\tR$ {saldo:>9,.2f}') 

def cadastrarUsuario(cpf, usuarios):
    nome = input('Nome: ')
    dataNascimento = input('Data de nascimento (dd-mm-aaaa): ')
    print('Endereço: ')
    rua = input('Rua: ')
    numero = input('Número: ')
    endereco = rua + ', ' + numero
    bairro = input('Bairro: ')
    cidade = input('Cidade: ')
    estado = input('UF: ')

    usuarios.append({"cpf":cpf, 
                     "nome":nome, 
                     "dataNascimento":dataNascimento, 
                     "endereco":endereco,
                     "bairro":bairro, 
                     "cidade":cidade,
                     "estado":estado
                     })
    print('Usuário cadastrado!')

def buscarUsuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario

def cadastrarConta(usuario, contas):
    proxConta = len(contas)+1
    contas.append({"agencia":AGENCIA,
                   "conta":proxConta,
                   "usuario":usuario
                   })
    print('Conta cadastrada com sucesso!')

def listarContas(contas):
    for conta in contas:
        linha = f'''\
Agência:\t{conta['agencia']}
  Conta:\t{conta['conta']}
Titular:\t{conta['usuario']['nome']}
    CPF:\t{conta['usuario']['cpf']}'''
        print(50 * '=')
        print(linha)


menu = '''
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
limite = 500
numero_saques = 0
LIMITE_SAQUES = 3
AGENCIA = '0001'
extrato = []
listaUsuarios = []
listaContas = []


while  True:

    opcao = input(menu)

    if opcao == 'd':
        valor = float(input('Valor depósito: '))
        saldo = depositar(saldo, valor)

    elif opcao == 's':
        if numero_saques >= LIMITE_SAQUES:
            print(f'Número de saques excedido({LIMITE_SAQUES})')
        else:
            valor = float(input('Valor saque: '))
            saldo = sacar(
                saldo=saldo,
                valor=valor,
                )
            numero_saques += 1

    elif opcao == 'e':
        if len(extrato) == 0:
            print('Não foram realizadas movimentações.')
        else:
            apresentaExtrato(saldo, extrato = extrato)

    elif opcao == 'q':
        break

    elif opcao == 'nu':
        cpf = input('Informe o CPF: ')
        usuario = buscarUsuario(cpf, listaUsuarios)
        if usuario:
            print(f'Usuário já cadastrado!')
        else:
            cadastrarUsuario(cpf, listaUsuarios)

    elif opcao == 'nc':
        cpfNovaConta = input('Informe o CPF: ')
        usuario = buscarUsuario(cpfNovaConta, listaUsuarios)
        if not usuario:
            print(f'Usuário não cadastrado!')
        else:
            cadastrarConta(usuario, listaContas)

    elif opcao == 'lc':
        listarContas(listaContas)

    else: print('Opção inválida')

    wait = input('\nPressione <ENTER> para continuar...\n')

