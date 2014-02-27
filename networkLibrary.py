import socket
import threading
from queue import Queue

lock = threading.Lock()

class client:
    def __init__(self, ip, port, socket):
        self.ip = ip
        self.port = port
        self.socket = socket

class server:
    def __init__(self, port):
        self.socket = socket.socket()
        self.hostName = socket.gethostname()
        self.port = port
        self.q = Queue()
        self.queue = []
        self.queue.append(self.q)
        self.maxUsers = 10

    def start(self):
        self.socket.bind((self.hostName, self.port))
        
        print(self.hostName, 'set up on port', str(self.port))
        
        self.socket.listen(5)

        print('Waiting for connections...')

        while True:
            (c, (ip, port)) = self.socket.accept()
            if c:
                user = client(ip, port, c)
                self.queue[0].put(user)
                t = threading.Thread(target=clientWorker, args=self.queue)
                t.daemon = True
                t.start()

        self.queue[0].join()

def handleClient(ip, port, socket):
    
    user = client(ip, port, socket)
    
    with lock:
        print('Connection from :', user.ip, ':', str(user.port))

    user.socket.send('Welcome to the server!\n'.encode())

    data = 'data'

    while len(data):
        try:
            data = user.socket.recv(2048)
            with lock:
                print('Client sent:', data)
            user.socket.send(('You sent me:' + data).encode())
        except:
            with lock:
                print('Client disconnected')
                break

def clientWorker(q):
    while True:
        item = q.get()
        handleClient(item.ip, item.port, item.socket)
        q.task_done()