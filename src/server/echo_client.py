
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
try:
    while True:
        l = raw_input("say-->")
        # Send data
        message = 'This is the message.  It will be sent.'
        print >> sys.stderr, 'sending "%s"' % l
        sock.sendall(l)

        # Look for the response
        amount_received = 0
        amount_expected = len(l)

        while amount_received < amount_expected:
            data = sock.recv(1024)
            amount_received += len(data)
            print >> sys.stderr, 'received "%s"' % data

finally:
    print >> sys.stderr, 'closing socket'
    sock.close()

