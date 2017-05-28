
import socket
import sys
import time
from subprocess import Popen, CREATE_NEW_CONSOLE




class Server(object):
    def __init__(self, proc):
        # init server
        server_child_stdout = open('server_child_stdout', 'w')
        server_child_stderr = open('server_child_stderr', 'w')
        ps = Popen([sys.executable,"server/server_script.py"],
                             #stdout=server_child_stdout,
                             #stderr=server_child_stderr,
                             creationflags=CREATE_NEW_CONSOLE)
        time.sleep(2)
        ps.poll()
        # print( p.returncode)
        if ps.returncode == 63:
            print('Server could not initialize properly', file=sys.stderr)
        # init client
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
        self.proc = proc
        self.client_process = pc
        self.server_process = pc

        # pass the server boject to the proc
        proc.take_server_object(self)

    def return_to_client(self):
        pass

    def send_data_to_client(self, data):
        print('sending data to the client')
        pass









