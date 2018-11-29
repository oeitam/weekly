# this file includes definitions, strings, help, etc for the weekly project

from ast import literal_eval

import configparser
import os
from datetime import datetime, timedelta #, date, time, timedelta

debug_delta = timedelta(days=0)



future = datetime.strptime('31/Dec/2099', '%d/%b/%Y')


days_of_week = {'Sun': '-0',
                'Mon': '-1',
                'Tue': '-2',
                'Wed': '-3',
                'Thu': '-4',
                'Fri': '-5',
                'Sat': '-6',
                }

# an alternate die command, so all commands in test_defs can be run
#die_word = 'kil'
die_word = 'die'


# columns definitions for the data bases
# megaprojects
dfm_columns = ['Name',
               'State',
               'PROJECTs_List',
               'Description',
               ]
# projects
dfp_columns = ['Name',
               'State',
               'MEGAPROJECT',
               'Description',
               'Tag',
               'Start_Time',
               'State_Time',
               'State_Text'
               ]
# tasks
dft_columns = ['State',
               'Description',
               'Start_Date',
               'PROJECT',
               'Tag',
               # optional from here
               'Due_Date',
               'Expiration_Date',
               'Wakeup_Date',
               'Location',
               'Context',
               #'Reminders',
               'ACTIVITYs',
               'Sub_TASKs',
               'Parent_TASK',
               'Start_Time',
               'State_Time',
               'State_Text'
               ]
# activities
dfa_columns = ['State',
               'Start_Date',
               'Description',
               'Tag',
               'End_Date',
               'Wakeup_Date',
               'TASK',
               'Task_Name',
               'PROJECT',
               'Project_Name',
               'Start_Time',
               'State_Time',
               'State_Text'
               ]

all_col = { 'megaproject' : dfm_columns ,
            'project'     : dfp_columns ,
            'task'        : dft_columns ,
            'activity'    : dfa_columns ,
            }

# columns to print
dfm_columns_to_print = ['Name',
                        'State',
                        #'PROJECTs_List',
                        'Description'
                        ]
# projects
dfp_columns_to_print = ['Name',
                        'State',
                        'MEGAPROJECT',
                        'Description',
                        'Tag',
                        ]
# tasks
dft_columns_to_print = ['State',
                        'Description',
                        'Start_Date',
                        'PROJECT',
                        'Tag',
                        'Wakeup_Date'
                        # optional from here
                        #'Due_Date',
                        #'Location',
                        #'Context',
                        #'Reminders',
                        #'ACTIVITYs',
                        #'Sub_TASKs',
                        #'Parent_TASK',
                         ]

dfa_columns_to_print = ['State',
                        'Start_Date',
                        'Description',
                        'Tag',
                        #'End_Date',
                        'Wakeup_Date',
                        'TASK',
                        'Task_Name',
                        'PROJECT',
                        'Project_Name',
                        ]

few_columns_to_print_table= { 'dfm' : dfm_columns_to_print ,
                              'dfp' : dfp_columns_to_print,
                              'dft' : dft_columns_to_print,
                              'dfa' : dfa_columns_to_print,
                             }
all_columns_to_print_table = { 'dfm' : dfm_columns ,
                               'dfp' : dfp_columns,
                               'dft' : dft_columns,
                               'dfa' : dfa_columns,
                              }
which_columns_to_print = [few_columns_to_print_table,
                          all_columns_to_print_table
                          ]

# activities



df_columns = { 'dfm': dfm_columns,
               'dfp': dfp_columns,
               'dft': dft_columns,
               'dfa': dfa_columns,
               }


# states definitions (all transitions are legel)
megaproject_states  = {'On' : 'The MEGAPROJECT is open',
                       'Off': 'The MEGAPROJECT is closed',
                       }

project_states   = {'Started' : 'The PROJECT started rolling',
                    'OnHold' : 'The PROJECT is not active - so nothin in it can change.',
                    'Ended'   : 'The project is concluded, done, finished.',
                    }

task_states      = {'Open'   : 'The TASK is created and may be on execution',
                    'OnHold' : 'Execution on this TASK is stopped',
                    'Closed' : 'The TASK is completed',
                    'Dormant': 'The TASK is to be completed in the future',
                    }

activity_states  = {'Started': 'The ACTIVITY is created and may be on execution',
                    'OnHold': 'Execution on this ACTIVITY is stopped',
                    'Ended'  : 'The ACTIVITY is completed',
                    'Dormant': 'The ACTIVITY is to be completed in the future',
                    }

all_stat = { 'megaproject' : megaproject_states,
             'project'     : project_states,
             'task'        : task_states,
             'activity'    : activity_states,
            }

###############
state_open = { 'dfm' : 'On',
               'dfp' : 'Started',
               'dft' : 'Open',
               'dfa' : 'Started'
               }

state_onhold = { 'dfm' : 'ERROR',
                 'dfp' : 'OnHold',
                 'dft' : 'OnHold',
                 'dfa' : 'OnHold'
                 }

state_closed = { 'dfm' : 'Off',
                 'dfp' : 'Ended',
                 'dft' : 'Closed',
                 'dfa' : 'Ended'
               }


state_Dormant = { 'dfm' : '',
                  'dfp' : '',
                  'dft' : 'Dormant',
                  'dfa' : 'Dormant'
               }

# databases name
db_names = {'dfm' : 'Megaprojects DataFrame',
            'dfp' : 'Projects DataFrame',
            'dft' : 'Tasks DataFrame',
            'dfa' : 'Activities DataFrame',
            }

###############################################################################
# check if the config file exists, and if not - craete one
def check_for_and_create_cfg():
    if not os.path.isdir(r'C:\weekly.local'):
        os.mkdir(r'C:\weekly.local')
    if not os.path.isfile(r'C:\weekly.local\weekly.local.cfg'):
        # write that file
        f = open(r'C:\weekly.local\weekly.local.cfg','w')
        f.write('\n')
        f.write(r'[MAIN]')
        f.write('\n')
        f.write(r'data_loc = C:\weekly.local')
        f.write('\n')
        f.write(r'mode_sel = 2')
        f.write('\n')
        f.write(r'local_client_script = C:\Users\oeitam\PycharmProjects\weekly\src\server\client_script.py')
        f.write('\n')
        f.write(r'dev_or_prod = production')
        f.write('\n')
        f.write('\n')
        f.close()

check_for_and_create_cfg()

config = configparser.ConfigParser()
config.read(r'C:\weekly.local\weekly.local.cfg')

dev_or_prod         = config['MAIN']['dev_or_prod']
data_loc            = config['MAIN']['data_loc']
mode_sel            = int(config['MAIN']['mode_sel'])
local_client_script = config['MAIN']['local_client_script']
use_tables          = config['MAIN']['use_tables']
max_width           = int(config['MAIN']['max_width'])
list_resp_row_limit = int(config['MAIN']['list_resp_row_limit'])
columns_print_style = int(config['MAIN']['columns_print_style'])

params_dict = { 'use_tables'          : use_tables,
                'max_width'           : max_width,
                'list_resp_row_limit' : list_resp_row_limit,
                'columns_print_style' : columns_print_style
                }

params_list = [ 'use_tables', 'max_width', 'list_resp_row_limit','dev_or_prod',
                'columns_print_style']


data_loc = data_loc + '\\' + dev_or_prod

#         -0-        -1-      -2-
mode = ['socket', 'direct', 'prod' ][mode_sel]

# columns_print_style = 0 : print less columns
# columns_print_style = 1 : print more columns
columns_to_print_table = which_columns_to_print[columns_print_style]

####################################################################################




help_message = '''
==================================
General Comments:
A.    listing returns the active (like state = Open) only. This option can be changed, see below
B.    Work Week (ww) start on Sunday
C.    the listing for time range (or others) shown here for activity (for example) work for other types 
      as well

----------------------------------

1     ci     # this shortcut creates an activity in a certain project when starting the day
2     co     # this shortcut creates an activity in a certain project when finishing the day
3     help   # prints all teh help test
3.1   help sleep     # prints all help lines with the phrase 'sleep' in them
4     die    # kills the program
5     start @00000000 | two...   # creates an activity at project or task 00000000 with Description
5.1   start @P01 state OnHold | activity #01    # start activity at project P01 at initial state OnHold 
5.2   start @123 state Dormant | activity #01    # start activity at task 123 at initial state Dormant (but no wakeup time!) 
6     create megaproject Work2 | 2all ...    # creates a megaproject with name Work2 and Description 2all ...
7     create project project_two @Work2 | th...  # create a project names project_two under megaproject Work2 with Description
8     task @project_one | 1this ...  # creates a task at project project_one with description
9     start @00000000 | two ...  # creates an activity at project or task 00000000 with Description
10    start @0 | some ...    # for testing: the program will replace the '0' with a valid project or task number
11    list search | ww26     # search for the text following the '|' in all the database items
12    list task week 18ww08  # list all tasks started/created on ww08 of 2018
13    list activity week 18ww08  # list all activities started on ww08 of 2018
14    list megaproject columns   # list the columns of the megaproject item type
15    list project columns   # list the columns of the project item type
16    list task columns      # list the columns of the task item type
17    list activity columns  # list the columns of the activity item type
18    list megaproject states    # list the possible states of megaproject items
19    list project states    # list the possible states of project items
20    list task states   # list the possible states of task items
21    list activity states   # list the possible states of activity items
22    list megaproject for project project_one   # list the megaproject items that has project project_one under them
23    list project for megaproject Work1     # list the projects under megaproject Work1
24    list task for project project_two  # list the tasks under project project_two
25    list activity for project project_one  # list the activities under project project project_one
25.1  list activity state all for project project_one    # list the activities (in all states: Open, OnHold, etc.) under project project project_one
25.2  list activity for project project_one state all    # list the activities (in all states: Open, OnHold, etc.) under project project project_one
26    list activity for task @2334   # list activities that are under task with ID 2334
27    list activity col Start_Date drange 17ww17.Sun 17ww20.Mon  # based on column Start_Date, for date range from Sunday, ww17 in 2017 up to Mon
27.1  list activity col Start_Date drange 17ww17.Sun 17ww20.Mon  # of ww20 in 2017 - list all the activites (in Open state)
28    list activity col Start_Date drange 17ww17 17ww20.Mon  # based on column Start_Date, for date range from begining of ww17 in 2017 (practically - Sunday)
28.1  list activity col Start_Date drange 17ww17 17ww20.Mon  # up to Mon of ww20 in 2017 - list all the activites (in Open state)
29    list activity col Start_Date drange 17ww17.Sun 17ww20  # based on column Start_Date, for date range from Sunday of ww17 in 2017 
29.1  list activity col Start_Date drange 17ww17.Sun 17ww20  # up to end of (all of) ww20 in 2017 - list all the activites (in Open state)
30    list activity col Start_Date drange 17ww17 17ww20  # based on column Start_Date, for date range from begining of ww17 in 2017 (practically - Sunday)
30.1  list activity col Start_Date drange 17ww17 17ww20  # up to end of ww20 in 2017 - list all the activites (in Open state)
30.2  list activity col Start_Date drange 17ww17 17ww20  # ( meaning all of these weeks plus all between)
31    list activity col Start_Date drange bot 17ww20.Mon     # based on column Start_Date, for date range from the very early activity ("bot" for bottom) 
31.1  list activity col Start_Date drange bot 17ww20.Mon     # up toMonday of ww20 in 2017
32    list activity col Start_Date drange bot 17ww20     # based on column Start_Date, for date range from the very early activity ("bot" for bottom) 
32.1  list activity col Start_Date drange bot 17ww20     # up to all of www20 in 2017 (including)
33    list activity col Start_Date drange 17ww17.Sun top     # based on column Start_Date, for date range from begining Sunday of ww17 in 2017
33.1  list activity col Start_Date drange 17ww17.Sun top     # up to the very latest (== recent) entry ("top" for top of the list)
34    list activity col Start_Date drange 17ww17 top     # based on column Start_Date, for date range from begining of ww17 in 2017 (practically - Sunday)
34.1  list activity col Start_Date drange 17ww17 top     # up to the very latest (== recent) entry ("top" for top of the list)
35    list activity col Start_Date drange bot top    # based on column Start_Date, list from earliets to latest == list all!
36    list megaproject col ID irange 2569 2631   # list megaproject items from ID 2569 to ID 2631
37    list megaproject col ID irange 2569 top    # list megaproject items with ID >= 2569 (meaning - from 2569 and up)
38    list megaproject col ID irange bot 2631    # list megaproject items with ID <= 2631 (meaning - up to 2631)
39    list megaproject col ID irange bot top     # list megaproject items - all IDs == print all !
40    halt @00000000     # halt item with ID 0000000 ==> move it to 'OnHold' state
41    stop @00000000     # stop item with ID 0000000 ==> Move it to off state like 'Ended', 'Closed' or 'Off'
42    cont @00000000     # cont item with ID 0000000 ==> move it (back) to active state like 'On', 'Started' or 'Open'
43    t | doing this something today     # if the 't' shortcut exists - used to craete an activity in a project that tracks my daily activities.
44    delete @1234   # remove item with ID 1234 from the database
45    list task week 18ww08 state OnHold     # list tasks crated on ww18 of 2018 that are of state OnHold
46    list activity state Ended week 18ww08  # list activity with state Ended that were created on ww 8 of 2018 
46.1  list activity state Ended week 18ww08 listall # list activities with all states that were created on ww 8 of 2018
47    sleep @11540 17ww50.Tue    # move item with ID 11540 to state 'Dormant' and set a wakeup date for Tuesday of ww50 in 2018
48    sleep @11540 17ww50    # move item with ID 11540 to state 'Dormant' and set a wakeup date for ww50 in 2018 (Sunday practically)
49    sleep @10687 20171205  # move item with ID 11540 to state 'Dormant' and set a wakeup date for Dec 5th, 2017
50    sleep @10673 plus 88   # move item with ID 11540 to state 'Dormant' and set a wakeup date in 88 days
51    sleep @10673   # move item with ID 11540 to state 'Dormant', with no wakeup date
52    list wakeup    # list all the items that have a wakeup date up to now and are still in 'Dormant' state
53    move task from test1 to test2  # move all the tasks from project test1 to project test 2
54    move activity from test1 to test2 state OnHold # mova all activities with state 'OnHold' from PROJECT test1 to 
54.1  move activity from test1 to test2 state OnHold # project test2. Note: does not handle activities under TASKs !
55    create list @10677 @10678 @10679   # creates an data structure inside the program which is a list of the following IDs
55.1  create list @10677 @10678 @10679   # 10677, 10678 and 10679. Following actions can operate on this list of items 
56    move list to test2     # move the items (tasks or activities) in the internal list (see help item 55) to PROJECT test2
57    move @10661 to test2   # move item with ID 10662 to (project) test2
58    set max_width value 13     # set the parameter max_width to 13 (controls the width of columns in printed tables)
59    list parameter     # list all the parameters and their value
60    list shortcut  # list all the shortcuts in effect
61    create shortcut | ["simple_substitution", "co", "start @10758 | checking out - go home"]   # see next lines
61.1  create shortcut ...    # simple substitution - user writes 'co' and the program see 'start @10768 | .... home'
61.2  create shortcut | ["pipe_substitution", "lulu", "start @12969"]    # see next lines
61.3  create shortcut ...    # substitution like user: 'lulu | bla bla bla' becomes 'start @12969 | bla bla bla'
62    delete shortcut 5  # deletes shortcut number 5
63    tag @10673 tag_two     # adds tag 'tag_two' to item 10673
64    tag project UNIQUE tag_for_proj_one    # tag the project named UNIQUE with tag tag_for_proj_one
65    list tag tag_for_proj_one  # list all teh items with tag tag_for_proj_one
66    list tag   # list all the tagged items
67    tag list TAG_FOR_LIST  # tag all the items in a defined list (see help 55) with tag TAG_FOR_LIST
68    list task tag tag_for_proj_one     # list all the tasks with tag tag_for_proj_one
69    list activity tag tag_for_proj_one     # list all the activities with tag tag_for_proj_one
70    list project tag tag_for_proj_one  # list all the projects with tag tag_for_proj_one
71    list activity tag tag_for_proj_one col Start_Date drange bot 17ww20    # list activities with tag tag_for_proj_one
71.1  list activity tag ...  # within the defined date range (see help 32 for example on date range)
72    list activity col Start_Date drange bot 17ww20 tag tag_for_proj_one    # list activities with tag tag_for_proj_one
72.1  list activity col ...  # within the defined date range (see help 32 for example on date range) (same as help 71, order change)
72.2  list activity listall col Start_Date drange bot 17ww20 tag tag_for_proj_one # same as help 72, but all items at once 
73    task @project_one tag QQQ1| some task  # create a task at project_one with tag QQQ1
74    start @13849 tag QQQ1 | some activity  # start an ectivity under item 13847 with tag QQQ1 
75    create project MYPROJ @Work1 tag QQQ1 | some proj desc     # create project MYPROJ under megaproject Work1 with tag QQQ1
76    timedelta  # print the value of the time backwords the system is set for. Used for entring items in the past
77    timedelta 10   # set the time of the system for marking items creation time 10 days beack
78    timedelta off  # set the time back to preset. Cancel any timedelta setting
79    list task lastdays 17  # list the tasks created in the last 17 days
80    create megaproject CB1 fromcb  # create a megaproject named CB1, taking the Description from the Windows Clipboard (cb)
81    create project P1 @CB1 fromcb  # create project P1 under megaproject CB1, taking the Description from the 
81.1  create project P1 @CB1 fromcb  # Windows Clipboard (cb)
82    task @P1 fromcb    # Start a task in project P1 with description taken from Windows Clipboard
83    start @P1 fromcb   # Start an activity in project P1 with description taken from Windows Clipboard
84    set columns_print_style 1  # set the parameter columns_print_style to 1 ('1' prints all columns of the DB, '0' just the 
84.1  set columns_print_style 1  # essential. 0 is default)
85    cont @14512 | cont text    # change state of item 14512 to active state, and add 'cont text' to State_Text field. 
86    halt @14513 | halt text    # change state of item 14512 to OnHold state, and add 'halt text' to State_Text field. 
87    stop @14514 | stop text    # change state of item 14512 to non-active state, and add 'stop text' to State_Text field. 
88    sleep @14512 plus 88 | sleep text  # change state of item 14512 to Dormant state, set wakeup date in 88 days,
88.1  sleep @14512 plus 88 | sleep text  # and add 'sleep text' to State_Text field. 
89    edit @14512 | new text for the Description of the item     # change the Description of item 14512 to 'new text .... the item'
90    push @14476 @14521     # put the later one of the two items on top of the other one, pushing the rest down
91    list task state all sort AI   # list all tasks of all states, sort results by code AI. code AI means sorting by order of tags,
91.1  list task state all sort AI   # if exist 'AI01', 'AI02' etc.. and later the rest
92    list activity sort AI state all   # list all activities of all states sorting by code AI (see help 91)
93    list @114     # list the details of item with ID 114, searching for it in all 4 databases
94    list @114 hier    # list the details of item with ID 114, and also print items in its hierarchy, up or down
95
96
97

==================================
'''

# ====================================================


