


import socket
import sys
import time
from test import test_defs
import logging
#cd_logger = logging.getLogger(__name__)

logging.basicConfig(filename='client.log', filemode='w', level=logging.DEBUG)
logging.info('Logging (client direct) Started')

cd_logger = logging.getLogger(__name__)

class client(object):
    def __init__(self, server):
        self.server = server
        self.f = open('clientlog.log','w')

    def operate(self):
        wait_for_user = 0
        cnt = 1
        for m in test_defs.test_commands:
            print(str(cnt).zfill(4) + ":" + m)
            cnt += 1
            if ("die" in m[0:5]):
                print('client: got a die command', file=sys.stdout)
                break
            if "turn on" in m[0:9]:
                wait_for_user = 1
            else:
                l = str(len(m)+5)
                sl = "{:0>4}:".format(l)
                slm = sl + m
                if wait_for_user != 0:
                    input('hit any key to send this message')
                message =  slm
                cd_logger.debug('client script sending {}'.format(message))
                recieved_data = self.server.command(message)
                self.f.write(str(cnt).zfill(4) + ":" + "\n" + message+"\n")
                self.f.write(recieved_data+"\n"+"\n")
                print("\nServer Said:")
                print(recieved_data+"\n")
                cd_logger.debug("ServerSaid: {}".format(recieved_data))

        print('client: closing socket', file=sys.stdout)
        cd_logger.debug("Client closing socket")
        self.f.close()
        #input("OK?")




