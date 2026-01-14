import socket, threading

def get_ip():
    hostname = socket.gethostname()
    ips      = socket.gethostbyname(hostname)
    return ips

def receive_msg(con, src):
        #receving len of the message
        print('receiving the message')
        msg_len = con.recv(4)
        msg = con.recv(int.from_bytes(msg_len))

        print(src[0], src[1], ' sends the following message: \n- ' + msg.decode())

        #sending the message to others users
        for cli_con, cli_src in ip_list:
            if cli_con != con:
                cli_con.send(msg)

def connecting():
    global ip_list
    #connecting the socket
    print(f'Connecting server by ips: \n{get_ip()}')

    cond = 'True'
    while cond == 'True':
        con, src = tcp_socket.accept()
        print(f'Connected with {src[0]}')

        #putting ips on a list to control the users that keep connected
        ip_list.append((con, src))

        threading.Thread(target=receive_msg, args =(con, src)).start()


ip_list = []

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind(('', 20000))
tcp_socket.listen(1)


threading.Thread(target=connecting).start()


