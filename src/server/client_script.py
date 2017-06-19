


import socket
import sys
import time
from test import test_defs
import logging
logger = logging.getLogger(__name__)

logging.basicConfig(filename='../client.log', filemode='w', level=logging.DEBUG)
logging.info('Logging Started')

##############################

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to %s port %s' % server_address, file=sys.stdout)
sock.connect(server_address)
wait_for_user = 0
cnt = 1
try:
    #while True:
    for m in test_defs.test_commands:
        time.sleep(1)
        #m = m + " #" + str(cnt).zfill(4)
        print(str(cnt).zfill(4) + ":" + m)
        cnt += 1
        if ("die" in m[0:5]):
            print('client: got a die command', file=sys.stdout)
            sock.sendall(m.encode())
            time.sleep(1)
            # raise
            break
        if "turn_on" in m[0:9]:
            wait_for_user = 1
        else:
            # adding length
            l = str(len(m)+5)
            sl = "{:0>4}:".format(l)
            slm = sl + m
            if wait_for_user != 0:
                input('hit any key to send this message')
            message =  slm
            #print(message)
            logger.debug('client script sending {}'.format(message))
            sock.sendall(message.encode())
            amount_received = 0
            #amount_expected = len(message)
            amount_expected = 4096 # arbitrary
            got_first_part = 0
            save_counter = 0
            try:
                while amount_received < amount_expected:
                    #print('amount rec: {}, amount exp {}'.format(amount_received, amount_expected))
                    save_counter += 1
                    if save_counter > 1000 :
                        print('save_counter over 1000. breaking!')
                        raise AssertionError
                    data = sock.recv(1024)
                    if len(data) == 0:
                        continue
                    data=data.decode()
                    if got_first_part == 0:
                        got_first_part = 1
                        l,d,data = data.partition(':')
                        amount_expected = int(l)
                        amount_received += len(data)+len(l)+len(d)
                    else:
                        amount_received += len(data)
            except AssertionError:
                logger.debug("Client recieve loop excceeded 1000 iterations on message {}".format(message))
                break

            time.sleep(1)
            print("\nServer Said:")
            print(data+"\n")
            logger.debug("ServerSaid: {}".format(data))


finally:
    print('client: closing socket', file=sys.stdout)
    logger.debug("Client closing socket")
    input("OK?")
    sock.close()