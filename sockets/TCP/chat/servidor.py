import socket, threading

DEBUG = False

def get_ip():
    hostname = socket.gethostname()
    ips      = socket.gethostbyname(hostname)
    return ips

def receive_msg(con, src):
        try:
            while True:   
                #receving len of the message
                if DEBUG: print('receiving the message')
                
                msg_len = con.recv(4)
                msg = con.recv(int.from_bytes(msg_len))

                if DEBUG: print(src[0], src[1], ' sends the following message: \n- ' + msg.decode())
                #sending the message to others users
                for cli_con, cli_src in ip_list:
                    if cli_con != con:
                        cli_con.send(msg_len)
                        cli_con.send(msg)
                        if DEBUG: print('enviado para ', cli_src)
        except Exception as e:
            print(e)

def connecting():
    global ip_list
    #connecting the socket
    print(f'Connecting server by ips: {get_ip()}')

    while True:
        con, src = tcp_socket.accept()
        print(f'Connected with {src[0]} in port {src[1]}')

        #putting ips on a list to control the users that keep connected
        ip_list.append((con, src))

        threading.Thread(target=receive_msg, args =(con, src)).start()

ip_list = []

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind(('', 20000))
tcp_socket.listen(1)

connecting()
