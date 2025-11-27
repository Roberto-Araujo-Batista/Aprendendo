import socket, os


host = '127.0.0.1'
port = 60000
servidor = (host, port)

#acoplar o socket da camada de transporte
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

nome_arquivo = input('Digite o nome do arquivo: ')
nome_arquivo = nome_arquivo.encode()
tamanho_nome = len(nome_arquivo).to_bytes()

udp_socket.sendto(tamanho_nome, (servidor))
udp_socket.sendto(nome_arquivo, (servidor))



status , src = udp_socket.recvfrom(1)
status = int.from_bytes(status)

if status:
    print('Arquivo encontrado, recebendo arquivo...')

    tamanho_arquivo = udp_socket.recvfrom(4)
    tamanho_arquivo = int.from_bytes(tamanho_arquivo)
    

    

else:
    print('Arquivo não encontrado')


udp_socket.close()
print('Fim da execução')