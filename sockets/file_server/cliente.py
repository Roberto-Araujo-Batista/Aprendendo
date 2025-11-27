import socket, os


host = '127.0.0.1'
port = 60000

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

nome_arquivo = input('Digite o nome do arquivo: ')
nome_arquivo = nome_arquivo.encode()
tamanho_arquivo = len(nome_arquivo).to_bytes()

udp_socket.sendto(tamanho_arquivo, (host, port))
udp_socket.sendto(nome_arquivo, (host, port))



status , src = udp_socket.recvfrom(1)
status = int.from_bytes(status)

if status:
    print('Arquivo encontrado, recebendo arquivo...')

else:
    print('Arquivo não encontrado \nFim da execução')