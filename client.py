import socket, threading, time

key = 8194

shutdown = False
join = False


def receving(name, sock):
    '''
    Get messages and decode
    :param name:
    :param sock:
    :return:
    '''
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)  # get message from another user
                # print(data.decode('utf-8'))

                # begin decryption message
                decrypt = ""
                k = False
                for i in data.decode("utf-8"):
                    if i == ':':
                        k = True
                        decrypt += i
                    elif k == False or i == ' ':
                        decrypt += i
                    else:
                        decrypt += chr(ord(i) ^ key)
                    print(decrypt)
                # end decryption message

                time.sleep(0.2)
        except:
            pass


host = socket.gethostbyname(socket.gethostname())
port = 0

server = ('192.168.0.101', 9090)

s_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_temp.bind(host, port)  # connect to server
s_temp.setblocking(0)  # use for exit for user

alias = input('Name: ')  # username in chat

rT = threading.Thread(target=receving, args=("RecvThread", s_temp))
rT.start()

while shutdown == False:  # send message to a server
    if join == False:  # user join to a server
        s_temp.sendto(("[" + alias + "] => join chat ").encode("utf-8"), server)
        join = True
    else:
        try:
            message = input()

            # begin encryption message
            crypt = ''
            for i in message:
                crypt += chr(ord(i) ^ key)
            message = crypt
            # end encryption message

            if message != "":
                s_temp.sendto(("[" + alias + "] :: " + message).encode("utf-8"), server)

            time.sleep(0.2)
        except:
            s_temp.sendto(("[" + alias + "] <= left chat ").encode("utf-8"), server)

rT.join()
s_temp.close()
