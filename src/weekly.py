# oeitam

import sys
import logging
from src.db import db as database
from src.gtd import gtd as gettingthingsdone
from src.server import server as serverinst
from src import defs
import os

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
    # temporary - removing file
    print(os.getcwd())
    if os.path.isfile('../data/dfm.csv'):
        os.remove('../data/dfm.csv')
    if os.path.isfile('../data/dfp.csv'):
        os.remove('../data/dfp.csv')
    if os.path.isfile('../data/dft.csv'):
        os.remove('../data/dft.csv')
    if os.path.isfile('../data/dfa.csv'):
        os.remove('../data/dfa.csv')
    main()













# end


