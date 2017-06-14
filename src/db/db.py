# oeitam

import os.path
import numpy as np
import pandas as pd
import logging
from src import defs
import datetime as dt
import time

logger = logging.getLogger(__name__)


class Db(object):
    def __init__(self):
        # set up or load the databases. Those will be in the form of pandas DataFrame
        # databases table
        self.dfm = None
        self.dfp = None
        self.dft = None
        self.dfa = None

        self.db_table = {'dfm': self.dfm,
                         'dfp': self.dfp,
                         'dft': self.dft,
                         'dfa': self.dfa,
                         }

        self.load_dbs()
        self.get_new_ID(1) # the 1 means this is the a setup - that is - check the file is here etc
        # create the operations_bucket
        self.operation_bucket = { "create project"     : self.create_project,
                                  "create megaproject" : self.create_megaproject,
                                  "create task"        : self.create_task,
                                  }


        logger.debug("class Db initialized")

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
    def load_dbs(self):
        logger.debug('setting up databases')
        # check if the file for the database exists
        # load only if exists
        # otherwise - set to None
        #metaproj
        if os.path.isfile('../data/dfm.csv'):
            self.dfm = pd.read_csv('../data/dfm.csv')
            self.dfm.set_index('ID', inplace=True)
            self.db_table['dfm'] = self.dfm
        else:
            self.dfm = None
        # proj
        if os.path.isfile('../data/dfp.csv'):
            self.dfp = pd.read_csv('../data/dfp.csv')
            self.dfp.set_index('ID', inplace=True)
            self.db_table['dfp'] = self.dfp
        else:
            self.dfp = None
        # task
        if os.path.isfile('../data/dft.csv'):
            self.dft = pd.read_csv('../data/dft.csv')
            self.dft.set_index('ID', inplace=True)
            self.db_table['dft'] = self.dft
        else:
            self.dft = None
        # activity
        if os.path.isfile('../data/dfa.csv'):
            self.dfa = pd.read_csv('../data/dfa.csv')
            self.dfa.set_index('ID', inplace=True)
            self.db_table['dfa'] = self.dfa
        else:
            self.dfa = None

    # add a dataframe to a db
    # if the db does not exist yet, create it
    def add_to_db(self, which_db, df_to_add):
        db_to_add_to = self.db_table[which_db]
        # here I assume that the df_to_add matches the db_to_add_to
        # so I do not do any checking
        if db_to_add_to is None:
            # need to create the data base
            db_to_add_to = pd.DataFrame(df_to_add)
            db_to_add_to.index.name = 'ID'
            if which_db == 'dfm':
                self.dfm = db_to_add_to
                self.db_table[which_db] = self.dfm
            elif which_db == 'dfp':
                self.dfp = db_to_add_to
                self.db_table[which_db] = self.dfp
            elif which_db == 'dft':
                self.dft = db_to_add_to
                self.db_table[which_db] = self.dft
            else:
                self.dfa = db_to_add_to
                self.db_table[which_db] = self.dfa
        else: # here we assume that the databaser alrad has an index 'ID'
            if which_db == 'dfm':
                self.dfm = self.dfm.append(df_to_add)
            if which_db == 'dfp':
                self.dfp = self.dfp.append(df_to_add)
            if which_db == 'dft':
                self.dft = self.dft.append(df_to_add)

        # this return checks for nothing ... just returnning true
        return True

    # save the databases
    def save_databases(self):
        if self.dfm is not None:
            self.dfm.to_csv('../data/dfm.csv')
        if self.dfp is not None:
            self.dfp.to_csv('../data/dfp.csv')
        if self.dft is not None:
            self.dft.to_csv('../data/dft.csv')
        if self.dfa is not None:
            self.dfa.to_csv('../data/dfa.csv')
        return True # blindly for now

    # set the project name for the next transaction
    def set_project_name(self, project_name):
        self.project_name = project_name

    # set the project name for the next transaction
    def set_megaproject_name(self, megaproject_name):
        self.megaproject_name = megaproject_name

    # set the description section of the next transaction
    def set_trans_description(self, trans_description):
        self.trans_description = trans_description

    # set the transaction (create project, create task etc)
    def transaction_is(self,transaction_type):
        self.transaction_type = transaction_type

    # this function tells the db to perform the transaction it was programmed to do
    # it returns the success + information about the transaction
    def do_transaction(self):
        res = self.operation_bucket.get(self.transaction_type, self.had_error)()
        if res:
            res2 = self.save_databases()
            if res2:
                return_string = "Success"
            else:
                return_string = "Had Error"
        else:
            return_string = "Had Error"
        return return_string

    def had_error(self):
        logger.debug("in had_error. Huston - we have a problem!")
        return False

    # transactions functions
    def create_project(self):
        # check if project exists
        if self.dfp is not None:
            if (self.project_name) in self.dfp['Name'].values:
                logger.debug("Request to create an already existing project {} {}".format(self.project_name, self.dfp['Name'].values))
                return False
        # check if the mega project exsists
        if self.dfm is not None:
            if self.megaproject_name not in self.dfm['Name'].values:
                logger.debug("Request to create a project in a non existing megaproject {}".format(self.megaproject_name))
                return False

        pID = self.get_new_ID()
        l = [self.project_name, 'Started', self.megaproject_name, self.trans_description]
        ldf = pd.DataFrame(data=[l], index=[pID], columns=defs.dfp_columns)
        logger.debug(ldf.to_string())
        res = self.add_to_db(which_db='dfp', df_to_add=ldf)
        # add the new project name to the list of projects in the mega project
        if res:
            t1 = self.dfm['Name'][self.dfm['Name'] == self.megaproject_name].index
            self.dfm['PROJECTs_List'][t1[0]].append(self.project_name)
        if res:
            return True
        else:
            return False

    def create_megaproject(self):
        # check if project exists
        if self.dfm is not None:
            if (self.megaproject_name) in self.dfm['Name'].values:
                ret = "Request to create an already existing megaproject {}".format(self.megaproject_name)
                logger.debug(ret)
                return False
        # regardless if the this is the first megaproject or not ...
        pID = self.get_new_ID()
        l = [self.megaproject_name, 'On', ['default'], self.trans_description]
        ldf = pd.DataFrame(data=[l], index=[pID], columns=defs.dfm_columns)
        logger.debug(ldf.to_string())
        self.add_to_db(which_db='dfm',df_to_add=ldf)
        return "True"

    # create a task
    # for now - no support for optional
    def create_task(self):
        pID = self.get_new_ID()
        # for optional fields, put in ''
        #'State','Description','Creation_Date','PROJECT',
        # optional from here
        #'Due_Date','Expiration_Date''Location','Context','Reminders','ACTIVITYs',
        #'Sub_TASKs','Parent_TASK',
        l = ['Open', self.trans_description, time.ctime(), self.project_name,
             '','','','','',
             [],[],'']
        ldf = pd.DataFrame(data=[l], index=[pID], columns=defs.dft_columns)
        logger.debug(ldf.to_string())
        self.add_to_db(which_db='dft', df_to_add=ldf)
        return True
