
import os.path
#import numpy as np
import os
import pandas as pd
import logging
import re

from src import defs
from test import test_defs
from shutil import move,copyfile
from terminaltables import AsciiTable
from textwrap import wrap

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


def date_conv_max_date(ds):
    if isinstance(ds, str) :
        ds1,ds2,ds3 = ds.partition('.')
        st1 = defs.days_of_week.get(ds3, None)
        if not st1: # meaning - None
            raise ValueError
        r = datetime.strptime(ds1 + st1, "%yww%W-%w")
        if ds3 == 'Sun':
            r = r - one_week
        return(r)
    else:
        return defs.future


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

def if_list_find_item(item, tag):
    if type(item) == list:
        if tag in item:
            return True
    return False

def if_list_and_not_empty(item):
    if type(item) == list:
        if len(item) > 0:
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

        # timedelta
        self.tdelta = timedelta(days=0)

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
                                  'sleep something'    : self.sleep_something,
                                  'list id'            : self.list_id,
                                  'list megaproject'   : self.list_glob,
                                  'list project'       : self.list_glob,
                                  'list task'          : self.list_glob,
                                  'list activity'      : self.list_glob,
                                  'list for'           : self.list_glob,
                                  'list search'        : self.list_search,
                                  'list wakeup'        : self.list_wakeup,
                                  'help'               : self.help_message,
                                  'delete id'          : self.delete_id,
                                  'online'             : self.online_check,
                                  'create list'        : self.create_list,
                                  'move list'          : self.move_items,
                                  'move task'          : self.move_items,
                                  'move activity'      : self.move_items,
                                  'move item'          : self.move_items,
                                  'set param'          : self.set_param,
                                  'list parameter'     : self.list_parameter,
                                  'list shortcut'      : self.list_shortcut,
                                  'create shortcut'    : self.create_shortcut,
                                  'delete shortcut'    : self.delete_shortcut,
                                  'tag something'      : self.tagging,
                                  'untag something'    : self.tagging,
                                  'tag project'        : self.tagging_project,
                                  'untag project'      : self.tagging_project,
                                  'list tag'           : self.list_tag,
                                  'tag list'           : self.tag_list,
                                  'list list'          : self.list_list,
                                  'timedelta'          : self.tdelta_func,
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
    def get_time_str(self, d = None, timedel = None):
        #d = date.today()
        if d is None:
            d = date.today()
        if timedel :
            d = d + timedel
        d = d - self.tdelta # if timedelta exists, use it
        tt = d.timetuple()
        #y = str(tt[0])[2:4]
        if tt[6] == 6:  # if a sunday, need to advance ww by one
        #    ww = str(d.isocalendar()[1] + 1).zfill(2)
            ww = (d + timedelta(days=1)).strftime("%V")
            y  = (d + timedelta(days=1)).strftime("%y")
        else:
        #    ww = str(d.isocalendar()[1]).zfill(2)
            ww = d.strftime("%V")
            y  = d.strftime("%y")

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
            self.dfm = pd.read_csv(defs.data_loc + '/dfm.csv',\
                           converters={'PROJECTs_List': literal_eval})
            self.dfm.set_index('ID', inplace=True)
            self.db_table['dfm'] = self.dfm
        else:
            self.dfm = None
        # proj
        if os.path.isfile(defs.data_loc + '/dfp.csv'):
            self.dfp = pd.read_csv(defs.data_loc + '/dfp.csv',\
                           converters={'Tag': literal_eval})
            self.dfp.set_index('ID', inplace=True)
            self.db_table['dfp'] = self.dfp
        else:
            self.dfp = None
        # task
        if os.path.isfile(defs.data_loc + '/dft.csv'):
            self.dft = pd.read_csv(defs.data_loc + '/dft.csv',\
                           converters={'ACTIVITYs': literal_eval,'Sub_TASKs': literal_eval,'Tag': literal_eval})
            self.dft.set_index('ID', inplace=True)
            self.db_table['dft'] = self.dft
        else:
            self.dft = None
        # activity
        if os.path.isfile(defs.data_loc + '/dfa.csv'):
            self.dfa = pd.read_csv(defs.data_loc + '/dfa.csv',\
                           converters={'TASK': myconv,'PROJECT': myconv, 'Tag': literal_eval})
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
            self.state_to_list          = 'clean'
            self.wakeup_time            = 'clean'
            self.help_search            = 'clean'
            self.move_from              = 'clean'
            self.move_to                = 'clean'
            self.param_to_set           = 'clean'
            self.value_to_set           = 'clean'
            self.shortcut_to_delete     = 'clean'
            self.tag                    = 'clean'
            self.item_to_tag_or_untag   = 'clean'
            self.tdelta_param           = 'clean'
            if hasattr(defs,'list_resp_row_limit'):
                self.list_resp_row_limit = defs.list_resp_row_limit
            else:
                self.list_resp_row_limit    = 15
            self.list_resp_rows         = -1
        if sec2:
            self.items_list             = ['clean']

    def store_context(self):
        if hasattr(defs, 'list_resp_row_limit'):
            self.list_resp_row_limit = defs.list_resp_row_limit
        else:
            self.list_resp_row_limit = 15
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

    def find_in_which_db(self,id):
        # search the id in all databases, and returns the one that has this id:
        # 'dfm', 'dfp', 'dft', 'dfa', 'nowhere'
        if id in list(self.dfm.index.values):
            return 'dfm'
        elif id in list(self.dfp.index.values):
            return 'dfp'
        elif id in list(self.dft.index.values):
            return 'dft'
        elif id in list(self.dfa.index.values):
            return 'dfa'
        else:
            return 'nowhere'


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
        if project_name.isdigit():
            # look for the project 'verbal' name
            if self.dfp is not None:
                if int(project_name) in self.dfp.index:
                    self.project_name = self.dfp.loc[int(project_name)].Name
                else:
                    self.had_error('Cannot find project {}\n'.format(project_name))
            else:
                self.had_error('Project database does not exist.\n')
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
                if self.error_details == 'clean':
                    self.had_error()
                self.create_return_message(False)
        else:
            if self.error_details == 'clean':
                self.had_error()
            self.create_return_message(False)
        return True

    def had_error(self,err_text=''):
        logger.debug("in had_error. Huston - we have a problem!")
        self.error_details = err_text
        return False

    def create_return_message(self, success):
        if 'list ' in self.transaction_type[0:8]:
            if success:
                m = self.list_resp
            else:
                m = "Transaction: {} FAILED with ERROR:\n {}".format(self.transaction_type, self.error_details)
        elif ( 'stop some' in self.transaction_type
            or 'cont some' in self.transaction_type
            or 'sleep some' in self.transaction_type
            or 'halt some' in self.transaction_type) :
            if success:
                m = "Transaction: {} COMPLETED. Referenced ID is: {}".format(self.transaction_type, self.use_this_ID_for_ref)
            else:
                m = "Transaction: {} FAILED with ERROR:\n {}".format(self.transaction_type, self.error_details)
        elif (self.transaction_type == 'help'):
            if self.help_search != 'clean':
                l1 = defs.help_message.split('\n')
                l2 = [k for k in l1 if self.help_search in k]
                if len(l2) == 0 :
                    m = "no help message with specified string"
                else:
                    m = "\n".join(l2)
            else:
                m = defs.help_message
        else:
            if success:
                m = "Transaction: {} COMPLETED. New ID is: {}".format(self.transaction_type, self.pID)
                if self.return_message_ext1 != 'clean':
                    m += self.return_message_ext1
            else:
                m = "Transaction: {} FAILED with ERROR:\n {}".format(self.transaction_type, self.error_details)

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

        if self.tag != 'clean': # we have a tag
            tag = [self.tag]
        else:
            tag = []

        l = [self.project_name, 'Started', self.megaproject_name, self.trans_description,tag]
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
        return True

    # create a task
    # for now - no support for optional
    def create_task(self):
        pID = self.get_new_ID()

        if self.tag != 'clean': # we have a tag
            tag = [self.tag]
        else:
            tag = []

        l = ['Open', self.trans_description, self.get_time_str(date.today()),
             self.project_name,tag,
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
        found_in = 'did not look yet ...'
        # search for the related task or project
        # if the use_this_ID_for_ref was actually given as a project name
        if not self.use_this_ID_for_ref.isdigit() : # it is not just digits
            num = int(self.dfp.index[self.dfp['Name'] == self.use_this_ID_for_ref].tolist()[0])
            if num is not None:
                self.use_this_ID_for_ref = num
                couple = ['', str(int(self.use_this_ID_for_ref))]
                found_in = 'projects'
            else:
                return False
        elif ((self.dfp is not None) and (int(self.use_this_ID_for_ref) in list(self.dfp.index.values))):
            couple = ['', str(int(self.use_this_ID_for_ref))]
            found_in = 'projects'
        elif ((self.dft is not None) and (int(self.use_this_ID_for_ref) in list(self.dft.index.values))) :
            couple = [str(int(self.use_this_ID_for_ref)), ""]
            found_in = 'tasks'
        elif self.use_this_ID_for_ref == 0: # indicating - ci or co (or non related activity)
            couple = ['','']
            found_in = 'not found'
        else: #found none
            self.error_details = 'ID {} from {} was not found'.format(self.use_this_ID_for_ref, found_in)
            logger.debug(self.error_details)
            return False

        if self.tag != 'clean': # we have a tag
            tag = [self.tag]
        else:
            tag = []

        l = ['Started', self.get_time_str(date.today()), self.trans_description,tag,
             '', ''] + couple
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
            self.error_details = 'Request to halt ACTIVITY or TASK or PROJECT {} failed (probably incorrect ID)'\
                .format(self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
        return True

    def sleep_something(self):
        # find the wakeup time
        if self.wakeup_time != 'clean':
            m0 = re.match('(\d\d)ww(\d\d)$', self.wakeup_time)
            if m0 :
                self.wakeup_time += ".Sun"
            m1 = re.match('(\d\d)ww(\d\d)\.[a-zA-Z]{3}', self.wakeup_time)
            if not m1 : # if no match, need to convert to work week
                m2 = re.match('\d{8}',self.wakeup_time)
                if m2 : # this is a YYYYMMDD date
                    y = int(self.wakeup_time[0:4])
                    m = int(self.wakeup_time[4:6])
                    d = int(self.wakeup_time[6:8])
                    dt = date(y,m,d)
                    self.wakeup_time = self.get_time_str(dt)
                else: # so this is a "plus XX" type of
                    m3 = re.match('plus (\d+)',self.wakeup_time)
                    if m3 :
                        timedel = timedelta(days=int(m3.groups(1)[0]))
                        self.wakeup_time = self.get_time_str(timedel=timedel)

        # handle activity, and then task
        state = 'idle' # helps understand status
        # activity
        if self.dfa is not None:
            state = 'found db'
            if self.use_this_ID_for_ref in self.dfa.index.values:
                state = 'id in db'
                # process
                self.dfa.loc[self.use_this_ID_for_ref, 'State'] = 'Dormant'
                if self.wakeup_time != 'clean':
                    self.dfa.loc[self.use_this_ID_for_ref, 'Wakeup_Date'] = self.wakeup_time
        # task
        if (self.dft is not None) and (state != 'id in db'):
            state = 'found db'
            if self.use_this_ID_for_ref in self.dft.index.values:
                state = 'id in db'
                # process
                self.dft.loc[self.use_this_ID_for_ref, 'State'] = 'Dormant'
                if self.wakeup_time != 'clean':
                    self.dft.loc[self.use_this_ID_for_ref, 'Wakeup_Date'] = self.wakeup_time

        if state != 'id in db':
            self.error_details = 'Request to sleep ACTIVITY or TASK {} failed (probably incorrect ID)'\
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
            self.error_details = 'Request to stop ACTIVITY or TASK or PROJECT {} failed (probably incorrect ID)'\
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

        # apply the state, if exists, we are listing for
        df = self.apply_state_to_df(df, which_db)

        # apply the tag, if exists, we are listing for
        df = self.apply_tag_to_df(df)

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
                        #df = pd.merge(df1, df2, how='inner',
                        #              left_on=defs.columns_to_print_table[which_db],
                        #              right_on=defs.columns_to_print_table[which_db],
                        #              left_index=True, right_index=True)
                        #df = df1.merge(df2,left_index=True,right_index=True)#.sort_index()
                        df  = pd.merge(df1,df2,on=defs.columns_to_print_table[which_db],left_index=True,right_index=True)
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
                if df is not None:
                    df = self.apply_state_to_df(df, which_db)
                    # apply the tag, if exists, we are listing for
                    df = self.apply_tag_to_df(df)
            elif self.list_ww != 'clean':
                df = df[df['Start_Date'].str.contains(self.list_ww)]
                if df is not None:
                    df = self.apply_state_to_df(df, which_db)
                    # apply the tag, if exists, we are listing for
                    df = self.apply_tag_to_df(df)

            if self.list_resp_rows == -1 : # means this is the first time we handle the specific lsit
                self.list_resp_rows = len(df)
            if self.list_resp_rows == 0 : # meaning-  we finished showing all
                self.list_resp = "No more data to show"
                return True
            t1 = self.list_resp_rows
            t2 = max(self.list_resp_rows - self.list_resp_row_limit ,0)
            resp_title  = "Showing items {} to {}:".format(t2+1,max(t1,0))
            resp_cont_1 = self.df_to_list_resp(df[t2:t1], which_db, resp_title)
            if defs.use_tables == 'no':
                self.list_resp = resp_title + '\n'+ resp_cont_1
            else:
                self.list_resp = resp_cont_1

            self.list_resp_rows = t2
        else:  # did not find it
            self.error_details = 'No SOMETHING to list'
            logger.debug(self.error_details)
            return False
        return True

    def apply_state_to_df(self, df, which_db):
        # apply the state, if exists, we are listing for
        if self.state_to_list != 'all':
            if self.state_to_list == 'clean':
                self.state_to_list = defs.state_open[which_db]
            df = df[df['State'] == self.state_to_list]
        return df

    def apply_tag_to_df(self, df):
        if self.tag == 'clean':
            return df
        if self.tag == 'any-tag-at-all':
            return df
        df = df[df['Tag'].\
                apply(if_list_find_item, args=(self.tag,)) == True]
        return df




    def df_to_list_resp(self, df, which_db, title):
        if defs.use_tables == 'no':
            s = df.to_string(
                columns=defs.columns_to_print_table[which_db],
                na_rep='N/A', float_format=conv, index_names=True, justify='left')
            s = s + '\n'
            return s
        elif defs.use_tables == 'ascii':
            csv_str = df.to_csv(sep='|',
                columns=defs.columns_to_print_table[which_db],
                na_rep='N/A')#, float_format=conv, index_names=True, justify='left')
            l = []
            q = defs.columns_to_print_table[which_db][:]
            q.insert(0, 'ID')
            l.append(q)
            c = 0
            for line in csv_str.splitlines():
                if c == 0:
                    c = c + 1
                    continue
                sl = line.split('|')
                for i in range(0,len(sl)):
                    if len(sl[i]) > defs.max_width:
                        sl[i] = '\n'.join(wrap(sl[i], defs.max_width))
                l.append(sl)
            table_instance = AsciiTable(l,title)
            #table_instance.justify_columns[3] = 'right'
            #table_instance.justify_columns[2] = 'right'

            #print("=====================================")
            #self.myprint(df,which_db,title)
            #print("=====================================")

            return table_instance.table
        else:
            return False

    # process for the list for command, and return a df that corresponds to the search
    def list_for(self):
        df = None
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
        if df is None:
            self.error_details = 'List for unsuccessful'
            self.had_error()
            logger.debug(self.error_details)
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
                self.list_resp += self.df_to_list_resp(df, df_name,'list search results')
        return True

    # print out wakeup tasks and activities
    def list_wakeup(self):
        self.list_resp = 'Searching for TASK and ACTIVITY in Dormant state what Wakeup time is this week or past{}:\n'
        for df_name in ['dft', 'dfa']:
            #self.list_resp += "\nResults from {}\n".format(defs.db_names[df_name])
            title = "Results from {}".format(defs.db_names[df_name])
            df = self.db_table[df_name]
            df1 = df[df['State'] == 'Dormant']
            # calculate end of this week for comparison
            d = date.today()
            ws = d-timedelta(days=d.weekday())
            we = ws + timedelta(days=6)
            we = we + defs.debug_delta
            df2 = df1[df1['Wakeup_Date'].apply(date_conv_max_date) <= we].copy()
            if len(df2) == 0: # nothing found
                self.list_resp += 'well ... nothing found here at {}.\n'.\
                    format(defs.db_names[df_name])
            else:
                # in order to sort, need to convert the Wakeup_Date to numbers
                # and then sort by these numbers
                df2['Wakeup_Date2'] = df2['Wakeup_Date'].apply(date_conv)
                df2.sort_values(by=['Wakeup_Date2'], axis=0, inplace=True)
                self.list_resp += self.df_to_list_resp(df2, df_name,title)
                self.list_resp += '\n\n'
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
        self.return_message_ext1 += '==============\n'
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
        self.return_message_ext1 += '==========================\n'
        # add if developement or production
        self.return_message_ext1 += 'Working environment is {}\n'\
                .format(defs.config['MAIN']['dev_or_prod'])
        # list of wake ups, and add into the return message
        self.return_message_ext1 += '==========================\n'
        self.list_wakeup()
        self.return_message_ext1 += self.list_resp
        self.return_message_ext1 += '==========================\n'
        # timedelta status
        self.return_message_ext1 += 'Timedelta set to {} days.\n'. \
            format(self.tdelta)
        self.return_message_ext1 += '==========================\n'
        return True

    def move_items(self):
        if self.transaction_type == 'move list':
            if len(self.items_list) > 0:
                for item in self.items_list:
                    if item in self.dfa.index:
                        self.dfa.loc[item, 'PROJECT'] = self.move_to
                    elif item in self.dft.index:
                        self.dft.loc[item, 'PROJECT'] = self.move_to
        elif self.transaction_type == 'move item':
            item = self.use_this_ID_for_ref
            if item in self.dfa.index:
                self.dfa.loc[item, 'PROJECT'] = self.move_to
            elif item in self.dft.index:
                self.dft.loc[item, 'PROJECT'] = self.move_to
        elif self.transaction_type == 'move task':
            if self.state_to_list == 'clean':
                self.dft.loc[self.dft['PROJECT'] == self.move_from,'PROJECT']\
                    = self.move_to
            else: # there is a specific state to move
                self.dft.loc[(self.dft['PROJECT'] == self.move_from) \
                             & (self.dft['State'] == self.state_to_list) \
                    , 'PROJECT'] = self.move_to
        elif self.transaction_type == 'move activity':
            self.dfa.loc[self.dfa['PROJECT'] == self.move_from,'PROJECT'] = self.move_to
            if self.state_to_list == 'clean':
                self.dfa.loc[self.dft['PROJECT'] == self.move_from, 'PROJECT'] \
                    = self.move_to
            else:  # there is a specific state to move
                self.dfa.loc[(self.dfa['PROJECT'] == self.move_from) \
                             & (self.dfa['State'] == self.state_to_list) \
                    , 'PROJECT'] = self.move_to
        return True

    def myprint(self, df,which_db,title):
        str1 = df.to_json()
        df1 = pd.read_json(str1)

        csv_str = df1.to_csv(sep='|',
                            columns=defs.columns_to_print_table[which_db],
                            na_rep='N/A')
                            # , float_format=conv, index_names=True, justify='left')
        l = []
        q = defs.columns_to_print_table[which_db][:]
        q.insert(0, 'ID')
        l.append(q)
        c = 0
        for line in csv_str.splitlines():
            if c == 0:
                c = c + 1
                continue
            sl = line.split('|')
            for i in range(0, len(sl)):
                if len(sl[i]) > defs.max_width:
                    sl[i] = '\n'.join(wrap(sl[i], defs.max_width))
            l.append(sl)
        table_instance = AsciiTable(l, title)
        table_instance.justify_columns[2] = 'right'
        print(table_instance.table)

    def create_list(self):
        # the list is already created during parsing, so
        # no need to do anything
        return True

    def set_param(self):
        if hasattr(defs, self.param_to_set):
            if (self.value_to_set.isdigit()):
                self.value_to_set = int(self.value_to_set)
            setattr(defs,self.param_to_set, self.value_to_set)
        else:
            return False
        return True

    def list_parameter(self):
        self.list_resp = "Program Parameters that can be set:\n"
        for par in defs.params_list:
            self.list_resp += "paramter: {} = {}\n"\
                .format(par, eval("defs." + par))
        return True

    def list_shortcut(self):
        defs.config.read(r'C:\weekly.local\weekly.local.cfg')
        self.list_resp = ''
        for sect in defs.config.sections():
            if 'replace_' in sect:
                (a1,a2,a3) = sect.partition("_")
                self.list_resp += "replacement shortcut number {}\n".format(a3)
                self.list_resp += "===================================\n"
                self.list_resp += "substitution type: {}\n".\
                    format(defs.config[sect]['replacement_type'])
                self.list_resp += "substitute this:   {}\n".\
                    format(defs.config[sect]['replace_what'])
                self.list_resp += "with this:         {}\n".\
                    format(defs.config[sect]['replace_with'])
                self.list_resp += "===================================\n\n"
        return True

    def create_shortcut(self):
        # find the number of the next repalcement
        max_replacement_num = 0
        for sect in defs.config.sections():
            if 'replace_' in sect:
                (a1,a2,a3) = sect.partition("_")
                if int(a3) >= max_replacement_num:
                    max_replacement_num = int(a3) +1
        # write to config file, assuming replacement is always 3 long !
        l = eval(self.trans_description)
        f = open(r'C:\weekly.local\weekly.local.cfg', 'a')
        f.write('\n')
        f.write('[replace_{}]\n'.format(max_replacement_num))
        f.write('replacement_type = {}\n'.format(l[0]))
        f.write('replace_what = {}\n'.format(l[1]))
        f.write('replace_with  = {}\n\n'.format(l[2]))
        f.close()
        # reread the config
        defs.config.read(r'C:\weekly.local\weekly.local.cfg')
        return True

    def delete_shortcut(self):
        section = 'replace_'+self.shortcut_to_delete
        res = defs.config.remove_section(section)
        if not res:
            self.had_error('Could not find the requested shortcut - number {}\n'\
                           .format(self.shortcut_to_delete))
            return False
        else:
            f = open(r'C:\weekly.local\weekly.local.cfg', 'w')
            defs.config.write(f)
            f.close()
        # copy_line = True
        # did_delete = False
        # temp_file = r'c:\temp\stamfile.txt'
        # pat = '^\[replace_'+self.shortcut_to_delete+'\]'
        # f = open(temp_file, 'w')
        # with open(r'C:\weekly.local\weekly.local.cfg') as origin_file:
        #     for line in origin_file:
        #         if copy_line :
        #             m = re.match(pat, line)
        #             if m:
        #                 copy_line = False
        #                 did_delete = True
        #             else:
        #                 f.write(line)
        #         else:
        #             n = re.match('\[replace_\d+\]$', line) #check if a new section starts
        #             if n:
        #                 copy_line = True
        #                 #f.write('\n')
        #                 f.write(line)
        #
        # f.close()
        # move(temp_file,r'C:\weekly.local\weekly.local.cfg')
        # if not did_delete: # meaning - did not find the requested shortcut
        #     self.had_error('Could not find the requested shortcut - number {}\n'\
        #                    .format(self.shortcut_to_delete))
        #     return False
        return True

    def tagging(self):
        if self.transaction_type == 'tag something':
            # look for the item and set the tag
            found_in = 'nowhere'
            ref_id = int(self.use_this_ID_for_ref)
            if ((self.dfp is not None) and\
                        (ref_id in list(self.dfp.index.values))):
                found_in = 'project'
                self.dfp.loc[ref_id,'Tag'].append(self.tag)
                item = self.dfp.loc[ref_id,'Name']
            elif ((self.dft is not None) and (ref_id in list(self.dft.index.values))):
                found_in = 'task'
                self.dft.loc[ref_id, 'Tag'].append(self.tag)
                item = ref_id
            elif ((self.dfa is not None) and (ref_id in list(self.dfa.index.values))):
                found_in = 'activity'
                self.dfa.loc[ref_id, 'Tag'].append(self.tag)
                item = ref_id
            self.return_message_ext1 = "\nTag {} was added to {} {}\n". \
                format(self.tag, found_in, item )
        ###
        elif self.transaction_type == 'untag something':
            # look for the item and set the tag
            found_in = 'nowhere'
            ref_id = int(self.use_this_ID_for_ref)
            if ((self.dfp is not None) and \
                        (ref_id in list(self.dfp.index.values))):
                found_in = 'project'
                if self.tag == 'clean':
                    self.dfp.loc[ref_id, 'Tag'].clear()
                else:
                    if self.tag in self.dfp.loc[ref_id, 'Tag']: \
                            self.dfp.loc[ref_id, 'Tag'].remove(self.tag)
                item = self.dfp.loc[ref_id, 'Name']
            elif ((self.dft is not None) and (ref_id in list(self.dft.index.values))):
                found_in = 'task'
                if self.tag == 'clean':
                    self.dft.loc[ref_id, 'Tag'].clear()
                else:
                    if self.tag in self.dft.loc[ref_id, 'Tag']: \
                            self.dft.loc[ref_id, 'Tag'].remove(self.tag)
                item = ref_id
            elif ((self.dfa is not None) and (ref_id in list(self.dfa.index.values))):
                found_in = 'activity'
                if self.tag == 'clean':
                    self.dfa.loc[ref_id, 'Tag'].clear()
                else:
                    if self.tag in self.dfa.loc[ref_id, 'Tag']: \
                            self.dfa.loc[ref_id, 'Tag'].remove(self.tag)
                item = ref_id
            if self.tag == 'clean':
                self.return_message_ext1 = "\nAll tags were removed from {} {}\n". \
                    format(found_in, item)
            else:
                self.return_message_ext1 = "\nTag {} was removed from {} {}\n". \
                    format(self.tag, found_in, item)
        ###

        return True

    def tagging_project(self):
        # find the project
        if ((self.dfp is not None) and \
                    (self.item_to_tag_or_untag in list(self.dfp.Name))):
            if len(self.dfp[self.dfp['Name'] == self.item_to_tag_or_untag]) > 1 :
                self.had_error('Multiple projects named with the specified name {}\n'.\
                               format(self.item_to_tag_or_untag))
                return False
            ref = int(self.dfp.index[self.dfp['Name'] == self.item_to_tag_or_untag].values)
        else:
            self.had_error('Could not find the specified project {}\n'.\
                           format(self.item_to_tag_or_untag))
            return False

        if self.transaction_type == 'tag project':
            self.dfp.loc[ref, 'Tag'].append(self.tag)
        elif self.transaction_type == 'untag project':
            if self.tag != 'clean':
                if self.tag in self.dfp.loc[ref,'Tag']:
                    self.dfp.loc[ref, 'Tag'].remove(self.tag)
                else:
                    self.had_error('Tag {} was not found for the specied project {}.\n'.\
                                   format(self.tag, self.item_to_tag_or_untag))
                    return False
            else: # tag is clean ==> remove all
                self.dfp.loc[ref,'Tag'].clear()

        return True

    def list_tag(self):
        if self.tag == 'clean':
            self.tag = 'any-tag-at-all'
            # search for the tag in project
            df_proj = self.dfp[self.dfp['Tag'].apply(if_list_and_not_empty) == True]
            # search for the tag in project
            df_task = self.dft[self.dft['Tag'].apply(if_list_and_not_empty) == True]
            # search for the tag in project
            df_act  = self.dfa[self.dfa['Tag'].apply(if_list_and_not_empty) == True]
        else: # listing for a certain tag
            # search for the tag in project
            df_proj = self.dfp[self.dfp['Tag'].apply(if_list_find_item, args=(self.tag,)) == True]
            # search for the tag in project
            df_task = self.dft[self.dft['Tag'].apply(if_list_find_item, args=(self.tag,)) == True]
            # search for the tag in project
            df_act  = self.dfa[self.dfa['Tag'].apply(if_list_find_item, args=(self.tag,)) == True]

        # remove clean from the list response
        self.list_resp = ""
        if len(df_proj) > 0:
            str1 = self.df_to_list_resp(df_proj, 'dfp', '*Projects with tag {}*'.\
                                        format(self.tag))
            self.list_resp += str1 # first, removing the 'clean'
            self.list_resp += '\n\n'
        if len(df_task) > 0:
            str2 = self.df_to_list_resp(df_task, 'dft', '*Tasks with tag {}*'.\
                                        format(self.tag))
            self.list_resp += str2
            self.list_resp += '\n\n'
        if len(df_act) > 0:
            str3 = self.df_to_list_resp(df_act, 'dfa', '*Activities with tag {}*'.\
                                        format(self.tag))
            self.list_resp += str3
            self.list_resp += '\n\n'

        if len(self.list_resp) == 0 :
            self.error_details = 'Nothing to list. No such tag found.'
            logger.debug(self.error_details)
            return False

        return True

    def tag_list(self):
        if len(self.items_list) <= 0: #smaller then zero ??
            return False
        else:
            for item in self.items_list:
                if item in self.dfa.index: # activity
                    self.dfa.loc[item, 'Tag'].append(self.tag)
                elif item in self.dft.index: # task
                    self.dft.loc[item, 'Tag'].append(self.tag)
                elif item in self.dfp.index:  # project
                    self.dfp.loc[item, 'Tag'].append(self.tag)
            return True

    def list_list(self):
        if ((self.items_list[0] == 'clean') or (len(self.items_list) == 0))  :
            self.had_error('list of items is empty. Cannot list it.')
            return False
        else:
            self.list_resp = ""
            for item in self.items_list:
                which_db = self.find_in_which_db(item)
                if which_db == 'nowhere':
                    self.had_error('List is bogus for item {} [1]'.format(item))
                    return False
                df = self.db_table[which_db]
                df = df.loc[item]
                if len(df) > 0:
                    self.list_resp += self.df_to_list_resp\
                        (pd.DataFrame(df).T, which_db, ' From '+defs.db_names[which_db])
                    self.list_resp += '\n\n'
                else:
                    self.had_error('List is bogus for item {} [2]'.format(item))
                    return False

        return True

    def tdelta_func(self):
        self.return_message_ext1 = '\n'
        if self.tdelta_param == 'clean':
            self.had_error('No timedelta param.')
            return False
        elif self.tdelta_param == 'off':
            self.tdelta = timedelta(days=0)
            self.return_message_ext1 += 'Timedelta set to zero\n'
        elif self.tdelta_param == 'printout':
            self.return_message_ext1 += 'Timedelta is {} (backwards)'.\
                format(self.tdelta)
        else: #creating timedelta
            self.tdelta = timedelta(days=float(self.tdelta_param))
            self.return_message_ext1 += 'Timedelta set to {} days.\n'.\
                format(self.tdelta_param)
        return True

