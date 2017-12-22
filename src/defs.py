# this file includes definitions, strings, help, etc for the weekly project

from ast import literal_eval

import configparser
import os
from datetime import datetime, timedelta #, date, time, timedelta

debug_delta = timedelta(days=0)

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

params_dict = { 'use_tables': use_tables,
                'max_width': max_width,
                'list_resp_row_limit': list_resp_row_limit
                }

params_list = [ 'use_tables', 'max_width', 'list_resp_row_limit','dev_or_prod']


data_loc = data_loc + '\\' + dev_or_prod


future = datetime.strptime('31/Dec/2099', '%d/%b/%Y')

#         -0-        -1-      -2-
mode = ['socket', 'direct', 'prod' ][mode_sel]

days_of_week = {'Sun': '-0',
                'Mon': '-1',
                'Tue': '-2',
                'Wed': '-3',
                'Thu': '-4',
                'Fri': '-5',
                'Sat': '-6',
                }


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
               ]
# activities
dfa_columns = ['State',
               'Start_Date',
               'Description',
               'Tag',
               'End_Date',
               'Wakeup_Date',
               'TASK',
               'PROJECT'
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
                        'Description',
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
                        #'TASK',
                        #'PROJECT'
                        ]

columns_to_print_table = { 'dfm' : dfm_columns_to_print ,
                           'dfp' : dfp_columns_to_print,
                           'dft' : dft_columns_to_print,
                           'dfa' : dfa_columns_to_print,
                           }
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
db_names = {'dfm': 'Megaprojects DataFrame',
            'dfp': 'Projects DataFrame',
            'dft': 'Tasks DataFrame',
            'dfa' : 'Activities DataFrame',
            }






help_message = '''
==================================
1    ci
2    co
3    help 
3.1  help sleep
4    die
5    start @00000000 | two...
6    create megaproject Work2 | 2all ...
7    create project project_two @Work2 | th...
8    task @project_one | 1this ...
9    start @00000000 | two ...
10   start @0 | some ...
11   list search | ww26
12   list activity ww 17
13   list task ww 17
14   list megaproject columns
15   list project columns
16   list task columns
17   list activity columns
18   list megaproject states
19   list project states
20   list task states
21   list activity states
22   list megaproject for project project_one
23   list project for megaproject Work1
24   list task for project project_two
25   list activity for project project_one
25.1 list activity state all for project project_one
25.2 list activity for project project_one state all
26   list activity for task @2334
27   list activity col Start_Date drange 17ww17.Sun 17ww20.Mon
28   list activity col Start_Date drange 17ww17 17ww20.Mon
29   list activity col Start_Date drange 17ww17.Sun 17ww20
30   list activity col Start_Date drange 17ww17 17ww20
31   list activity col Start_Date drange bot 17ww20.Mon
32   list activity col Start_Date drange bot 17ww20
33   list activity col Start_Date drange 17ww17.Sun top
34   list activity col Start_Date drange 17ww17 top
35   list activity col Start_Date drange bot top
36   list megaproject col ID irange 2569 2631
37   list megaproject col ID irange 2569 top
38   list megaproject col ID irange bot 2631
39   list megaproject col ID irange bot top
40   halt @00000000
41   stop @00000000
42   cont @00000000
43   today | doing this something today
44   delete @1234
45   list task ww 17 state OnHold
46   list activity state Ended ww 17
47   sleep @11540 17ww50.Tue
48   sleep @11540 17ww50
49   sleep @10687 20171205
50   sleep @10673 plus 88
51   sleep @10673
52   list wakeup
53   move task from test1 to test2
54   move activity from test1 to test2 state OnHold
55   create list @10677 @10678 @10679
56   move list to test2
57   move @10661 to test2
58   set max_width value 13
59   list parameter
60   list shortcut
61   create shortcut | ["simple_substitution", "co", "start @10758 | checking out - go home"]
62   delete shortcut 5
63   tag @10673 tag_two
64   tag project UNIQUE tag_for_proj_one
65   list tag tag_for_proj_one
66   list tag
67   tag list TAG_FOR_LIST
68   list task tag tag_for_proj_one
69   list activity tag tag_for_proj_one
70   list project tag tag_for_proj_one
71   list activity tag tag_for_proj_one col Start_Date drange bot 17ww20
72   list activity col Start_Date drange bot 17ww20 tag tag_for_proj_one
73   task @project_one tag QQQ1| some task
74   start @13849 tag QQQ1 | some activity
75   create project MYPROJ @Work1 tag QQQ1 | some proj desc
76   timedelta
77   timedelta 10
78   timedelta off
 
==================================
'''

# ====================================================


