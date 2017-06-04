
import socket
import sys
import time
from subprocess import Popen, CREATE_NEW_CONSOLE

import logging
logger = logging.getLogger(__name__)



class Server(object):
    def __init__(self, gtd):
        print('server init')
        self.gtd = gtd

    # start_the_client method starts the client seperate process
    def start_the_client(self):
        print("Launching the clinet")
        client_child_stdout = open('client_child_stdout', 'w')
        client_child_stderr = open('client_child_stderr', 'w')
        pc = Popen([sys.executable, 'server/client_script.py'],
                   #stdout=client_child_stdout,
                   #stderr=client_child_stderr,
                   creationflags=CREATE_NEW_CONSOLE)

        time.sleep(2)
        if pc.returncode == 63:
            print("Client could not initilize properly", file=sys.stderr)
        print('class Server initialized', file=sys.stderr)

        # setup variables
        self.client_process = pc

    ###################### NOT USED ????  #############################
    # send_data_to_client method sends data to the client to display
    # this is for the gtd to use
    def send_data_to_client(self, data):
        print('sending data to the client')
        pass
    ###################### NOT USED ????  #############################

    # server_process method is the main method of the server
    # crates a socket from the server for the client to use
    # once requests are coming from the client, it sends it to
    # the gtd for processing
    def server_process(self):
        print('Starting the communications server')
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = ('localhost', 10000)
        print('starting up on %s port %s' % server_address, file=sys.stderr)
        self.sock.bind(server_address)

        # Listen for incoming connections
        self.sock.listen(1)

        # start the slient
        self.start_the_client()

        while True:
            # Wait for a connection
            print('waiting for a connection', file=sys.stderr)
            connection, client_address = self.sock.accept()
            try:
                print('connection from', client_address, file=sys.stderr)

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(1024)
                    print('recieved "%s"' % data.decode(), file=sys.stderr)
                    if (data.decode() == 'die'):
                        print('server: Dieing!!!')
                        #raise
                        break
                    if data:
                        print('sending data to the proc', file=sys.stderr)
                        self.gtd.take_data(data.decode())
                        self.gtd.process() # gtd to process the latest data it recieved
                        # once the process method is done, it means data is ready for the
                        return_message = self.gtd.get_message_back_to_client()
                        connection.sendall(return_message.encode())
                    else:
                        print('no more data from ', client_address, file=sys.stderr)
                        break

            finally:
                # Clean up the connection
                print('server: Closing socket', file=sys.stdout)
                connection.close()
                break
        print('server off')






