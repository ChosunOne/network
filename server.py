import socket
import threading
from queue import Queue
from networkLibrary import *

port = int(input('Please indicate a port for the server'))

print('Setting up server')

s = server(port)
s.start()

    