# oeitam

import sys
import os
import pandas as pd
import logging
logger = logging.getLogger(__name__)


class Db(object):
    def __init__(self):
        # set up or load the databases. Those will be in the form of pandas DataFrame
        self.set_up_dbs()
        self.get_new_ID(1) # the 1 means this is the a setup - that is - check the file is here etc
        print("class Db initialized")

    ###################################
    # returns to caller the ID it
    # reads from the file, and sets into the file
    # the next ID (+1)
    ###################################
    def get_new_ID(self, mode = 0):
        fh = open('../ID', 'r+')
        cID = int(fh.read())
        fh.seek(0)
        fh.write(str(cID+1)) # increase by 1 for next time
        if mode == 1:
            logger.debug('Starting with ID {}'.format(cID))
        logger.debug('ID is: {}'.format(cID))
        fh.close()
        if mode == 1:
            return -1
        else:
            return cID

    ####################################
    # setting up 4 databases
    # metaprojects: dbm
    # projects    : dbp
    # tasks       : dbt
    # activities  : dba
    ####################################
    def set_up_dbs(self):
        logger.debug('setting up databases')
        # check if the file for the database exists
        #metaproj
        if os.path.isfile('../data/dfm.csv'):
            dfm = pd.read_csv('../data/dfm.csv')
        else:
            dfm = pd.DataFrame()
            dfm.to_csv('../data/dfm.csv')
        # proj
        if os.path.isfile('../data/dfp.csv'):
            dfm = pd.read_csv('../data/dfp.csv')
        else:
            dfm = pd.DataFrame()
            dfm.to_csv('../data/dfp.csv')
        # task
        if os.path.isfile('../data/dft.csv'):
            dfm = pd.read_csv('../data/dft.csv')
        else:
            dfm = pd.DataFrame()
            dfm.to_csv('../data/dft.csv')
        # activity
        if os.path.isfile('../data/dfa.csv'):
            dfm = pd.read_csv('../data/dfa.csv')
        else:
            dfm = pd.DataFrame()
            dfm.to_csv('../data/dfa.csv')







