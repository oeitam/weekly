


import socket
import sys
import time
from test import test_defs

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to %s port %s' % server_address, file=sys.stdout)
sock.connect(server_address)
try:
    #while True:
    for m in test_defs.test_commands:
        print('going to send:')
        print(m)
        input('hit any key to send this message')
        message =  m
        #print(message)
        if (message == "die"):
            print('client: got a die command', file=sys.stdout)
            sock.sendall(message.encode())
            #time.sleep(1)
            #raise
            break
        print('sending "%s"' % message, file=sys.stdout)
        sock.sendall(message.encode())
        amount_received = 0
        amount_expected = len(message)
        #while amount_received < amount_expected:
        #    print('amount rec: {}, amount exp {}'.format(amount_received, amount_expected))
        #    data = sock.recv(1024)
        #    amount_received += len(data)
        #    time.sleep(1)
        #    print('c recieved "%s"' % data.decode(), file=sys.stdout)

finally:
    print('client: closing socket', file=sys.stdout)
    sock.close()