import socket

s = socket.socket()
host = input('Please enter the ip you would like to connect to\n')
port = int(input('Please enter the port to connect on\n'))

print('Connecting to', host, 'on port', port)

try:
    s.connect((host, port))
except:
    print('Unable to connect to', host, 'on port', port)

while True:

    received = s.recv(1024)
    
    if received != b'':
        print(received.decode('utf-8'))

    s.close
