# oeitam

import sys
import logging
from src.db import db as database
from src.gtd import gtd as gettingthingsdone
from src.server import server as serverinst
from src import defs

logger = logging.getLogger()

def main():

    logging.basicConfig(filename='../weekly.log', filemode='w', level=logging.DEBUG)
    logging.info('Logging Started')

    db = database.Db()
    gtd = gettingthingsdone.Gtd(db)
    server = serverinst.Server(gtd)
    server.server_process()

    input("Press enter to finish the program")
    logging.info('Logging Finished')

if __name__ == '__main__':
    main()













# end


