import socket, os

host = '192.168.1.110'
port = 60000

# acoplar o socket da camada de transporte
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.connect((host, port))

nome_arquivo = input('Digite o nome do arquivo: ')
nome_arquivo = nome_arquivo.encode()
tamanho_nome = len(nome_arquivo).to_bytes()

tcp_socket.send((tamanho_nome))
tcp_socket.send(nome_arquivo)

status = tcp_socket.recv(1)
status = int.from_bytes(status)

if status:
    print('Arquivo encontrado, recebendo arquivo...')

    tamanho_arquivo = tcp_socket.recv(4)
    tamanho_arquivo = int.from_bytes(tamanho_arquivo)

    arquivo = open(nome_arquivo, 'bw')
    while tamanho_arquivo > 0:
        dados = tcp_socket.recv(4096)
        arquivo.write(dados)
        tamanho_arquivo = tamanho_arquivo - 4096
    print('Arquivo salvo com sucesso')
    arquivo.close()

else:
    print('Arquivo não encontrado')

tcp_socket.close()
print('Fim da execução')
