import socket

host = '127.0.0.1'
port = 60000

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.connect((host, port))

msg = input('Digite uma mensagem: ')

msg = msg.encode()

tcp_socket.send(msg)

tcp_socket.close()

