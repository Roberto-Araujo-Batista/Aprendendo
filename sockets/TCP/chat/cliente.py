import socket, sys, threading

parametros = sys.argv

host = parametros[1]
port = 20000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

def enviar_mensagem():
    while True:
        msg = input('Digite uma mensagem: ')
        if msg != '':
            tam = len(msg)
            sock.send(int.to_bytes(tam, 4))
            sock.send(msg.encode())

def receber_mensagem():
    while True:
        tam = sock.recv(4)
        msg = sock.recv(int.from_bytes(tam))
        print(msg.decode())

threading.Thread(target=enviar_mensagem).start()
threading.Thread(target=receber_mensagem).start()
