import socket

class client:
    def __init__(self):
        self.socket = socket.socket()
        self.address = ''