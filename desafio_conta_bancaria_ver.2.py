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
-----------------------------
          Extrato
-----------------------------
  Tipo            Valor 
------------   --------------
                  ''')
    for valor in extrato:
        if valor > 0:
            print(f'depósito \tR$ {valor:>9,.2f}')
        else: print(f'saque \t\tR$ {valor:>9,.2f}')
    print(f'saldo \t\tR$ {saldo:>9,.2f}') 

def cadastrarUsuario(usuarios):
    cpf = input('Informe o CPF: ')
    usuario = buscarUsuario(cpf, usuarios)
    if usuario:
        print(f'Usuário, {usuario["nome"]}, já cadastrado!')
        return
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
                     "Nome":nome, 
                     "dataNascimento":dataNascimento, 
                     "endereco":endereco,
                     "bairro":bairro, 
                     "cidade":cidade,
                     "estado":estado
                     })
    print('Usuário cadastrado!')

def buscarUsuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf
            return usuario

menu = '''

[d]/tDepositar
[s]/tSacar
[e]/tExtrato
[q]/tSair
[nu]/tCadastrar novo usuário 

=> '''

saldo = 0
limite = 500
numero_saques = 0
LIMITE_SAQUES = 3
extrato = []
listaUsuarios = []


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
        cadastrarUsuario(listaUsuarios)

    else: print('Opção inválida')

