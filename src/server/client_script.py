


import socket
import sys
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to %s port %s' % server_address, file=sys.stderr)
sock.connect(server_address)
try:
    while True:
        message = input("say-->")
        #time.sleep(3); print('--')
        # Send data
        print('sending "%s"' % message, file=sys.stderr)
        #print(message) ; time.sleep(3) ; print('--')
        sock.sendall(message.encode())
        #time.sleep(3); print('--')
        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
           data = sock.recv(1024)
           amount_received += len(data)
           print('recieved "%s"' % data.decode(), file=sys.stderr)

finally:
    print('closing socket', file=sys.stderr)
    sock.close()