# oeitam

import sys
import logging

logger = logging.getLogger()
logging.basicConfig(filename='weekly.log', filemode='w', level=logging.DEBUG)
logging.info('Logging (into weekly.log)Started')


from src.db import db as database
from src.gtd import gtd as gettingthingsdone
from src.server import server as serverinst


# logger = logging.getLogger()
# logging.basicConfig(filename='weekly.log', filemode='w', level=logging.DEBUG)
# logging.info('Logging Started')


def main():


    db = database.Db()
    gtd = gettingthingsdone.Gtd(db)
    server = serverinst.Server(gtd)
    server.server_process()

    #input("Press enter to finish the program")
    logging.info('Logging Finished')
    print('Server Done. Bye')

if __name__ == '__main__':
    main()













# end


