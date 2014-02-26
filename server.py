import socket
from multiprocessing import Pool
from networkLibrary import *

print('Setting up server')

s = socket.socket()
host = socket.gethostname()
port = 12345
clients = {}

s.bind((host, port))

print(host, 'set up on port', port)

s.listen(5)

print('Waiting for connections')

while True:
    c, addr = s.accept()

    if addr[0] not in clients.keys():

        user = client()
        user.socket = c
        user.address = addr[0]

        clients[addr[0]] = user

        print('New user from', user.address)

        message = 'Thank you for connecting'

    elif addr[0] in clients.keys():

        message = 'Thank you for connecting again'

    print('Got connection from', addr[0])
    
    c.send(message.encode())
    c.close()
    