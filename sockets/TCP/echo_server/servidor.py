import socket 

host = ''
port = 60000

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((host, port))

tcp_socket.listen(1)

print('Recebendo Mensagens...')

while True:

    con, cliente = tcp_socket.accept()
    print('Conectado por: ', cliente)

    while True:
        msg = con.recv(1024)
        if not msg: break
        print(cliente, msg.decode('utf-8'))
    print('finalizando conexão do cliente', cliente)
    con.close()