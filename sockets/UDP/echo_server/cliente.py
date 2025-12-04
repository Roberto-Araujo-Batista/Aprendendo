import socket

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


ip = '127.0.0.1'
porta = 60000
servidor = (ip, porta)

dados = input('Digite os dados a serem enviados: \n')
dados = dados.encode()

udp_socket.sendto(dados, servidor)

dados, serv = udp_socket.recvfrom(4050)

print('retorno do servidor: /n', dados)
