import socket
import threading

class client:
    def __init__(self):
        self.socket = socket.socket()
        self.address = ''

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