
import os.path
import numpy as np
import os
import pandas as pd
import logging
from src import defs
from test import test_defs
import shutil

from datetime import datetime, date, time, timedelta
from ast import literal_eval
import math

one_week = timedelta(days=7)

pd.options.display.max_colwidth = 100 # 50 by defaul
#pd.set_option('colheader_justify', 'left')

# this is an addition from home on local
# and this is from work local

def myconv(x):
    if x is not '':
        return str(int(float(x)))

def date_conv(ds):
    ds1,ds2,ds3 = ds.partition('.')
    st1 = defs.days_of_week.get(ds3, None)
    if not st1: # meaning - None
        raise ValueError
    r = datetime.strptime(ds1 + st1, "%yww%W-%w")
    if ds3 == 'Sun':
        r = r - one_week
    return(r)

def mycnv2(x,other_df,str_to_cmp):
    if type(x) == str and x != '':
        return other_df.loc[int(x)]['Name'] == str_to_cmp
    else:
        return False


def search_in_df(x,list_to_fill,pat):
    for i in x:
        if pat in str(i):
            list_to_fill.append(int(x.name))
            return True
    return False

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
                                  'stop something'     : self.stop_something,
                                  'cont something'     : self.cont_something,
                                  'halt something'     : self.halt_something,
                                  'list id'            : self.list_id,
                                  'list megaproject'   : self.list_glob,
                                  'list project'       : self.list_glob,
                                  'list task'          : self.list_glob,
                                  'list activity'      : self.list_glob,
                                  'list for'           : self.list_glob,
                                  'list search'        : self.list_search,
                                  'help'               : self.help_message,
                                  'delete id'          : self.delete_id,
                                  'online'             : self.online_check,
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
        path_to_ID_file = defs.data_loc + '\\ID'
        if not os.path.isfile(path_to_ID_file):
            fb = open(path_to_ID_file,'w')
            fb.write('100')
            fb.close()
        #print(path_to_ID_file)
        fh = open(path_to_ID_file, 'r+')
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

        ###################################
        # returns to caller the ID it
        # reads from the file,
        # does not advance the ID !!
        ###################################
    def get_current_ID(self):
        path_to_ID_file = defs.data_loc + '\\ID'
        if not os.path.isfile(path_to_ID_file):
            fb = open(path_to_ID_file,'w')
            fb.write('100')
            fb.close()
        fh = open(path_to_ID_file, 'r')
        cID = int(fh.read())
        logger.debug('current ID is: {}'.format(cID))
        fh.close()
        return cID

    # expecting date (like date.today())
    def get_time_str(self, d = None):
        #d = date.today()
        if d is None:
            d = date.today()
        d = d - test_defs.debug_delta
        tt = d.timetuple()
        y = str(tt[0])[2:4]
        if tt[6] == 6:  # if a sunday, need to advance ww by one
            ww = str(d.isocalendar()[1] + 1).zfill(2)
        else:
            ww = str(d.isocalendar()[1]).zfill(2)
        wd = d.strftime('%a')
        a = y + "ww" + ww + "." + wd
        return a







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
        if os.path.isfile(defs.data_loc + '/dfm.csv'):
            self.dfm = pd.read_csv(defs.data_loc + '/dfm.csv',converters={'PROJECTs_List': literal_eval})
            self.dfm.set_index('ID', inplace=True)
            self.db_table['dfm'] = self.dfm
        else:
            self.dfm = None
        # proj
        if os.path.isfile(defs.data_loc + '/dfp.csv'):
            self.dfp = pd.read_csv(defs.data_loc + '/dfp.csv')
            self.dfp.set_index('ID', inplace=True)
            self.db_table['dfp'] = self.dfp
        else:
            self.dfp = None
        # task
        if os.path.isfile(defs.data_loc + '/dft.csv'):
            self.dft = pd.read_csv(defs.data_loc + '/dft.csv',converters={'ACTIVITYs': literal_eval,'Sub_TASKs': literal_eval})
            self.dft.set_index('ID', inplace=True)
            self.db_table['dft'] = self.dft
        else:
            self.dft = None
        # activity
        if os.path.isfile(defs.data_loc + '/dfa.csv'):
            self.dfa = pd.read_csv(defs.data_loc + '/dfa.csv',converters={'TASK': myconv,'PROJECT': myconv})
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
            self.return_message_ext1    = 'clean'
            self.keep_context           = False
            self.list_col_name          = 'clean'
            self.list_col_value         = 'clean'
            self.list_col_rel           = 'clean'
            self.list_col_bot           = 'clean'
            self.list_col_top           = 'clean'
            self.list_what_for          = 'clean'
            self.list_for_what          = 'clean'
            self.list_for_val           = 'clean'
            self.list_attr              = 'clean'
            self.list_ww                = 'clean'
        if sec2:
            self.list_resp_row_limit    = 15
            self.list_resp_rows         = -1

    def store_context(self):
        self.last_list_resp_row_limit = 15
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
            self.dfm.to_csv(defs.data_loc + '\dfm.csv')
        if self.dfp is not None:
            self.dfp.to_csv(defs.data_loc + '\dfp.csv')
        if self.dft is not None:
            self.dft.to_csv(defs.data_loc + '\dft.csv')
        if self.dfa is not None:
            self.dfa.to_csv(defs.data_loc + '\dfa.csv')

        # copy the files over to dropbox area
        #if os.path.isfile(defs.data_loc + '/dfm.csv'):
        #    if os.path.isfile(defs.data_loc_dropbox + '/dfm.csv'):
        #        os.remove(defs.data_loc_dropbox + '/dfm.csv')
        #    shutil.copy2(defs.data_loc + '/dfm.csv', defs.data_loc_dropbox)

        return True # blindly for now

    # set the project name for the next transaction
    def set_project_name(self, project_name):
        had_error = 0
        if project_name.isdigit():
            # look for the project 'verbal' name
            if self.dfp is not None:
                if int(project_name) in self.dfp.index:
                    self.project_name = self.dfp.loc[int(project_name)].Name
                else:
                    had_error = 1
            else:
                had_error = 1
        else:
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
        elif ( 'stop some' in self.transaction_type
            or 'cont some' in self.transaction_type
            or 'halt some' in self.transaction_type) :
            if success:
                m = "Transaction: {} COMPLETED. Referenced ID is: {}".format(self.transaction_type, self.use_this_ID_for_ref)
            else:
                m = "Transaction: {} FAILED with ERROR: {}".format(self.transaction_type, self.error_details)
        elif (self.transaction_type == 'help'):
            m = defs.help_message
        else:
            if success:
                m = "Transaction: {} COMPLETED. New ID is: {}".format(self.transaction_type, self.pID)
                if self.return_message_ext1 != 'clean':
                    m += self.return_message_ext1
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
        ldf.index.name = 'ID'
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
        ldf.index.name = 'ID'
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
        l = ['Open', self.trans_description, self.get_time_str(date.today()), self.project_name,
             '','','','','',
             [],[],'']
        ldf = pd.DataFrame(data=[l], index=[pID], columns=defs.dft_columns)
        ldf.index.name = 'ID'
        logger.debug(ldf.to_string())
        self.add_to_db(which_db='dft', df_to_add=ldf)
        return True

    # craete an ACTIVITY
    def start_activity(self):
        pID = self.get_new_ID()
        # search for the related task or project
        found_in = 'no where'
        if self.dfp is not None and self.use_this_ID_for_ref in self.dfp.index.values:
            found_in = 'projects'
            couple = ['', str(int(self.use_this_ID_for_ref))]
        elif self.dft is not None and self.use_this_ID_for_ref in self.dft.index.values :
            found_in = 'tasks'
            couple = [str(int(self.use_this_ID_for_ref)), ""]
        elif self.use_this_ID_for_ref == 0: # indicating - ci or co (or non related activity)
            found_in = 'orphan activity'
            couple = ['','']
        else: #found none
            self.error_details = 'ID {} from {} was not found'.format(self.use_this_ID_for_ref, found_in)
            logger.debug(self.error_details)
            return False
        l = ['Started', self.get_time_str(date.today()), self.trans_description,
             ''] + couple
        ldf = pd.DataFrame(data=[l], index=[pID], columns=defs.dfa_columns)
        ldf.index.name = 'ID'
        logger.debug(ldf.to_string())
        self.add_to_db(which_db='dfa', df_to_add=ldf)
        # FOR LATER
        # add this activity to the projets or tasks list
        # for cross reference
        return True

    def cont_something(self):
        # handle activity, and then task and then project
        state = 'idle' # helps understand status
        # activity
        if self.dfa is not None:
            state = 'found db'
            if self.use_this_ID_for_ref in self.dfa.index.values:
                state = 'id in db'
                # process
                self.dfa.loc[self.use_this_ID_for_ref, 'State'] = 'Started'
                self.dfa.loc[self.use_this_ID_for_ref, 'End_Time'] = ''
        # task
        if (self.dft is not None) and (state != 'id in db'):
            state = 'found db'
            if self.use_this_ID_for_ref in self.dft.index.values:
                state = 'id in db'
                # process
                self.dft.loc[self.use_this_ID_for_ref, 'State'] = 'Open'
                #self.dft.loc[self.use_this_ID_for_ref, 'End_Time'] = ''
        # project
        if (self.dfp is not None) and (state != 'id in db'):
            state = 'found db'
            if self.use_this_ID_for_ref in self.dfp.index.values:
                state = 'id in db'
                # process
                self.dfp.loc[self.use_this_ID_for_ref, 'State'] = 'Started'
                #self.dft.loc[self.use_this_ID_for_ref, 'End_Time'] = ''

        if state != 'id in db':
            self.error_details = 'Requested to continue ACTIVITY or TASK or PROJECT {} failed (probably incorrect ID)'\
                .format(self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
        return True

    def halt_something(self):
        # handle activity, and then task and then project
        state = 'idle' # helps understand status
        # activity
        if self.dfa is not None:
            state = 'found db'
            if self.use_this_ID_for_ref in self.dfa.index.values:
                state = 'id in db'
                # process
                self.dfa.loc[self.use_this_ID_for_ref, 'State'] = 'OnHold'
                #self.dfa.loc[self.use_this_ID_for_ref, 'End_Time'] = ''
        # task
        if (self.dft is not None) and (state != 'id in db'):
            state = 'found db'
            if self.use_this_ID_for_ref in self.dft.index.values:
                state = 'id in db'
                # process
                self.dft.loc[self.use_this_ID_for_ref, 'State'] = 'OnHold'
                #self.dft.loc[self.use_this_ID_for_ref, 'End_Time'] = ''
        # project
        if (self.dfp is not None) and (state != 'id in db'):
            state = 'found db'
            if self.use_this_ID_for_ref in self.dfp.index.values:
                state = 'id in db'
                # process
                self.dfp.loc[self.use_this_ID_for_ref, 'State'] = 'OnHold'
                #self.dft.loc[self.use_this_ID_for_ref, 'End_Time'] = ''

        if state != 'id in db':
            self.error_details = 'Requested to halt ACTIVITY or TASK or PROJECT {} failed (probably incorrect ID)'\
                .format(self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
        return True

    def stop_something(self):
        # handle activity, and then task and then project
        state = 'idle' # helps understand status
        # activity
        if self.dfa is not None:
            state = 'found db'
            if self.use_this_ID_for_ref in self.dfa.index.values:
                state = 'id in db'
                # process
                self.dfa.loc[self.use_this_ID_for_ref, 'State'] = 'Ended'
                #self.dfa.loc[self.use_this_ID_for_ref, 'End_Time'] = ''
        # task
        if (self.dft is not None) and (state != 'id in db'):
            state = 'found db'
            if self.use_this_ID_for_ref in self.dft.index.values:
                state = 'id in db'
                # process
                self.dft.loc[self.use_this_ID_for_ref, 'State'] = 'Closed'
                #self.dft.loc[self.use_this_ID_for_ref, 'End_Time'] = ''
        # project
        if (self.dfp is not None) and (state != 'id in db'):
            state = 'found db'
            if self.use_this_ID_for_ref in self.dfp.index.values:
                state = 'id in db'
                # process
                self.dfp.loc[self.use_this_ID_for_ref, 'State'] = 'Ended'
                #self.dft.loc[self.use_this_ID_for_ref, 'End_Time'] = ''

        if state != 'id in db':
            self.error_details = 'Requested to stop ACTIVITY or TASK or PROJECT {} failed (probably incorrect ID)'\
                .format(self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
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
        # check if listing attributes
        if self.list_attr != 'clean':
            self.list_attributes()
            return True
        # set the right database
        if self.transaction_type == 'list megaproject':
            which_db = 'dfm'
        elif self.transaction_type == 'list project':
            which_db = 'dfp'
        elif self.transaction_type == 'list task':
            which_db = 'dft'
        elif self.transaction_type == 'list activity':
            which_db = 'dfa'
        elif self.transaction_type == 'list for' :
            if self.list_what_for == 'megaproject':
                which_db = 'dfm'
            elif self.list_what_for == 'project':
                which_db = 'dfp'
            elif self.list_what_for == 'task':
                which_db = 'dft'
            elif self.list_what_for == 'activity':
                which_db = 'dfa'
            else:
                which_db = 'dfm'  # stam
        else:
            which_db = 'dfm' # stam
        df = self.db_table[which_db]

        if df is not None:
            if self.list_col_name != 'clean':
                if self.list_col_rel == 'is':
                    df = df[df[self.list_col_name] == self.list_col_value]
                elif self.list_col_rel == 'inc':
                    df = df[df[self.list_col_name].str.contains(self.list_col_value)]
                if self.list_col_rel == 'not':
                        df = df[df[self.list_col_name] != self.list_col_value]
                elif self.list_col_rel == 'ninc':
                    df = df[df[self.list_col_name].str.contains(self.list_col_value)==False]
                elif self.list_col_rel == 'irange':
                    if self.list_col_name == 'ID': # handling ID values
                        if self.list_col_bot.isdigit() and self.list_col_top.isdigit():    #val -> val
                            df = df.loc[int(self.list_col_bot):int(self.list_col_top)]
                        elif self.list_col_bot.isdigit() and self.list_col_top == 'top':   #val -> top
                            df = df.loc[int(self.list_col_bot):]
                        elif self.list_col_bot == 'bot' and self.list_col_top.isdigit():   #bot -> val
                            df = df.loc[:int(self.list_col_top)]
                        elif self.list_col_bot == 'bot' and self.list_col_top == 'top':   #bot -> top
                            pass # actually - it is simply all
                elif self.list_col_rel == 'drange': #handling of range of dates
                    if self.list_col_bot != 'bot' and self.list_col_top != 'top':  # val -> val
                        df1 = df[df[self.list_col_name].apply(date_conv) >= date_conv(self.list_col_bot)].copy()
                        df2 = df[df[self.list_col_name].apply(date_conv) <= date_conv(self.list_col_top)].copy()
                        df = pd.merge(df1,df2)
                    elif self.list_col_bot != 'bot' and self.list_col_top == 'top':  # val -> top
                        df = df[df[self.list_col_name].apply(date_conv) >= date_conv(self.list_col_bot)]
                    elif self.list_col_bot == 'bot' and self.list_col_top != 'top':  # bot -> val
                        df = df[df[self.list_col_name].apply(date_conv) <= date_conv(self.list_col_top)]
                    elif self.list_col_bot != 'bot' and self.list_col_top == 'top':  # bot -> top
                        pass
                else:
                    self.had_error()
            elif self.transaction_type == 'list for':
                df = self.list_for()
            elif self.list_ww != 'clean':
                df = df[df['Start_Date'].str.contains(self.list_ww)]

            if self.list_resp_rows == -1 : # means this is the first time we handle the specific lsit
                self.list_resp_rows = len(df)
            if self.list_resp_rows == 0 : # meaning-  we finished showing all
                self.list_resp = "No more data to show"
                return True
            t1 = self.list_resp_rows
            t2 = max(self.list_resp_rows - self.list_resp_row_limit ,0)
            self.list_resp = self.df_to_list_resp(df[t2:t1], which_db)
            self.list_resp = "Showing items {} to {}:\n".format(t2+1,max(t1-1,0)) + self.list_resp
            self.list_resp_rows = t2
        else:  # did not find it
            self.error_details = 'No megaprojects to list'
            logger.debug(self.error_details)
            return False
        return True

    def df_to_list_resp(self, df, which_db):
        s = df.to_string(
                columns=defs.columns_to_print_table[which_db],
                na_rep='N/A', float_format=conv, index_names=True, justify='left')
        s = s + '\n'
        return s

    # process for the list for command, and return a df that corresponds to the search
    def list_for(self):
        if self.list_what_for == 'megaproject' and self.list_for_what == 'project':
            df = self.dfm[self.dfm['PROJECTs_List'].apply(lambda x: self.list_for_val in x)]
        elif self.list_what_for == 'project' and self.list_for_what == 'megaproject':
            df = self.dfp[self.dfp['MEGAPROJECT'] == self.list_for_val]
        elif self.list_what_for == 'task' and self.list_for_what == 'project':
            df = self.dft[self.dft['PROJECT'] == self.list_for_val]
        elif self.list_what_for == 'activity' and self.list_for_what == 'project':
            df = self.dfa[self.dfa['PROJECT'].apply(mycnv2,args=(self.dfp,self.list_for_val))]
        elif self.list_what_for == 'activity' and self.list_for_what == 'task':
            if not self.list_for_val.isdigit():
                self.had_error()
            df = self.dfa[self.dfa['TASK'] == self.list_for_val]
        return df

    # print attributes
    def list_attributes(self):
        if self.list_attr == 'columns':
            s1,s2,wtp = self.transaction_type.partition(' ')
            ltp = defs.all_col[wtp]
            self.list_resp = "Showing columns for {}s:\n".format(wtp)
            for i in ltp:
                self.list_resp += i + '\n'
            #
        elif self.list_attr == 'states':
            s1, s2, wtp = self.transaction_type.partition(' ')
            dtp = defs.all_stat[wtp]
            self.list_resp = "Showing states for {}s:\n".format(wtp)
            for i in dtp.keys():
                self.list_resp += ("{:9}".format(i) + " : " + dtp[i] + '\n')


    # global search
    # the search for value is in self.transaction_description
    def list_search(self):
        self.list_resp = 'Searching for {}:\n'.format(self.trans_description)
        for df_name in ['dfm', 'dfp', 'dft', 'dfa']:
            self.list_resp += "\nResults from {}\n".format(defs.db_names[df_name])
            df = self.db_table[df_name]
            l = []
            df.apply(search_in_df, axis=1, args = (l,self.trans_description.lstrip()))
            if len(l) == 0: # nothing found
                self.list_resp += 'well ... nothing found here\n'
            else:
                df = df.loc[l]
                self.list_resp += self.df_to_list_resp(df, df_name)
        return True

    def delete_id(self):
        for df_name in ['dft', 'dfa']:
            df = self.db_table[df_name]
            if self.use_this_ID_for_ref in df.index :
                logger.debug("found the ID in index of {}".format(df_name))
                df.drop(self.use_this_ID_for_ref, inplace = True)
                return True
        return False

    def help_message(self):
        pass
        return True


    def online_check(self):
        # example
        # '{:15} {:5} {:5} {:10}\n'.format('Megaproject','db', 'is', 'online')
        self.return_message_ext1 = '\nOnline Status:\n'
        if self.dfm is not None:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8}\n'.format('Megaproject', 'db', 'is', 'online')
        else:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8}\n'.format('Megaproject', 'db', 'is', 'None')
        if self.dfp is not None:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8}\n'.format('Project', 'db', 'is', 'online')
        else:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8}\n'.format('Project', 'db', 'is', 'None')
        if self.dft is not None:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8}\n'.format('Task', 'db', 'is', 'online')
        else:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8}\n'.format('Task', 'db', 'is', 'None')
        if self.dfa is not None:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8}\n'.format('Activity', 'db', 'is', 'online')
        else:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8}\n'.format('Activity', 'db', 'is', 'None')
        cid = self.get_current_ID()
        lstr = "The ID in file is: {}\n".format(cid)
        self.return_message_ext1     += lstr
        return True




