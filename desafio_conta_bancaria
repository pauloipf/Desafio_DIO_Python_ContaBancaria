menu = '''

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> '''

saldo = 0
limite = 500
numero_saques = 0
LIMITE_SAQUES = 3
extrato = []



while  True:

    opcao = input(menu)

    if opcao == 'd':
        valor = float(input('Valor depósito: '))
        if valor <= 0:
            valor = float(input('Valor depósito deve ser positivo: '))

        saldo += valor
        extrato.append(valor)

    elif opcao == 's':
        if numero_saques >= LIMITE_SAQUES:
            print(f'Número de saques excedido({LIMITE_SAQUES})')
        else:
            valor = float(input('Valor saque: '))
            if saldo < valor:
                print(f'Valor de saque superior ao saldo(R$ {saldo:.2f})')
            else:
                if valor <= 0:
                    valor = float(input('Valor saque deve ser positivo: '))
                saldo -= valor
                extrato.append(-valor)
                numero_saques += 1
         

    elif opcao == 'e':
        if len(extrato) == 0:
            print('Não foram realizadas movimentações.')
        else:
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

    elif opcao == 'q':
        break

    else: print('Opção inválida')

