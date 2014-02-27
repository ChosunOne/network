import socket
import threading
from queue import Queue

lock = threading.Lock()

class client:
    def __init__(self, ip, port, socket):
        self.ip = ip
        self.port = port
        self.socket = socket

class clientThread(threading.Thread):
    def __init__(self, ip, port, socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsock = socket

    def __run__(self):
        print('Connection from :', self.ip, ':', str(self.port))

        self.clientsock.send('Welcome to the server!\n'.encode())

        data = 'data'

        while len(data):
            try:
                data = self.clientsock.recv(2048)
                print('Client sent:', data)
                self.clientsock.send(('You sent me:' + data).encode())
            except:
                print('Client disconnected')
                break

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