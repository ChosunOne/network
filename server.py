import socket
import threading
from queue import Queue
from networkLibrary import *

print('Setting up server')

s = socket.socket()
host = socket.gethostname()
port = 12345
q = Queue()
que = []
que.append(q)

MAXUSERS = 4

s.bind((host, port))

print(host, 'set up on port', port)

s.listen(5)

print('Waiting for connections')

while True:
    (c, (ip, port)) = s.accept()
    if c:
        
        user = client(ip, port, c)
        que[0].put(user)
        
        t = threading.Thread(target=clientWorker, args=que)
        t.daemon = True
        t.start()

q.join()

    

    