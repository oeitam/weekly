
import os.path
import numpy as np
import pandas as pd
import logging
from src import defs
import datetime as dt
import time
from ast import literal_eval
import math

pd.options.display.max_colwidth = 100 # 50 by defaul
#pd.set_option('colheader_justify', 'left')


logger = logging.getLogger(__name__)

conv = lambda x: str(int(x)) if not math.isnan(x) else 'N/A'

class Db(object):
    def __init__(self):
        # set up or load the databases. Those will be in the form of pandas DataFrame
        # databases table
        self.dfm = None
        self.dfp = None
        self.dft = None
        self.dfa = None

        # start fresh
        self.clean_context()

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
                                  'start activity'     : self.start_activity,
                                  'stop activity'      : self.stop_activity,
                                  'cont activity'      : self.cont_activity,
                                  'halt activity'      : self.halt_activity,
                                  'list id'            : self.list_id,
                                  'list megaproject'   : self.list_glob,
                                  'list project'       : self.list_glob,
                                  'list task'          : self.list_glob,
                                  'list activity'      : self.list_glob,
                                  #'list megaproject'   : self.list_megaproject,
                                  #'list project'       : self.list_project,
                                  #'list task'          : self.list_task,
                                  #'list activity'      : self.list_activity,
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
            self.pID = cID
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
            self.dfm = pd.read_csv('../data/dfm.csv',converters={'PROJECTs_List': literal_eval})
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
            self.dft = pd.read_csv('../data/dft.csv',converters={'ACTIVITYs': literal_eval,'Sub_TASKs': literal_eval})
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

    # the purpose of this function is to clean all the
    # relevant 'self' variables to avoid information
    # form one transaction affecting the other transaction
    def clean_context(self, sec1=True, sec2=True):
        if sec1:
            self.pID                    = -1
            self.use_this_ID_for_ref    = -1
            self.project_name           = 'clean'
            self.megaproject_name       = 'clean'
            self.megaproject_name       = 'clean'
            self.transaction_type       = 'clean'
            self.list_resp              = 'clean'
            self.error_details          = 'clean'
            self.trans_description      = 'clean'
            self.return_message         = 'clean'
            self.keep_context           = False
            self.list_col_name          = 'clean'
            self.list_col_value         = 'clean'
            self.list_col_rel           = 'clean'
        if sec2:
            self.list_resp_row_limit    = 10
            self.list_resp_rows         = -1

    def store_context(self):
        self.last_list_resp_row_limit = 10
        self.last_list_resp_rows = -1

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
                self.db_table[which_db] = self.dfm
            if which_db == 'dfp':
                self.dfp = self.dfp.append(df_to_add)
                self.db_table[which_db] = self.dfp
            if which_db == 'dft':
                self.dft = self.dft.append(df_to_add)
                self.db_table[which_db] = self.dft
            if which_db == 'dfa':
                self.dfa = self.dfa.append(df_to_add)
                self.db_table[which_db] = self.dfa

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
                self.create_return_message(True)
            else:
                self.had_error()
                self.create_return_message(False)
        else:
            self.had_error()
            self.create_return_message(False)
        return True

    def had_error(self):
        logger.debug("in had_error. Huston - we have a problem!")
        return False

    def create_return_message(self, success):
        if 'list ' in self.transaction_type[0:8]:
            if success:
                m = self.list_resp
            else:
                m = "Transaction: {} FAILED with ERROR: {}".format(self.transaction_type, self.error_details)
        elif ( 'stop act' in self.transaction_type
            or 'cont act' in self.transaction_type
            or 'halt act' in self.transaction_type) :
            if success:
                m = "Transaction: {} COMPLETED. Referenced ID is: {}".format(self.transaction_type, self.use_this_ID_for_ref)
            else:
                m = "Transaction: {} FAILED with ERROR: {}".format(self.transaction_type, self.error_details)
        else:
            if success:
                m = "Transaction: {} COMPLETED. New ID is: {}".format(self.transaction_type, self.pID)
            else:
                m = "Transaction: {} FAILED with ERROR: {}".format(self.transaction_type, self.error_details)

        self.return_message = m

    # transactions functions
    ########################
    def create_project(self):
        # check if project exists
        if self.dfp is not None:
            if (self.project_name) in self.dfp['Name'].values:
                logger.debug("Request to create an already existing project {} {}".format(self.project_name, self.dfp['Name'].values))
                #temp return False
        # check if the mega project exsists
        if self.dfm is not None:
            if self.megaproject_name not in self.dfm['Name'].values:
                self.error_details = "Request to create a project in a non existing megaproject {}".format(self.megaproject_name)
                logger.debug(self.error_details)
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
            self.error_details = "Failed to add a new project {} to the database([])".format(self.project_name, self.pID)
            logger.debug(self.error_details)
            return False

    def create_megaproject(self):
        # check if project exists
        if self.dfm is not None:
            if (self.megaproject_name) in self.dfm['Name'].values:
                ret = "Request to create an already existing megaproject {}".format(self.megaproject_name)
                logger.debug(ret)
                #self.error_details = ret
                #temp return False
        # regardless if the this is the first megaproject or not ...
        pID = self.get_new_ID()
        l = [self.megaproject_name, 'On', [], self.trans_description]
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

    # craete an ACTIVITY
    def start_activity(self):
        pID = self.get_new_ID()
        # search for the related task or project
        found_in = 'no where'
        if self.use_this_ID_for_ref in self.dfp.index.values:
            found_in = 'projects'
            couple = ['', self.use_this_ID_for_ref]
        elif self.use_this_ID_for_ref in self.dft.index.values :
            found_in = 'tasks'
            couple = [self.use_this_ID_for_ref, ""]
        else: #found none
            self.error_details = 'ID {} from {} was not found'.format(self.use_this_ID_for_ref, found_in)
            logger.debug(self.error_details)
            return False
        l = ['Started', time.ctime(), self.trans_description,
             ''] + couple
        ldf = pd.DataFrame(data=[l], index=[pID], columns=defs.dfa_columns)
        logger.debug(ldf.to_string())
        self.add_to_db(which_db='dfa', df_to_add=ldf)
        # FOR LATER
        # add this activity to the projets or tasks list
        # for cross reference
        return True

    def stop_activity(self):
        # check for error conditions
        if self.dfa is None :
            self.error_details = 'Requested to stop ACTIVITY {} but no ACTIVITY database exists (dfa)'.format(self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
        if self.use_this_ID_for_ref not in self.dfa.index.values:
            self.error_details = 'Requested to stop ACTIVITY {} but no such ACTIVITY in database at proper state'.format(self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
        # process
        self.dfa.loc[self.use_this_ID_for_ref, 'State'] = 'Ended'
        self.dfa.loc[self.use_this_ID_for_ref, 'End_Time'] = time.ctime()
        return True

    def cont_activity(self):
        # check for error conditions
        if self.dfa is None:
            self.error_details = 'Requested to continue ACTIVITY {} but no ACTIVITY database exists (dfa)'.format(
                self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
        if self.use_this_ID_for_ref not in self.dfa.index.values:
            self.error_details = 'Requested to continue ACTIVITY {} but no such ACTIVITY in database at proper state'.format(self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
        # process
        self.dfa.loc[self.use_this_ID_for_ref, 'State'] = 'Started'
        self.dfa.loc[self.use_this_ID_for_ref, 'End_Time'] = ''
        return True

    def halt_activity(self):
        # check for error conditions
        if self.dfa is None:
            self.error_details = 'Requested to halt ACTIVITY {} but no ACTIVITY database exists (dfa)'.format(
                self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
        if self.use_this_ID_for_ref not in self.dfa.index.values:
            self.error_details = 'Requested to halt ACTIVITY {} but no such ACTIVITY in database at proper state'.format(self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
        # process
        self.dfa.loc[self.use_this_ID_for_ref, 'State'] = 'OnHold'
        return True


    def list_id(self):
        # find the ID
        if self.use_this_ID_for_ref in self.dfm.index.values:
            temp = pd.DataFrame([self.dfm.loc[self.use_this_ID_for_ref]])
            self.list_resp = temp.to_string(na_rep='N/A', float_format=conv, index_names=True, justify='left')
        elif self.use_this_ID_for_ref in self.dfp.index.values:
            temp = pd.DataFrame([self.dfp.loc[self.use_this_ID_for_ref]])
            self.list_resp = temp.to_string(na_rep='N/A', float_format=conv, index_names=True, justify='left')
        elif self.use_this_ID_for_ref in self.dft.index.values:
            temp = pd.DataFrame([self.dft.loc[self.use_this_ID_for_ref]])
            self.list_resp = temp.to_string(na_rep='N/A', float_format=conv, index_names=True, justify='left')
        elif self.use_this_ID_for_ref in self.dfa.index.values:
            temp = pd.DataFrame([self.dfa.loc[self.use_this_ID_for_ref]])
            self.list_resp = temp.to_string(na_rep='N/A', float_format=conv, index_names=True, justify='left')
        else: # did not find it
            self.error_details = 'Requested ID {} to list was not found'.format(self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
        return True

    def list_glob(self):
        # set the right database
        if self.transaction_type == 'list megaproject':
            which_db = 'dfm'
        elif self.transaction_type == 'list project':
            which_db = 'dfp'
        elif self.transaction_type == 'list task':
            which_db = 'dft'
        elif self.transaction_type == 'list activity':
            which_db = 'dfa'
        df = self.db_table[which_db]

        if df is not None:
            if self.list_col_name != 'clean':
                if self.list_col_rel == 'is':
                    df = df[df[self.list_col_name] == self.list_col_value]

            if self.list_resp_rows == -1 : # means this is the first time we handle the specific lsit
                self.list_resp_rows = len(df)
            if self.list_resp_rows == 0 : # meaning-  we finished showing all
                self.list_resp = "No more data to show"
                return True
            t1 = self.list_resp_rows
            t2 = max(self.list_resp_rows - self.list_resp_row_limit ,0)
            #if self.list_col_name != 'clean':
            #    if self.list_col_rel == 'is':
            #        self.list_resp = df[df[self.list_col_name] == self.list_col_value][t2:t1].to_string(
            #            # na_rep='N/A', float_format=conv, index_names=True, justify='left')
            #            columns=defs.columns_to_print_table[which_db],
            #            na_rep='N/A', float_format=conv, index_names=True, justify='left')
            #else:
            self.list_resp = df[t2:t1].to_string(#na_rep='N/A', float_format=conv, index_names=True, justify='left')
                columns=defs.columns_to_print_table[which_db],
                na_rep='N/A', float_format=conv, index_names=True, justify='left')
            self.list_resp = "Showing items {} to {}:\n".format(t2,t1) + self.list_resp
            self.list_resp_rows = t2
        else:  # did not find it
            self.error_details = 'No megaprojects to list'
            logger.debug(self.error_details)
            return False
        return True




    #########################################################################################
    # def list_megaproject(self):
    #     if self.dfm is not None:
    #         if self.list_resp_rows == -1 : # means this is the first time we handle the specific lsit
    #             self.list_resp_rows = len(self.dfm)
    #         if self.list_resp_rows == 0 : # meaning-  we finished showing all
    #             self.list_resp = "No more data to show"
    #             return True
    #         t1 = self.list_resp_rows
    #         t2 = max(self.list_resp_rows - self.list_resp_row_limit ,0)
    #         self.list_resp = self.dfm[t2:t1].to_string(#na_rep='N/A', float_format=conv, index_names=True, justify='left')
    #             columns=defs.dfm_columns_to_print,
    #             na_rep='N/A', float_format=conv, index_names=True, justify='left')
    #         self.list_resp = "Showing items {} to {}:".format(t2,t1) + self.list_resp
    #         self.list_resp_rows = t2
    #     else:  # did not find it
    #         self.error_details = 'No megaprojects to list'
    #         logger.debug(self.error_details)
    #         return False
    #     return True
    #
    # def list_project(self):
    #     if self.dfp is not None:
    #         self.list_resp = self.dfp.to_string(#na_rep='N/A', float_format=conv, index_names=True, justify='left')
    #             columns=defs.dfp_columns_to_print,
    #             na_rep='N/A', float_format=conv, index_names=True, justify='left')
    #     else:  # did not find it
    #         self.error_details = 'No projects to list'
    #         logger.debug(self.error_details)
    #         return False
    #     return True
    #
    # def list_task(self):
    #     if self.dft is not None:
    #         self.list_resp = self.dft.to_string(
    #             # na_rep='N/A', float_format=conv, index_names=True, justify='left')
    #             columns=defs.dft_columns_to_print,
    #             na_rep='N/A', float_format=conv, index_names=True, justify='left')
    #     else:  # did not find it
    #         self.error_details = 'No tasks to list'
    #         logger.debug(self.error_details)
    #         return False
    #     return True
    #
    # def list_activity(self):
    #     if self.dfa is not None:
    #         self.list_resp = self.dfa.to_string(
    #             # na_rep='N/A', float_format=conv, index_names=True, justify='left')
    #             columns=defs.dfa_columns_to_print,
    #             na_rep='N/A', float_format=conv, index_names=True, justify='left')
    #     else:  # did not find it
    #         self.error_details = 'No activities to list'
    #         logger.debug(self.error_details)
    #         return False
    #     return True
