
import socket
import sys


class Server(object):
    def __init__(self):
        # init server
        pass
        # init client
        pass
        print('class Server initialized')

    def weekly_server(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = ('localhost', 10000)
        print('starting up on %s port %s' % server_address, file=sys.stderr)
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)

        while True:
            # Wait for a connection
            print('waiting for a connection', file=sys.stderr)
            connection, client_address = sock.accept()
            try:
                print('connection from', client_address, file=sys.stderr)

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(1024)
                    print('recieved "%s"' % data, file=sys.stderr)
                    if data:
                        print('sending data back to the client', file=sys.stderr)
                        connection.sendall(data)
                    else:
                        print('no more data from ', client_address, file=sys.stderr)
                        break

            finally:
                # Clean up the connection
                print('Closing socket', file=sys.stderr)
                connection.close()

    def weekly_client(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 10000)
        print('connecting to %s port %s' % server_address, file=sys.stderr)
        sock.connect(server_address)
        try:
            while True:
                message = input("say-->")
                # Send data
                print('sending "%s"' % message, file=sys.stderr)
                sock.sendall(message)

                # Look for the response
                amount_received = 0
                amount_expected = len(message)

                while amount_received < amount_expected:
                    data = sock.recv(1024)
                    amount_received += len(data)
                    print('recieved "%s"' %data, file=sys.stderr)

        finally:
            print('closing socket', file=sys.stderr)
            sock.close()




