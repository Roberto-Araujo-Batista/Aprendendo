import socket, sys, threading

parametros = sys.argv

host = parametros[1]
port = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

def enviar_mensagem():
    msg = input('Digite uma mensagem: ')

    tam = len(msg)

    sock.send(int.to_bytes(tam, 4))
    sock.send(msg.decode())


while True:
    print('----- recebendo mensagens -----')
    tam = sock.recv(4)
    msg = sock.recv(tam)
    print(msg)

    threading.Thread(target=enviar_mensagem).start()
