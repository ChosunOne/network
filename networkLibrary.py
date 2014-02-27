import socket
import threading
from queue import Queue

lock = threading.Lock()

class client:
    def __init__(self):
        self.name = input('Please choose a username\n')
        self.host = input('Please enter an ip to connect to\n')
        self.port = int(input('Please enter a port to connect on\n'))
        self.s = socket.socket()

    def start(self):
        
        print('Connecting to', self.host, 'on port', self.port)
        
        try:
            self.s.connect((self.host, self.port))
            self.s.send(self.name.encode())
            
        except:
            print('Unable to connect to', self.host, 'on port', self.port)

        while True:

            try:
                received = self.s.recv(2048)

                if received != b'':
                    print(received.decode('utf-8'))

            except:
                print('Connection to server lost')
                break

            message = input('Send a message to the server\n')

            try:
                self.s.send(message.encode())
            except:
                print('Error sending message')

        self.s.close()


class serverClient:
    def __init__(self, ip, port, socket):
        self.ip = ip
        self.port = port
        self.socket = socket
        self.name = ''

class server:
    def __init__(self):
        self.socket = socket.socket()
        self.hostName = socket.gethostname()
        self.port = int(input('Please indicate a port for the server\n'))
        self.q = Queue()
        self.queue = []
        self.queue.append(self.q)
        self.maxUsers = 10

    def start(self):
        print('Setting up server')

        self.socket.bind((self.hostName, self.port))
        
        print(self.hostName, 'set up on port', str(self.port))
        
        self.socket.listen(5)

        print('Waiting for connections...')

        while True:
            (c, (ip, port)) = self.socket.accept()
            if c:
                user = serverClient(ip, port, c)
                self.queue[0].put(user)
                t = threading.Thread(target=clientWorker, args=self.queue)
                t.daemon = True
                t.start()

        self.queue[0].join()

def handleClient(ip, port, socket):
    
    user = serverClient(ip, port, socket)
    
    with lock:
        print('Connection from :', user.ip, ':', str(user.port))

    user.socket.send('Welcome to the server!\n'.encode())

    username = user.socket.recv(2048)
    user.name = username.decode()

    while True:
        try:

            data = user.socket.recv(2048)
            
            with lock:
                print(user.name, 'sent:' + data.decode())

            user.socket.send(('You sent me:' + data.decode()).encode())
            
        except:
            with lock:
                print(user.name, 'disconnected')
                user.socket.close()
                break

def clientWorker(q):
    while True:
        item = q.get()
        handleClient(item.ip, item.port, item.socket)
        q.task_done()