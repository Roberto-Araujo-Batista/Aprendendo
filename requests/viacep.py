import requests

def encontra_cep():
    print('--- Digite os dados abaixo ---')
    uf         = input('uf: ').upper()
    cidade     = input('cidade: ').title()
    logradouro = input('logradouro: ').replace(' ', '+')

    link = f'https://viacep.com.br/ws/{uf}/{cidade}/{logradouro}/json/'
    endereco = requests.get(link).json()

    #caso retorne apenas um, então mostre esse único endereço
    if len(endereco) == 1:
        unico_endereco = endereco[0]

        print('-'*20)
        for dados in unico_endereco.keys():
            print(f'{dados}: {unico_endereco[dados]}')
    #caso o nome seja genérico, ele retornará uma lista de dicionários com vários endereços
    else:
        print('--- Foram encontrados mais de um resultado: ---')
        print('-'*20)

        for any in endereco:
            for dados in any.keys():
                print(f'{dados}: {any[dados]}')
            print('-'*20)


def encontra_endereco():
    cep = input('entre com o seu cep: ')
    link = f'https://viacep.com.br/ws/{cep}/json/'
    endereco = requests.get(link).json()

    #exibição do dicionário
    print('-' * 20)
    for dados in endereco.keys():
        print(f'{dados}: {endereco[dados]}')

def menu():
    print('''
    1. Encontrar CEP.
    2. Encontrar Endereço pelo CEP.
    ''')

    opcao = int(input('Escolha uma opção: '))

    if opcao == 1:
        encontra_cep()
    elif opcao == 2:
        encontra_endereco()

if __name__ == '__main__':
    menu()
