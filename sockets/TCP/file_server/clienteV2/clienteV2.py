
#imports para o sistema
import socket
import sys, os
import json

DEBUG = True

def enviar_dados(opcao):
    nome_arquivo = opcao[1:]
    opcao = opcao[0]

    tcp_socket.send(int.to_bytes(opcao))

    #download arquivos
    if opcao == 10:
        print('----- Download de arquivos -----')

        #lendo e preparando nome do arquivo
        nome_arquivo = input('Digite o nome do Arquivo: ')
        nome_arquivo = nome_arquivo.encode()

        tamanho_nome = len(nome_arquivo)
        tamanho_nome = int.to_bytes(tamanho_nome, 4)

        #enviando tamanho do nome de arquivo e depois o nome do arquivo em si
        tcp_socket.send(tamanho_nome)
        tcp_socket.send(nome_arquivo)

        #recebendo status para saber se arquivo existe
        status = tcp_socket.recv(1)
        status = int.from_bytes(status)

        if status == 0:
            #recebendo tamanho do arquivo
            tamanho_arquivo = tcp_socket.recv(4)
            tamanho_arquivo = int.from_bytes(tamanho_arquivo)

            print(f'Tamanho do arquivo: {tamanho_arquivo}')

            #gravando arquivo recebido
            caminho_arquivo = f'arquivos/{nome_arquivo.decode()}'
            arquivo = open(caminho_arquivo, 'wb')
            while tamanho_arquivo > 0:
                dados = tcp_socket.recv(1024)
                arquivo.write(dados)
                tamanho_arquivo = tamanho_arquivo - 1024
            arquivo.close()

            print('Arquivo recebido com sucesso!!!')
        else: 
            print('Esse arquivo não existe.')

    #exbir lista
    if opcao == 20:
        #status da operação, caso deu certo: status = 0
        status = tcp_socket.recv(1)
        status = int.from_bytes(status)

        if status == 0:

            print('----- Listar Arquivos -----')
            tamanho_json = tcp_socket.recv(4)
            tamanho_json = int.from_bytes(tamanho_json)

            lista_json = tcp_socket.recv(tamanho_json)
            lista_json = json.loads(lista_json)

            #exibindo a lista
            pos = 0
            while pos < len(lista_json):
                dic = lista_json[pos]
                print(f"Arquivo: {dic['nome']} \nTamanho: {dic['tamanho']}")
                print('-'*10)
                pos = pos +1

        
        else:
            print('algum erro na operação')



    if opcao == 30:
        print('----- Upload de Arquivos -----')
        nome_arquivo = input('Digite o nome do arquivo: ')

        nome_arquivo = nome_arquivo.encode()    
        tamanho_nome = len(nome_arquivo)

        tcp_socket.send(int.to_bytes(tamanho_nome,4))
        tcp_socket.send(nome_arquivo.encode())

        print('tudo foi enviado, esperando status')
        status = tcp_socket.recv(1)
        status = int.from_bytes(status)
        if status == 1:
            print('confirmada permissão enviar arquivo')
            #enviando arquivo
            arquivo = open(f'arquivos/{nome_arquivo}', 'rb')
            while tamanho_arquivo > 0:
                dados = arquivo.read(1024)
                tcp_socket.send(dados)
                tamanho_arquivo -= 1024
            arquivo.close()

        print('arquivo enviado com sucesso!')
        if status == 0:
            print('permissão negada')

        
    if opcao == 50:
        nome_arquivo = input('Digite os nomes dos arquivos: ')
        nome_arquivo = nome_arquivo.replace(' ', '')
        nome_arquivo = nome_arquivo.encode()
        tamanho_nome = int.to_bytes(len(nome_arquivo), 4)


        tcp_socket.send(tamanho_nome)
        tcp_socket.send(nome_arquivo)

        #recebendo resposta com quantos arquivos encontrou
        quantidade_arquivos = tcp_socket.recv(4)
        quantidade_arquivos = int.from_bytes(quantidade_arquivos)

        if DEBUG: print('quantidade de arquivos a serem recebidos: ', quantidade_arquivos)

        if quantidade_arquivos == 0:
            print('sem nenhum arquivo para baixar')
            return 0
        
        for _ in range(quantidade_arquivos):
            #recebendo tamanho do nome, nome e tamanho do arquivo
            tamanho_nome = tcp_socket.recv(4)
            nome_arquivo = tcp_socket.recv(int.from_bytes(tamanho_nome))
            nome_arquivo = nome_arquivo.decode() #convertendo em string
            tamanho_arquivo = tcp_socket.recv(4)
            tamanho_arquivo = int.from_bytes(tamanho_arquivo) #convertendo em inteiro
            if DEBUG: print('recebendo arquivo: ', nome_arquivo)

            #recebendo bytes do arquivo
            arquivo = open(f'arquivos/{nome_arquivo}', 'wb')
            #valor a ser gravado para os bytes não serem confundido com o próximo arquivo
            gravar = 1024
            while tamanho_arquivo > 0:
                if min(tamanho_arquivo, gravar) == tamanho_arquivo:
                    gravar = tamanho_arquivo % 1024
                dados = tcp_socket.recv(gravar)
                arquivo.write(dados)
                tamanho_arquivo -= gravar
            arquivo.close()


def exibicao():
    try:
        while True:
            print('''
----- legenda -----
ls : listar arquivos
dw : baixar um arquivo
up : envia um arquivo
qt : sair do programa
   [nome dos arquivos]
          ''')
        
            opcoes = {'qt'  :  0,
                    'dw'  : 10,
                    'ls'  : 20,
                    'up'  : 30,
                    'dw-m': 50}

            #traduzindo solicitação
            opcao = input('digite uma opção: ')
            opcao = opcao.replace(',', ' ').split()
            #para downloads de mais de um arquivo
            if len(opcao) > 2 and opcao[0] == 'dw':
                opcao[0] = 'dw-m'

            opcao[0] = opcoes[opcao[0]] #substitui a string por um inteiro com o número que será enviado ao servidor

            if opcao[0] == 0:
                print('Encerrando conexão.')
                return 0
            if opcao[0] == 20: #se não for a opcao de downloads multiplos, ele exclúi os outros parâmetros
                opcao = [opcao.pop(0)]
            if opcao[0] != 50 and len(opcao) > 2:
                print('Para essa opção, só pode um arquivo por vez, será considerado apenas o primeiro arquivo da lista')
                opcao = opcao[0:2]
            if DEBUG: print(opcao)


            #comunicação com o servidor:
            enviar_dados(opcao)
    
    except Exception as e:
        erro = type(e).__name__
        print('Erro na seleção, tente novamente...\nErro: ', erro)
        return exibicao()

def config_conexao():
    #sabendo informações do servidor
    parametros = sys.argv
    if len(parametros) >= 3:
        host = parametros[1]
        port = int(parametros[2])
    elif len(parametros) == 2:
        host = parametros[1]
        port = int(input('Digite o número da porta: '))
    else:
        host = input('Digite o ip do host: ')
        port = int(input('Digite o número da porta: '))

    return host, port

def main():
    global tcp_socket

    #estabelecendo conexão
    host, port = config_conexao()
    
    #informações sobre o socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((host, port))

    exibicao()
    
    tcp_socket.close()

main()
