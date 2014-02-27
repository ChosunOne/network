import socket
import threading
from networkLibrary import *

print('Setting up server')

s = socket.socket()
host = socket.gethostname()
port = 12345
threads = []

s.bind((host, port))

print(host, 'set up on port', port)

s.listen(5)

print('Waiting for connections')

while True:
    (c, (ip, port)) = s.accept()
    newthread = clientThread(ip, port, c)
    newthread.__run__()
    threads.append(newthread)

for t in threads:
    t.join()
    