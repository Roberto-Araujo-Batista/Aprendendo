import socket
import sys, os
import json

#estabelecendo conexão
def main():
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

    #informações sobre o socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((host, port))
    
    #enviando solicitação
    opcao = int(input('digite uma opção: '))  
    opcao_e = opcao.to_bytes(1)
    tcp_socket.send(opcao_e)
    
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
            print(lista_json)
        
        else:
            print('algum erro na operação')



    tcp_socket.close()

main()