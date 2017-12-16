
import socket
import sys

import time
from subprocess import Popen, CREATE_NEW_CONSOLE
import os

from src import defs
#from src.server import client_direct

import logging
logger = logging.getLogger(__name__)



# start_the_client method starts the client seperate process
#if (defs.mode == 'direct' or defs.mode == 'socket'):
#    print(defs.days_of_week)
#else:
print("Launching the clinet")
pc = Popen([sys.executable, defs.local_client_script],
           creationflags=CREATE_NEW_CONSOLE)
#print(pc)
time.sleep(1)
if pc.returncode == 63:
    print("Client could not initilize properly", file=sys.stderr)
print('Client Stand Alone (sa) initialized', file=sys.stderr)

