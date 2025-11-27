import socket

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_socket.bind('', 60000)
print('Servidor Online')

while True:
    print('Aguardando solicitações...')

    dados, cliente = udp_socket.recvfrom(4096)
    udp_socket.sendto(dados, cliente)

    dados = dados.decode('utf-8')

    print('dados recebidos: \n', dados)
