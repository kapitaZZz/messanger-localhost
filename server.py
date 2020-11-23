import socket, time

host = socket.gethostbyname(socket.gethostname())  # ip address of server
port = 9090

clients = []

s_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # AF_NET - TCP, SOCK_DGRAM - IP
s_temp.bind(host, port)  # create protocol TCP/IP

quit_status = False  # for finish loop
print('[ Server started! ]')

while not quit_status:
    try:
        data, addr = s_temp.recvfrom(1024)  # data - message by user, addr - user address, 1024bytes

        if addr not in clients:  # check new client in clients, if not - add
            clients.append(addr)

        itsatime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # current time of message or any event

        print("[" + addr[0] + "]=[" + str(addr[1]) + "]=[" + itsatime + "]/", end="")  # server message
        print(data.decode("utf-8"))

        for client in clients:
            if addr != client:
                s_temp.sendto(data, client)

    except:
        print('\n [ Server stopped! ]')
        quit_status = True

s_temp.close()
